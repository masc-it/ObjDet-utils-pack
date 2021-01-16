import os.path
from pathlib import Path
from shutil import copyfile
from PIL import Image
import argparse
import pandas as pd
import xml.etree.ElementTree as ET


def resize_bbox(bbox, in_size, out_size):

    bbox = bbox.copy()
    y_scale = float(out_size[1]) / in_size[1]
    x_scale = float(out_size[0]) / in_size[0]
    
    # xmin, ymin
    bbox[0] = x_scale * int(bbox[0])
    bbox[1] = y_scale * int(bbox[1])
    
    # xmax, ymax
    bbox[2] = x_scale * int(bbox[2])
    bbox[3] = y_scale * int(bbox[3])
      
    return bbox
    
    
    
def patch_labels_yolo( img_name, img_width, img_height, new_width, new_height):
    
    with open("labels_ok/" + img_name.replace(".jpg", "") +".txt") as f:
        lines = f.readlines()
    
    with open("train_labels.csv", "a") as f:
        for line in lines:
            parts = line.split(" ")
            filename = img_name
            class_id = parts[0]
            
            width = float(parts[3])*img_width
            height = float(parts[4])*img_height
            
            xmin = float(parts[1])*img_width - (width/2)
            ymin = float(parts[2])*img_height - (height/2)
            
            xmax = xmin + width
            ymax = ymin + height
            
            width_1 = new_width
            height_1 = new_height
            
            new_coords = resize_bbox([xmin, ymin, xmax, ymax], (img_width, img_height), (new_width, new_height))
            f.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (filename, str(width_1), str(height_1), "cell", str(int(new_coords[0])), str(int(new_coords[1])), str(int(new_coords[2])), str(int(new_coords[3]))))
            print(new_coords)
        f.close()
        

def patch_labels( fold_name, img_name, img_width, img_height, new_width=300, new_height=300):
    
    with open(fold_name +"/labels/" + img_name.replace(".jpg", ".txt")) as f:
        lines = f.readlines()
    
    with open(fold_name + "_labels.csv", "a") as f:
        for line in lines:
            parts = line.split(" ")
            filename = img_name
            class_id = parts[0]
             
            xmin = float(parts[1])
            ymin = float(parts[2])
            
            xmax = float(parts[3])
            ymax = float(parts[4])
            
            width_1 = new_width
            height_1 = new_height
            
            new_coords = resize_bbox([xmin, ymin, xmax, ymax], (img_width, img_height), (new_width, new_height))
            f.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (filename, str(width_1), str(height_1), "person", str(int(new_coords[0])), str(int(new_coords[1])), str(int(new_coords[2])), str(int(new_coords[3]))))
            print(new_coords)
        f.close()
        
        
def patch_labels_xml( fold_name, img_name, img_width, img_height, new_width=None, new_height=300):
    
    xml_list = []
    
    tree = ET.parse(fold_name +"/labels/" + img_name.replace(".jpg", ".xml"))
    root = tree.getroot()
    for member in root.findall('object'):
        
        if new_width == None:
            value = (root.find('filename').text.replace(".jpeg", ".jpg"), # filename
                    int(root.find('size')[0].text), # width
                    int(root.find('size')[1].text), # height
                    member[0].text, # class
                    int(member[4][0].text), # xmin
                    int(member[4][1].text), # ymin
                    int(member[4][2].text), # xmax
                    int(member[4][3].text)  # ymax
                    )
        else:
            resized_bbox = resize_bbox([float(member[4][0].text), float(member[4][1].text), float(member[4][2].text), float(member[4][3].text)], (int(root.find('size')[0].text),int(root.find('size')[1].text)), (new_width, new_height))
            value = (root.find('filename').text.replace(".jpeg", ".jpg"), # filename
                    int(new_width), # width
                    int(new_height), # height
                    member[0].text, # class
                    int(resized_bbox[0]), # xmin
                    int(resized_bbox[1]), # ymin
                    int(resized_bbox[2]), # xmax
                    int(resized_bbox[3])  # ymax
                    )
        xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    xml_df.to_csv(fold_name + "_labels.csv",mode='a', index=None, header=False)


        
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Build csv")
    parser.add_argument('-m', '--mode', type=str, required=True, help='xml, yolo')
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')
    parser.add_argument('-s', '--newsize', type=int, nargs=2, required=True, metavar=('width', 'height'), help='Directory containing the images')

    args = parser.parse_args()

    for t in ["train", "test"]:
        images = Path(args.directory + "/" + t + "/imgs").iterdir()  
        f = open(args.directory + "/" + t + "_labels.csv", "w")
        f.write("filename,width,height,class,xmin,ymin,xmax,ymax\n")
        f.close()
        for img in images:
            image = Image.open(img)
            (width, height) = image.size
            if args.mode == "xml":
                patch_labels_xml(args.directory + "/" + t, os.path.basename(img), width, height, args.newsize[0], args.newsize[1])
            elif args.mode == "yolo":
                patch_labels_yolo(args.directory + "/" + t, os.path.basename(img), width, height, args.newsize[0], args.newsize[1]) # to fix
            else:
                patch_labels(args.directory + "/" + t, os.path.basename(img), width, height, args.newsize[0], args.newsize[1])                
            print("\n\n")
        
