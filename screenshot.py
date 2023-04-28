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
                    frame.pack_forget()
                    self.next_frame['setting'](
                        path = path, start_number = start_number
                    )
            except:
                pass

        tk.Button(frame, text = 'Start', command = command) \
            .grid(row = 2, column = 0, columnspan = 3)

        frame.columnconfigure(1, weight = 1)
        frame.pack(fill = tk.X)

        self.resizable(True, False)

    def switch_shot_frame(self, *, path: str, start_number: int):
        self.resizable(True, True)
        self.geometry('500x500')
        frame = tk.Frame(self, background = 'blue')
        self.attributes("-transparentcolor", 'blue')

        margin = 20
        frame.pack(padx = margin, pady = margin, expand = True, fill = tk.BOTH)

        self.config(background = 'red')

        i = start_number

        def shot(_):
            # Gap between the coordinate obtained by tkinter and the actual coordinate
            gap = (10, 60)

            x = self.winfo_x() + gap[0] + frame.winfo_x()
            y = self.winfo_y() + gap[1] + frame.winfo_y()
            x2 = x + frame.winfo_width()
            y2 = y + frame.winfo_height()

            self.withdraw()
            image = ImageGrab.grab((x, y, x2, y2))
            self.deiconify()

            nonlocal i
            file = '{}/{:0>3}.png'.format(path, i)
            i += 1

            image.save(file)
            print('TAKEN:', file)

        self.bind('<Return>', func = shot)

        def end_process():
            from tkinter.messagebox import askyesno
            yes = askyesno(message = 'Convert image to pdf?')
            if yes:
                import png2pdf
                png2pdf.convert(path)
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", end_process)


if __name__ == '__main__':
    main()
