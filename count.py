import re

def main():
    file = '../' + input('path >> IB/')
    s = read(file)
    s = replace(s)
    print(s)
    print(len(s))

def read(file):
    with open(file, encoding = 'utf-8') as f:
        return f.read()

def replace(s):
    return re.sub('[ \n\t#@]', '', s)

if __name__ == '__main__':
    main()
