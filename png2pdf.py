import os
import img2pdf

path = '../' + input('IB/')
os.chdir(path)
pngs = os.listdir()
with open('main.pdf', 'wb') as f:
    f.write(img2pdf.convert(pngs))
