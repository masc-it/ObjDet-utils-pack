import os.path
from pathlib import Path
from shutil import copyfile


if __name__ == '__main__':
    images = Path(".").iterdir()
    
    i = 1
    for img in images:
        try:
            copyfile(img, "imgs/%s.jpg" % str(i))
            i = i + 1
        except FileNotFoundError:
            print(os.path.basename(img)+".txt")
