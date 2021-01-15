import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import argparse


def resize_bbox(bbox, in_size, out_size):

    bbox = bbox.copy()
    y_scale = float(out_size[1]) / in_size[1]
    x_scale = float(out_size[0]) / in_size[0]
    
    # xmin, ymin
    bbox[0] = x_scale * bbox[0]
    bbox[1] = y_scale * bbox[1]
    
    # xmax, ymax
    bbox[2] = x_scale * bbox[2]
    bbox[3] = y_scale * bbox[3]
      
    return bbox


def xml_to_csv(path, folder, old_size=None, new_size=None ):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            
            if old_size == None:
                value = (root.find('filename').text, # filename
                        int(root.find('size')[0].text), # width
                        int(root.find('size')[1].text), # height
                        member[0].text, # class
                        int(member[4][0].text), # xmin
                        int(member[4][1].text), # ymin
                        int(member[4][2].text), # xmax
                        int(member[4][3].text)  # ymax
                        )
            else:
                resized_bbox = resize_bbox([int(member[4][0].text), int(member[4][1].text), int(member[4][2].text), int(member[4][3].text)], (int(root.find('size')[0].text),int(root.find('size')[1].text)), new_size)
                value = (root.find('filename').text, # filename
                        int(new_size[0]), # width
                        int(new_size[1]), # height
                        member[0].text, # class
                        int(resized_bbox[0]), # xmin
                        int(resized_bbox[1]), # ymin
                        int(resized_bbox[2]), # xmax
                        int(resized_bbox[3])  # ymax
                        )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    parser = argparse.ArgumentParser(description="convert xml to csv")
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')
    parser.add_argument('-i', '--in_s', type=int, nargs=2, metavar=("width", "height"),  help='initial size (w x h)')
    parser.add_argument('-o', '--out_s', type=int, nargs=2, metavar=("width", "height"), help='new size (w x h)')
    args = parser.parse_args()
    
    for folder in ['train', 'test']:
        image_path = os.path.join(args.directory, ( folder, "labels"))
        xml_df = xml_to_csv(image_path, folder, args.in_s, args.out_s)
        xml_df.to_csv(os.path.join(args.directory,folder+'_labels.csv'), index=None)
    print('Successfully converted xml to csv.')


main()