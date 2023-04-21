from tkinter import filedialog, Tk
import pyautogui as gui
import time

file = 'config.txt'
home = r'C:\Users\tafh0\OneDrive\デスクトップ\IB'

def main():
    path, region = get_config()
    start(path, region)

def get_config():
    res = gui.confirm(text = '初期化しますか？', buttons = ['Yes', 'No'])
    if res == 'Yes':
        root = Tk()
        root.withdraw()
        path = filedialog.askdirectory(initialdir = home)
        root.destroy()
        region = get_region()
    else:
        with open(file, encoding = 'utf-8') as f:
            s = f.read()
        s = s.split('\n')
        path = s[0]
        region = tuple(map(int, s[1].split()))
    return path, region

def get_region():
    gui.alert(text = '左上にマウスを合わせる')
    x1, y1 = gui.position()
    gui.alert(text = '右下にマウスを合わせる')
    x2, y2 = gui.position()
    w = x2 - x1
    h = y2 - y1
    return x1, y1, w, h

def start(path, region):
    i = int(gui.prompt(text = '先頭ページ', default = 1))
    while True:
        cmd = gui.confirm(buttons = ('shot', 'resize'))
        if cmd == 'shot':
            time.sleep(0.25)
            image = gui.screenshot(f'{path}/{str(i).zfill(3)}.png', region = region)
            i += 1
        elif cmd == 'resize':
            region = get_region()
        else:
            break
    save_config(path, region)

def save_config(path, region):
    s = path + '\n' + ' '.join(map(str, region))
    with open(file, 'w', encoding = 'utf-8') as f:
        f.write(s)

if __name__ == '__main__':
    main()
