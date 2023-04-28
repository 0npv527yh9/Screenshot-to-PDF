import os
from tkinter.filedialog import askdirectory

import resolution


def main():
    resolution.adapt()

    path = askdirectory()
    os.chdir(path)

    png_list = sorted(filter(lambda f: f.endswith('.png'), os.listdir()))
    for i, png in enumerate(png_list):
        os.rename(png, '{:0>3}.png'.format(i))


if __name__ == '__main__':
    main()
