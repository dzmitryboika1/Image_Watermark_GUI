import subprocess
import sys
import tkinter.filedialog as fd
from pathlib import Path
from tkinter import *
from tkinter.messagebox import showinfo
from PIL import Image, ImageDraw, ImageFont


class WatermarkInterface:

    def __init__(self):

        # window
        self.app = Tk()
        self.app.title("Image Watermark")
        self.app.resizable(False, False)
        self.app.geometry("500x400")
        self.app.config(padx=20, pady=20)

        self.input_directory = None
        self.input_image = None
        self.output_directory = None
        self.watermark_text = None
        self.extensions = [('all image format', '*.jpg'), ('all image format', '*.png'), ('all image format', '*.jpeg')]

        # canvas with logo
        self.canvas = Canvas(width=330, height=150)
        logo_img = PhotoImage(file="logo.png")
        self.canvas.create_image(165, 75, image=logo_img)
        self.canvas.grid(column=0, row=0, columnspan=2)

        # radio buttons
        self.r_var = StringVar()
        self.r_var.set('single')
        self.singe = Radiobutton(text='Watermark Single Image', variable=self.r_var, value='single')
        self.singe.grid(row=1, column=0, sticky='w', columnspan=2)
        self.multi = Radiobutton(text='Watermark Directory With Images ', variable=self.r_var, value='multi')
        self.multi.grid(row=2, column=0, sticky='w', columnspan=2)

        # buttons
        self.select_path = Button(self.app, text='Select', width=14, command=self.open)
        self.select_path.grid(column=2, row=3, sticky='w')

        self.watermark_btn = Button(text="Watermark", width=26, command=self.save)
        self.watermark_btn.grid(column=1, row=5, columnspan=3, sticky="w", pady=10, padx=10)

        # labels
        self.select_img_label = Label(text="Image/Directory:")
        self.select_img_label.grid(column=0, row=3, sticky="e")

        self.email_username_label = Label(text="Watermark Text:")
        self.email_username_label.grid(column=0, row=4, sticky="e")

        # # entries
        self.selected_path_entry = Entry(width=24)
        self.selected_path_entry.grid(column=1, row=3)

        self.watermark_text = Entry(width=43)
        self.watermark_text.grid(column=1, row=4, columnspan=2, sticky="w", padx=10, pady=10)

        self.app.mainloop()

    def open(self):
        if self.r_var.get() == 'single':
            self.input_image = fd.askopenfilename(parent=self.app, initialdir='/', filetypes=self.extensions,
                                                  title='Select Image')
            if self.input_image:
                showinfo(title='Selected Files', message=self.input_image)
                self.selected_path_entry.insert(0, self.input_image)
            else:
                showinfo(title='Selected Files', message="None")
        else:
            self.input_directory = fd.askdirectory(parent=self.app, initialdir='/',
                                                   title='Select Directory With Images')
            if self.input_directory:
                showinfo(title='Selected Directory', message=self.input_directory)
                self.selected_path_entry.insert(0, self.input_directory)
            else:
                showinfo(title='Selected Files', message="None")

    def save(self):
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        if self.watermark_text.get():
            if self.input_image:
                self.output_directory = fd.askdirectory(parent=self.app, initialdir='/', title='Save To')
                showinfo(title='Selected Directory To Save', message=self.output_directory)
                self.watermark(self.input_image)
                self.input_image = None
                self.selected_path_entry.delete(0, END)
                showinfo(title='Success', message='Watermark Completed!')
                subprocess.call([opener, self.output_directory])
            elif self.input_directory:
                self.output_directory = fd.askdirectory(parent=self.app, initialdir='/', title='Save To')
                showinfo(title='Selected Directory To Save', message=self.output_directory)
                self.multiple_watermark()
                self.input_directory = None
                self.selected_path_entry.delete(0, END)
                showinfo(title='Success', message='Watermark Completed!')
                subprocess.call([opener, self.output_directory])
            else:
                showinfo(title='Warning', message='Please, choose image or directory!')
        else:
            showinfo(title='Warning', message='Please, input watermark text!')

    def watermark(self, image_path):
        input_path = Path(image_path)
        file_name = input_path.stem

        output_path = f'{self.output_directory}/{file_name}_output.png'

        # get an image
        opened_image = Image.open(input_path).convert("RGBA")

        # make a blank image for the text, initialized to transparent text color
        txt = Image.new('RGBA', opened_image.size, (255, 255, 255, 0))
        # get a font
        font_size = int(opened_image.width / 10)
        fnt = ImageFont.truetype("Arial.ttf", font_size)
        # get a drawing context
        draw = ImageDraw.Draw(txt)
        # coordinates for where we want to image
        x, y = int(opened_image.width / 2), int(opened_image.height / 2)

        # draw text 5% alpha
        draw.text((x, y), self.watermark_text.get(), font=fnt, fill=(0, 0, 0, 40), stroke_width=10, anchor='ms')

        combined = Image.alpha_composite(opened_image, txt)
        combined.save(output_path)

    def multiple_watermark(self):
        all_files = []

        for ext in self.extensions:
            all_files.extend(Path(self.input_directory).glob(ext[1]))

        for index, item in enumerate(all_files):
            self.watermark(item)
            print(f"Completed: {index + 1}/{len(all_files)}")


def main():
    app = WatermarkInterface()


if __name__ == "__main__":
    main()
