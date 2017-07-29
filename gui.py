from Tkinter import *
from PIL import Image, ImageTk, ImageDraw
import glob

global index, classifications

import pickle
import collections
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('ImagesDirectory',help='Images Directory')
args = parser.parse_args()

def check_args():
	if args.ImagesDirectory[-1]!='/':
		args.ImagesDirectory += '/'
	if not os.path.isdir(args.ImagesDirectory):
		# Argparse uses the ArgumentTypeError to give a rejection message like:
		# error: argument input: x does not exist
		print "{} does not exist".format(args.ImagesDirectory)
		exit(0)
	else: 
		print "Images Folder found.".format(args.ImagesDirectory)
		print "Loading."

def load_image(path):
    image = Image.open(path)
    draw = ImageDraw.Draw(image)
    draw.rectangle([(127, 127), (383, 383)], outline=(255))
    pi = ImageTk.PhotoImage(image)
    return pi

def next_button(event):
    global index, classifications
    if v.get()!=0:
        classifications[images_list[index]] = v.get()

        if index < (len(images_list)-1):
            index+=1
            imgName = images_list[index][len(args.ImagesDirectory):]
            nameLabel.config(text='# '+str(index+1)+'/'+str(len(images_list))+': '+imgName)
            photo = load_image(images_list[index])
            img_label.configure(image=photo)
            img_label.image = photo
            img_label.grid(row=0)
        else:
            nameLabel.config(text="This is the last image.")
    else:
        nameLabel.config(text="Please choose a classification")


def previous_button(event):
    global index
    if index>0:
        index-=1
        imgName = images_list[index][len(args.ImagesDirectory):]
        nameLabel.config(text=imgName)
        photo = load_image(images_list[index])
        img_label.configure(image=photo)
        img_label.image = photo
        img_label.grid(row=0)


def keypad_1(event):
    class1.select()


def keypad_2(event):
    class2.select()


def keypad_3(event):
    class3.select()

def keypad_5(event):
    class4.select()


index = 0

check_args()

if os.path.exists('Classifications.p'):
    with open('Classifications.p', 'rb') as f:
        classifications = pickle.load(f)
else:
    classifications = collections.OrderedDict()

index = len(classifications.keys())
print index

images_directory = args.ImagesDirectory	
images_list = glob.glob(images_directory+'*.png')
images_list.sort()

root = Tk() #blank window
v = IntVar()
img_label = Label(root)
photo  = load_image(images_list[index])
img_label.configure(image=photo)
img_label.image=photo
img_label.grid(row=0, column=0, columnspan=2)


img_name = images_list[index][len(args.ImagesDirectory):]
nameLabel = Label(root, text='# '+str(index+1)+'/'+str(len(images_list))+': '+img_name)

nextButton= Button(root, text="Save+Next", fg="white", bg="black")

root.bind('<KP_Enter>',next_button)
root.bind('<Left>',previous_button)

root.bind('<KP_1>',keypad_1)
root.bind('<KP_2>',keypad_2)
root.bind('<KP_3>',keypad_3)
root.bind('<KP_5>', keypad_5)

root.bind('<KP_4>',previous_button)
root.bind('<KP_6>',next_button)

prevButton= Button(root, text="Previous", fg="white", bg="black")
prevButton.bind('<Button-1>', previous_button)
nextButton.bind('<Button-1>', next_button)
class1 = Radiobutton(root, text="Coconut farm", variable=v, value=1)
class2 = Radiobutton(root, text="Partly coconut farm", variable=v, value=2)
class3 = Radiobutton(root, text="Not a coconut farm", variable=v, value=3)
class4 = Radiobutton(root, text="Unsure", variable=v, value=4)

nameLabel.grid(row=1, column=0, columnspan=2)
class1.grid(row=2, column=0,columnspan=2, sticky=W)
class2.grid(row=3, column=0,columnspan=2,sticky=W)
class3.grid(row=4, column=0, columnspan=2,sticky=W)
class4.grid(row=5, column=0, columnspan=2,sticky=W)
prevButton.grid(row=6, column=0)
nextButton.grid(row=6, column=1)

root.mainloop()

with open('Classifications.p', 'wb') as f:
    pickle.dump(classifications, f)

