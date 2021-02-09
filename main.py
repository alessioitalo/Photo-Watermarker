from tkinter import Tk, Radiobutton, Canvas, PhotoImage, StringVar, Label, Text, Button, filedialog, messagebox, colorchooser
import os
from PIL import Image, ImageFont, ImageDraw

chosen_path = None
chosen_output = None
background = None
color = None
text = None
font = 'arial.ttf'


def choose_dir():
    global chosen_path
    chosen_path = filedialog.askdirectory()
    path_label = Label(text=chosen_path)
    path_label.grid(column=1, row=2)


def choose_font():
    global font
    font = font_var.get()


def choose_color():
    global color
    color = colorchooser.askcolor()[0]
    r = int(color[0])
    g = int(color[1])
    b = int(color[2])
    a = 80
    color = (r, g, b, a)
    color_label = Label(text=f"{color}")
    color_label.grid(column=1, row=7, sticky='nw')


def submit_text():
    global text
    text = watermark.get("1.0","end")
    chosen_text = Label(text=f"©{text}")
    chosen_text.grid(column=1, row=5, sticky='nw', pady=0)


def choose_output():
    global chosen_output
    chosen_output = filedialog.askdirectory()
    output_label = Label(text=chosen_output)
    output_label.grid(column=1, row=13, sticky='nw')


def apply_watermark():
    if chosen_path != None and color != None and chosen_output != None:
        counter = 0
        chosen_font = ImageFont.truetype(font, 200)
        for image in os.listdir(chosen_path):
            counter +=1
            global background
            background = Image.open(chosen_path + '/' + image).convert('RGBA')
            x, y = background.size
            txt = Image.new("RGBA", background.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt)
            w, h = draw.textsize(f"©{text}")
            wm_x = x-w*15
            wm_y = y-h*15
            draw.text((wm_x, wm_y), f"©{text}", font=chosen_font, fill=color)
            final = Image.alpha_composite(background, txt)
            final.save(chosen_output + f'/watermarked_photo_{counter}.png')
        messagebox.showinfo('Success!', 'Please check your output folder.')
    else:
        messagebox.showerror("Error", "Please choose an input folder, a text and an output folder.")


window = Tk()
window.title('Watermark App')
window.config(padx=20, pady=10)
canvas = Canvas(width=220, height=100)

title = PhotoImage(file='watermarker.png')
canvas.create_image(110, 45, image=title)
canvas.grid(column=1, row=0, pady=0)

choose_dir_btn = Button(text='Choose input directory', command=choose_dir)
choose_dir_btn.grid(column=1, row=1, sticky='nw')
choose_dir_label = Label(text="")
choose_dir_label.grid(column=1, row=2, sticky='nw')

watermark_label = Label(text='Enter your name')
watermark_label.grid(column=1, row=3, sticky='nw')
watermark = Text(height=1, width=25)
watermark.grid(column=1, row=4, sticky='nw')
get_text = Button(text='Submit', command=submit_text)
get_text.grid(column=1, row=4, sticky='ne')
chosen_text = Label(text="")
chosen_text.grid(column=1, row=5, sticky='nw', pady=0)
color_btn = Button(text='Choose a color', command=choose_color)
color_btn.grid(column=1, row=6, pady=5, sticky='nw')

chosen_font = Label(text='Choose a font')
chosen_font.grid(column=1, row=8, sticky='nw')

font_var = StringVar(value='arial.ttf')
arial_font = Radiobutton(window, text="Arial", value='arial.ttf', variable=font_var, command= choose_font)
arial_font.grid(column=1, row=9, sticky='nw')
calibri_font = Radiobutton(window, text="Calibri", value='Calibri Regular.ttf', variable=font_var, command=choose_font)
calibri_font.deselect()
calibri_font.grid(column=1, row=10, sticky='nw')
signature_font = Radiobutton(window, text="Baker Script", value='BakerScript.ttf', variable=font_var, command=choose_font)
signature_font.deselect()
signature_font.grid(column=1, row=11, sticky='nw')

choose_output_btn = Button(text='Choose your destination folder', command=choose_output)
choose_output_btn.grid(column=1, row=12, pady=5, sticky='nw')
output_label = Label(text="")
output_label.grid(column=1, row=13, sticky='nw')

start = Button(text='Start', command=apply_watermark)
start.grid(column=1, row=15, pady=5, sticky='nw')

window.mainloop()