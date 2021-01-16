import os.path
from pathlib import Path
from shutil import copyfile
import argparse
import cv2
    

def rotate_img(basepath, info, labelsfile):
    
    imgname = info[0]
    if imgname == "filename":
        return 
    imgg_orig = cv2.imread(basepath + "/" + imgname)
    
    imgg_rot = cv2.rotate(imgg_orig, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite(basepath + "/" + imgname.replace(".jpg", "_1.jpg"), imgg_rot)
    
    # (ymin, width-xmax), (ymax, height-xmin)
    labelsfile.write( imgname.replace(".jpg", "_1.jpg") + "," + info[1] + "," + info[2]
        + "," + info[3] + "," + info[5] + "," + str(int(info[1]) - int(info[6])) + "," + info[7].strip()
        + "," + str(int(info[2]) - int(info[4])) + "\n")
    
    imgg_rot2 = cv2.rotate(imgg_orig, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(basepath + "/" + imgname.replace(".jpg", "_2.jpg"), imgg_rot2)
    
    # (width-ymax, xmin), (height-ymin, xmax)

    labelsfile.write( imgname.replace(".jpg", "_2.jpg") + "," + info[1] + "," + info[2]
        + "," + info[3] + "," + str(int(info[1]) - int(info[7].strip())) + "," + info[4] + "," + str(int(info[2]) - int(info[5]))
        + "," + info[6] + "\n")
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="augment from csv")
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')
    parser.add_argument('-l', '--labels', type=str, required=True, help='Directory containing the images')

    args = parser.parse_args()
    lines = open(args.labels).readlines()
    
    with open(args.labels, "a") as f:
        
        for line in lines:
            info = line.split(",")
            rotate_img(args.directory, info, f)
    
    f.close()
    