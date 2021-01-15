import cv2
from pathlib import Path
import os.path
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="show boxes")
    parser.add_argument('-b', '--base', type=str, required=True, help='Directory containing the images')
    parser.add_argument('-l', '--labelfile', type=str, required=True, help='labels file')
    args = parser.parse_args()
    
    i = 0
    images = Path(args.base + "/imgs_resized").iterdir()
    lines = open(args.labelfile).readlines()
    
    for img in images:
        #if i < 3:
        imgg = cv2.imread(str(img))
        
        for line in lines:
            box = line.split(",")
            if os.path.basename(img) in line:
                cv2.rectangle(imgg,(int(box[4]),int(box[5])), (int(box[6]),int(box[7])),(0,255,0),1)
        
        cv2.imwrite(args.base + "/imgs_boxes/"+ os.path.basename(img), imgg)
        #cv2.imshow("we", imgg)
        i = i + 1
        #cv2.waitKey(0)
                