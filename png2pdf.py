import os
from tkinter.filedialog import askdirectory

import img2pdf

import resolution


def main():
    resolution.adapt()

    path = askdirectory()
    os.chdir(path)

    png_list = sorted(filter(lambda f: f.endswith('.png'), os.listdir()))
    reindex(png_list)
    convert(png_list)


def reindex(png_list: list[str]):
    for i in range(len(png_list)):
        new_name = '{:0>3}.png'.format(i)
        os.rename(png_list[i], new_name)
        png_list[i] = new_name


def convert(png_list: list[str]):
    with open('output.pdf', 'wb') as f:
        b = img2pdf.convert(png_list)
        assert b is not None
        f.write(b)
