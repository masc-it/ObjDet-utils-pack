import os
import argparse
from shutil import copyfile, copy

def main():
    parser = argparse.ArgumentParser(description="setup dataset dir")
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')
    #parser.add_argument('-i', '--in_s', type=int, nargs=2, metavar=("width", "height"),  help='initial size (w x h)')
    # parser.add_argument('-o', '--out_s', type=int, nargs=2, metavar=("width", "height"), help='new size (w x h)')
    args = parser.parse_args()
    
    for folder in ['train', 'test']:
        os.makedirs('%s/%s/imgs' % (args.directory, folder), exist_ok=True)
        os.makedirs('%s/%s/imgs_boxes' % (args.directory, folder), exist_ok=True)
        os.makedirs('%s/%s/imgs_resized' % (args.directory, folder), exist_ok=True)
        os.makedirs('%s/%s/labels'% (args.directory, folder), exist_ok=True)
        copy("D:\Projects\python\od_utils\labelmap.pbtxt", args.directory)

main()