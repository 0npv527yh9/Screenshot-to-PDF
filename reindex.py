import os

def main():
    d = os.getcwd()
    path = '../' + input('IB/')
    os.chdir(path)
    files = get_pngs()
    reindex(files)
    os.chdir(d)

def get_pngs():
    files = os.listdir()
    files = list(filter(lambda file : file[-4:].lower() == '.png', files))
    return files

def reindex(files):
    files.sort()
    for i, file in enumerate(files, 1):
        os.rename(file, f'{str(i).zfill(3)}.png')

if __name__ == '__main__':
    main()
