import os

from PIL import Image
from PyPDF2 import PdfMerger


def convert(path: str):
    os.chdir(path)
    png_list = sorted(
        filter(
            lambda f: f.endswith('.png'), os.listdir()
        )
    )

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
