import h5py
import pickle
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('ImagesDirectory',help='Path to images directory')
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

check_args()
dataset_h5_path ='Dataset.h5'

if not os.path.exists(dataset_h5_path):
    dataset_h5 = h5py.File(dataset_h5_path, 'a')
    dataset_h5.create_dataset('data', shape=(1731, 256,256,3),
                              maxshape=(None, 256,256,3),
                              compression='gzip', compression_opts=6)
    dataset_h5.create_dataset('labels', shape=(1731, 3),
                              maxshape=(None,3),
                              compression='gzip', compression_opts=6)
    print ('Dataset was created')
else:
    print ('Dataset exists')
    dataset_h5 = h5py.File(dataset_h5_path, 'a')

images_directory_path = args.ImagesDirectory
pickled_data = 'Classifications.p'


with open(pickled_data, 'rb') as f:
    datasource = pickle.load(f)

cleaned_source = {k:v-1 for k, v in datasource.items() if 1 <= v <= 3}
from sklearn.preprocessing import LabelBinarizer
enc = LabelBinarizer()
enc.fit(cleaned_source.values())
all_labels = enc.transform(cleaned_source.values())


from PIL import Image
import numpy as np
import imutils


for i in range(0, len(cleaned_source.items())//16, 16):
    print i, i+16
    images_batch = np.array([np.asarray(Image.open(key).convert('RGB')) for key in cleaned_source.keys()[i:i+16]])
    dataset_h5['labels'][i:i+16,...] = all_labels[i:i+16]
    for k in range(16):
        temp2 = imutils.resize(images_batch[k,0:236,:,:], height=256)[:,0:256,:]
        images_batch[k, ...] = temp2
    dataset_h5['data'][i:i+16,...] = images_batch

