import os, glob, pickle, argparse, imutils
import numpy as np
from PIL import Image
import common

weights = glob.glob('output/weights*.h5')
parser = argparse.ArgumentParser()
parser.add_argument('ImagesDirectory',help='Test Images Directory')
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


def process_img(image):
    temp = np.asarray(Image.open(image).convert('RGB'))
    temp = imutils.resize(temp[0:236,:,:], height=256)[:,0:256,:]
    return temp

check_args()


classifier = common.getModel()
classifier.load_weights(weights[0])

images_directory = args.ImagesDirectory

images_list = glob.glob(images_directory+'/*.png')

answers = {}

for i in range(0, len(images_list), 32):
    print i, i+32
    img_paths = images_list[i:i+32]
    x = np.asarray([process_img(img) for img in img_paths])*(1./255)
    y = classifier.predict_classes(x, batch_size=32)
    temp_dict = dict(zip(img_paths, y))
    answers.update(temp_dict)

labels = {0:'coconut farm', 1:'partly coconut farm', 2:'not coconut farm', 3:'Unsure'}

import csv
with open('Predictions.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow('Latitude,Longitude,Label')
    for k,v in answers.items():
        lat, lon= map(float, k[:k.find('_z')].split('_')[-2:])
        writer.writerow([lat, lon, labels[v]])