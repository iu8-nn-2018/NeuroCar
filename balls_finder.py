from tkinter import *
from PIL import Image, ImageTk
import os
import sys
arg = sys.argv
from math import floor
path = arg[1]

ims_path = os.listdir(path)
samp = os.path.join(path, 'samples')
if not os.path.exists(samp):
    os.mkdir(samp)
else:
    ims_path.remove('samples')
nothing = os.path.join(path, 'nothing')
if not os.path.exists(nothing):
    os.mkdir(nothing)
else:
    ims_path.remove('nothing')

class Searching_Lines(Tk):
    dots = []
    img_number = 0
    x = []
    y = []
    R = []
    
    def __init__(self, filename):
        Tk.__init__(self)
        self.width = int(self.winfo_screenwidth() * 0.8)
        self.height = int(self.winfo_screenheight() * 0.8)
        self.ratio = float(self.width) / self.height
        self.title('Find tennis ball')
        
        self.photos = [os.path.join(path, i) for i in ims_path]
        if os.path.exists(filename):
            self.photos.remove(filename)
            ims_path.remove(arg[2])
            self.result_file = open(filename, 'a+')
        else:
            self.result_file = open(filename, 'w+')
        self.canvas = Canvas(self, width=self.width, height=self.height, bg="white")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<Escape>", self.back)
        self.bind("<Tab>", self.next)
        if len(self.photos) == 0:
            self.result_file.close()
            self.destroy()
        else:
            self.draw_image()
    def find_name(self):
        for i in self.result_file:
            if i.startswith(self.photos[self.img_number]):
                self.img_number += 1
                if self.img_number == len(self.photos):
                    pass
                self.find_name()

    def draw_image(self):
        self.dots.clear()
        self.R.clear()
        self.x.clear()
        self.y.clear()
        self.find_name()
        self.image = Image.open(self.photos[self.img_number])
        w,h = self.image.size
        ratio = float(w)/h
        
        if ratio > self.ratio:
            self.coef = float(w) / self.width
            size = (self.width, int(floor(h / self.coef)))

        if ratio < self.ratio:
            self.coef = float(h) / self.height
            size = (int(floor(w / self.coef)), self.height)

        if ratio == self.ratio:
            self.coef = float(im_width / self.width)
            size = (self.width, self.height)
        
        self.resized = self.image.resize(size, Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(self.resized)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        
    '''
    def check(self, event):
        for i in range(len(self.dots) // 3):
            x12 = self.dots[i * 3][0] - self.dots[i * 3 + 1][0]
            x23 = self.dots[i * 3 + 1][0] - self.dots[i * 3 +2][0]
            x31 = self.dots[i * 3 + 2][0] - self.dots[i * 3][0]
            y12 = self.dots[i * 3][1] - self.dots[i * 3 + 1][1]
            y23 = self.dots[i * 3 +1][1] - self.dots[i * 3 + 2][1]
            y31 = self.dots[i * 3 + 2][1] - self.dots[i * 3][1]
            z1 = self.dots[i * 3][0] ** 2 + self.dots[i * 3][1] ** 2
            z2 = self.dots[i * 3 + 1][0] ** 2 + self.dots[i * 3 + 1][1] ** 2
            z3 = self.dots[i * 3 + 2][0] ** 2 + self.dots[i * 3 + 2][1] ** 2
            zx = y12 * z3 + y23 * z1 + y31 * z2
            zy = x12 * z3 + x23 * z1 + x31 * z2
            z = x12 * y31 - y12 * x31
            xx = (-1) * zx / (2 * z)
            self.x.append(xx)
            yy = zy / (2 * z)
            self.y.append(yy)
            a = (x12 ** 2 + y12 **2) ** 0.5
            b = (x23 ** 2 + y23 **2) ** 0.5
            c = (x31 ** 2 + y31 **2) ** 0.5
            p = (a + b + c) / 2
            S = (p * (p - a) * (p - b) * (p - c)) ** 0.5
            r = a * b * c / (4 * S)
            self.R.append(r)
            self.canvas.create_oval(xx - r, yy - r,
                                   xx + r, yy + r,
                                    fill='Red', outline="Red")
    '''
    def back(self, event):
        self.canvas.delete()
        self.dots.clear()
        self.R.clear()
        self.x.clear()
        self.y.clear()
        self.draw_image()
        
    def draw_circle(self, arr):
        x12 = arr[0][0] - arr[1][0]
        x23 = arr[1][0] - arr[2][0]
        x31 = arr[2][0] - arr[0][0]
        y12 = arr[0][1] - arr[1][1]
        y23 = arr[1][1] - arr[2][1]
        y31 = arr[2][1] - arr[0][1]
        z1 = arr[0][0] ** 2 + arr[0][1] ** 2
        z2 = arr[1][0] ** 2 + arr[1][1] ** 2
        z3 = arr[2][0] ** 2 + arr[2][1] ** 2
        zx = y12 * z3 + y23 * z1 + y31 * z2
        zy = x12 * z3 + x23 * z1 + x31 * z2
        z = x12 * y31 - y12 * x31
        xx = (-1) * zx / (2 * z)
        self.x.append(xx)
        yy = zy / (2 * z)
        self.y.append(yy)
        a = (x12 ** 2 + y12 **2) ** 0.5
        b = (x23 ** 2 + y23 **2) ** 0.5
        c = (x31 ** 2 + y31 **2) ** 0.5
        p = (a + b + c) / 2
        S = (p * (p - a) * (p - b) * (p - c)) ** 0.5
        r = a * b * c / (4 * S)
        self.R.append(r)
        self.canvas.create_oval(xx - r, yy - r,
                                   xx + r, yy + r,
                                    fill='Red', outline="Red")
    def on_button_press(self, event):
            self.dots.append([event.x, event.y])
            if len(self.dots) % 3 == 0:
                self.draw_circle(self.dots[-3:])
        
            
    def f(self, x):
        return self.coef*x
    
    def next(self, event):
        cur = os.path.join(path, ims_path[self.img_number])
        if len(self.dots) % 3 != 0:
            win = Toplevel(self, relief=SUNKEN, bd=10, bg="lightblue")
            win.title("Error. Put more dots or do it again")
            win.minsize(width=400, height=200)
        elif len(self.dots) != 0:
            self.result_file.write(ims_path[self.img_number] + ' ')
            self.result_file.write(str(len(self.R)) + ' ')
            for i in range(len(self.R)):
                self.result_file.write(str(self.f(self.x[i])) + ' ' + str(self.f(self.y[i]))
                                       + ' ' + str(self.f(self.R[i])) + '\n')
            dest = os.path.join(samp, ims_path[self.img_number])
            os.rename(cur, dest)
            self.img_number += 1
        else:
            dest = os.path.join(nothing, ims_path[self.img_number])
            os.rename(cur, dest)
            self.img_number += 1
        if self.img_number >= len(self.photos):
            self.result_file.close()
            self.destroy()
        else:
            self.draw_image()

        
if __name__ == '__main__':
    app = Searching_Lines(os.path.join(arg[1], arg[2]))
    app.mainloop()

