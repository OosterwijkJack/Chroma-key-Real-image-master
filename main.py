import math
import os
import time
from numpy import asarray, copy
from PIL import Image
import matplotlib.pyplot as plt


"""

Program replaces background of image based on chroma key and tolerance
(With example images chrome key [0,255,0] and tolerance 200 seems to work pretty well)

Author: Jack Oosterwijk

"""

class Vec3:  #  vector 3 class (used to handle colors nicely)
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"


def get_distance(a: Vec3, b: Vec3):
    return math.sqrt( math.pow(b.x - a.x, 2) + math.pow(b.y - a.y,2) + math.pow(b.z - a.z,2) ) # distance formula

def valid_chroma_key(key: Vec3):  #  Checks if chroma keys values are withing 0-255
    if True in [x > 255 or x < 0 for x in (key.x, key.y, key.z)]:
        print("Invalid chroma key")
        time.sleep(3)
        exit()


def get_image():
    fg = Image.open(r"Image/foreground.jpeg")
    bg = Image.open(r"Image/background.jpeg")

    # resize background to match foreground
    bg = bg.resize((fg.width, fg.height), Image.Resampling.LANCZOS)
    return copy(asarray(fg)), copy(asarray(bg)) # return copy so array is writeable

def is_tolerant(chroma: Vec3, color: Vec3, tolerance):  # check of color is tolerated based on chroma and tolerance level
    return get_distance(color, chroma) <= tolerance


def main():
    tolerance = int(input("Enter chroma key tolerance (0-255): "))

    if tolerance > 255 or tolerance < 0:
        print("Invalid Tolerance.")
        time.sleep(3)
        exit()

    chroma_key = ([int(input(f"Enter {x} value of chroma key: ")) for x in ("r", "g", "b")])
    chroma_key = Vec3(chroma_key[0], chroma_key[1], chroma_key[2])   

    valid_chroma_key(chroma_key)

    fg, bg = get_image()

    # Loop through each pixel and replace pixels tolerated by chroma key with corresponding background pixel
    for i, ii in enumerate(fg):
        for a, aa in enumerate(ii):
            if is_tolerant(chroma_key, Vec3(aa[0], aa[1], aa[2]), tolerance):
                fg[i][a] = bg[i][a]
    plt.imshow(fg)
    plt.show()
    plt.imsave(r"Result/result.jpeg", fg)


if __name__ == "__main__":
    os.system("cls")
    main()
