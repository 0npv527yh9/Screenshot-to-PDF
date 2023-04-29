# %%
import os
import os.path
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory
from typing import Callable

from PIL import ImageGrab

import resolution


def main():
    root = App()
    root.mainloop()


class App(tk.Tk):

    def __init__(self):
        resolution.adapt()
        super().__init__()
        self.next_frame: dict[str, Callable] = {
            'setting': self.switch_shot_frame
        }

        self.switch_setting_frame()

    def switch_setting_frame(self):
        self.title('Setting')
        frame = tk.Frame(self)

        def add_label(row: int, text: str):
            tk.Label(frame,
                     text = text).grid(row = row, column = 0, sticky = tk.W)

        add_label(0, 'Save directory')
        path_label = tk.Label(frame, text = os.getcwd(), anchor = tk.W)
        path_label.grid(row = 0, column = 1, sticky = tk.EW)

        def set_path():
            path = askdirectory()
            path_label.configure(text = path)

        tk.Button(frame, text = '...', command = set_path) \
            .grid(row = 0, column = 2, sticky = 'news')

        add_label(1, 'Start number')
        spinbox = ttk.Spinbox(frame, from_ = 0, to = float('inf'))
        spinbox.insert(0, '0')
        spinbox.grid(row = 1, column = 1, columnspan = 2, sticky = tk.EW)

        @self.register
        def validate(value):
            return value == '' or value.isdigit()

        @self.register
        def invalid(value):
            spinbox.delete(0, tk.END)
            spinbox.insert(0, value)

        spinbox.configure(
            validatecommand = (validate, '%P'),
            invalidcommand = (invalid, '%s'),
            validate = 'key'
        )
        spinbox.get()

        def command():
            try:
                path: str = path_label.cget('text')
                start_number = int(spinbox.get())
                if os.path.isdir(path):
                    os.chdir(path)
                    frame.pack_forget()
                    self.next_frame['setting'](start_number = start_number)
            except:
                pass

        tk.Button(frame, text = 'Start', command = command) \
            .grid(row = 2, column = 0, columnspan = 3)

        frame.columnconfigure(1, weight = 1)
        frame.pack(fill = tk.X)

        self.resizable(True, False)

    def switch_shot_frame(self, *, start_number: int):
        self.title('Press [Enter] to take a screenshot')
        self.resizable(True, True)
        self.geometry('500x500')

        frame = tk.Frame(self)

        if os.name == 'nt':
            transparent_color = 'blue'
            frame['bg'] = transparent_color
            self.attributes("-transparentcolor", transparent_color)
        else:
            self.wm_attributes("-transparent", True)
            frame['bg'] = 'systemTransparent'

        margin = 20
        frame.pack(padx = margin, pady = margin, expand = True, fill = tk.BOTH)

        self.config(background = 'red')

        i = start_number

        def shot(_):
            x = self.winfo_rootx() + frame.winfo_x()
            y = self.winfo_rooty() + frame.winfo_y()
            x2 = x + frame.winfo_width()
            y2 = y + frame.winfo_height()

            self.withdraw()
            image = ImageGrab.grab((x, y, x2, y2))
            self.deiconify()

            nonlocal i
            file = '{:0>3}.png'.format(i)
            i += 1

            image.save(file, quality = 100)
            print('TAKEN:', file)

        self.bind('<Return>', func = shot)

        def end_process():
            from tkinter.messagebox import askyesno
            yes = askyesno(message = 'Convert image to pdf?')
            if yes:
                png_list = ['{:0>3}.png'.format(j) for j in range(i)]
                import png2pdf
                png2pdf.convert(png_list)
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", end_process)


if __name__ == '__main__':
    main()
