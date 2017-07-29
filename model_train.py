from keras.preprocessing.image import ImageDataGenerator
from keras import callbacks
from sklearn.model_selection import train_test_split
from sklearn.utils import compute_class_weight
import pickle
import h5py
import numpy as np
import model_define

file_path = 'Dataset.h5'
dataset_h5 = h5py.File(file_path, 'r')

print ('H5 Dataset retrieved')

labels = {0:'coconut farm', 1:'partly coconut farm', 2:'not a coconut farm'}

with open('Classifications.p', 'rb') as f:
    datasource = pickle.load(f)

print ('Paths and labels unpickled.')
from collections import OrderedDict
cleaned_source = OrderedDict((k,v-1) for k,v in datasource.items() if 1<=v<=3)

X = cleaned_source.keys()
dataset_labels = [v for v in cleaned_source.values()]
# dimensions of our images.
img_width, img_height = 256, 256

epochs = 500
batch_size = 16

data_indices =[i for i in range(len(cleaned_source.items()))]

train, test, _, _= train_test_split(data_indices, dataset_labels, train_size=0.75, random_state=42)
train.sort()
test.sort()

x = np.asarray(train)
dataset_labels = np.asarray(dataset_labels)
temp= dataset_labels[x]
classes = np.array([0,1,2])
class_weight_vect = compute_class_weight('balanced', classes, temp)
class_weight = {0:class_weight_vect[0], 1:class_weight_vect[1], 2:class_weight_vect[2]}

indices = {'train':train, 'test':test}

model_name = '15_July_Model_v3'

with open('output/'+model_name+'_indices.p', 'wb') as f:
    pickle.dump(indices, f, protocol=2)

print ("Building model - ", model_name)
# create model
model = model_define.create_model_v3()
model.compile(loss='categorical_crossentropy',optimizer='adam', metrics=['accuracy'])
print ("Model built.")

#create augmented data for training
train_datagen = ImageDataGenerator(fill_mode='reflect',
                                   shear_range=0.3,
                                   rotation_range=90,
                                   vertical_flip=True,
                                   horizontal_flip=True,
                                   rescale=1. / 255)

train_generator = train_datagen.flow(dataset_h5['data'][train, :,:,:], dataset_h5['labels'][train,:],
batch_size=batch_size)

#create validation data
test_datagen = ImageDataGenerator(rescale=1. / 255)

validation_generator = test_datagen.flow(dataset_h5['data'][test,:,:,:], dataset_h5['labels'][test,:],
batch_size=batch_size)

print ("Training and Evaluating model")

filepath = "output/weights"+model_name+".h5"

checkpoint = callbacks.ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
#early_stop = callbacks.EarlyStopping(monitor='val_loss', min_delta=0.00001, patience=4, mode='min', verbose=1)
reduce_lr = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.8,patience=5, min_lr=0.00001, verbose=1)

callbacks_list = [checkpoint, reduce_lr]

model.fit_generator(train_generator,
    steps_per_epoch=len(train) // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=len(test) // batch_size, callbacks=callbacks_list, verbose=1)

print ('Model: '+model_name +' saved.')
