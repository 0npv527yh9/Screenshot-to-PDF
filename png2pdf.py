import os
from tkinter.filedialog import askdirectory

from PIL import Image
from PyPDF2 import PdfMerger

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
    merger = PdfMerger()
    pdf_list = []
    for png in png_list:
        with Image.open(png) as image:
            pdf = png.split('.')[0] + '.pdf'
            image.convert('RGB').save(pdf)
            merger.append(pdf)
            pdf_list.append(pdf)

    merger.write('output.pdf')
    merger.close()

    for pdf in pdf_list:
        os.remove(pdf)
