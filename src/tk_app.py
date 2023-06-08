import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import numpy as np
import compression as cf
from zoom import MainWindow


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Jpg Comp')
        self.resizable(False, False)
        self.geometry('450x300')

        # select bmp file and show path
        self.open_file_button = ttk.Button(
            self,
            text='Select a .bmp file',
            command=self.select_file
        )
        self.open_file_button.pack(expand=True)
        self.file_path_label = tk.Label(text='Please choose a file')
        self.file_path_label.pack(padx=2, pady=10)

        # Set F parameter
        self.f_label = tk.Label(self, text="Enter chunk size", font=('Calibri 10'))
        self.f_label.pack()
        self.f = tk.IntVar()
        self.f.set(8)
        self.f_input = tk.Entry(self, width=10, textvariable=self.f)
        self.f_input.pack(pady=5)

        # set d parameter
        self.d_label = tk.Label(self, text="Enter frequency threshold", font=('Calibri 10'))
        self.d_label.pack()
        self.d = tk.IntVar()
        self.d.set(14)
        self.d_input = tk.Entry(self, width=10, textvariable=self.d)
        self.d_input.pack(pady=5)

        # compression algorithm toggle
        self.alg = 'dct'
        self.var_alg = tk.StringVar()
        self.dct_radio = ttk.Radiobutton(self, text='Use dct', variable=self.var_alg, value='dct', command=self.comp_alg_switch)
        self.fft_radio = ttk.Radiobutton(self, text='Use fft', variable=self.var_alg, value='fft', command=self.comp_alg_switch)
        self.dct_radio.pack()
        self.fft_radio.pack()

        # start compression
        self.start = ttk.Button(self, text="Start", command=self.exec)
        self.start.pack(pady=10)

    def select_file(self):
        filetypes = (
            ('bmp files', '*.bmp'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        self.file_path_label['text'] = filename

    def comp_alg_switch(self):
        self.alg = self.var_alg.get()
        if self.alg == 'fft':
            tk.messagebox.showinfo(
                'Info', f'fft mode is only for testing purpose, click \'OK\' to continue'
            )

    def exec(self):
        start = time.time()

        # parse parameters
        try:
            self.f = int(self.f_input.get())
            self.d = int(self.d_input.get())
        except:
            tk.messagebox. \
                showerror('Python Error', 'Error: Insert two positive integer')
        if self.f <= 0 or self.d < 0:
            tk.messagebox. \
                showerror('Python Error', 'Error: Chunk size and threshold must be positive')
            return
        if self.d > 2 * self.f - 2:
            tk.messagebox. \
                showerror('Python Error', 'Error: Frequency treshold too high')
            return
        try:
            filename = self.file_path_label['text']
            image = Image.open(filename)

        except:
            tk.messagebox. \
                showerror('Python Error', f'No such file {filename}')
            return

        # create array of pixels from image
        image = image.convert('L')
        pixels = np.asarray(image)

        #check if block size is too big
        if pixels.shape[0] < self.f or pixels.shape[1] < self.f:
            tk.messagebox. \
                showerror('Python Error', 'Error: Chunk size is too high')
            return

        comp_matrix = cf.compress(pixels, self.f, self.d, self.alg)
        elapsed = round(time.time() - start, 2)

        tk.messagebox.showinfo(
            'Job Completed', f'Image saved ({self.alg} compression) in {elapsed}s'
        )

        # save results
        comp_pic = Image.fromarray(comp_matrix)
        comp_pic = comp_pic.convert("L")
        save_path_file = f'{filename[:-3]}jpg'
        comp_pic.save(save_path_file)

        # show results
        jpg_w = tk.Toplevel()
        width = jpg_w.winfo_screenwidth()
        height = jpg_w.winfo_screenheight()
        jpg_w.geometry(f'{int(width / 2)}x{int(height)}+0+0')

        MainWindow(jpg_w, save_path_file, 'Jpeg')

        bmp_w = tk.Toplevel()
        bmp_w.geometry(f'{int(width / 2)}x{int(height)}+{int(width / 2)+1}+0')
        MainWindow(bmp_w, filename, 'Bitmap')




