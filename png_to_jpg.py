from PIL import Image, ImageFile
import os
import argparse
import cv2
from pathlib import Path

ImageFile.LOAD_TRUNCATED_IMAGES = True

def rescale_images(img):
    
    image = cv2.imread(str(img))
    # Save .jpg image
    cv2.imwrite(str(img).replace(".png", ".jpg"), image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rescale images")
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')
    args = parser.parse_args()
    
    for t in ["train", "test"]:
        images = Path(args.directory + "/" + t + "/imgs").iterdir()
        
        for img in images:
            rescale_images(img)
