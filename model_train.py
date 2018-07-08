from keras.preprocessing.image import ImageDataGenerator
from keras import callbacks
from sklearn.model_selection import train_test_split
from sklearn.utils import compute_class_weight
import pickle
import h5py
import numpy as np
import common
from collections import OrderedDict
import matplotlib.pyplot as plt

# hyper-parameters
epochs = 500
batch_size = 16
learning_rate_init = 0.00001
loss_function = 'categorical_crossentropy'
optimizer = 'adam'


dataset_h5 = h5py.File(common.dataset_name, 'r')
labels = {0:'coconut farm', 1:'partly coconut farm', 2:'not a coconut farm'}
with open(common.classifications_file_name, 'rb') as f:
    datasource = pickle.load(f)
cleaned_source = OrderedDict((k,v-1) for k,v in datasource.items() if 1<=v<=3)
X = cleaned_source.keys()
dataset_labels = [v for v in cleaned_source.values()]

data_indices =[i for i in range(len(cleaned_source.items()))]
train, test, _, _= train_test_split(data_indices, dataset_labels, train_size=0.75, random_state=42)
train.sort()
test.sort()
x = np.asarray(train)
dataset_labels = np.asarray(dataset_labels)
temp= dataset_labels[x]
classes = np.array(labels.keys())
class_weight_vect = compute_class_weight('balanced', classes, temp)
class_weight = {0:class_weight_vect[0], 1:class_weight_vect[1], 2:class_weight_vect[2]}
indices = {'train':train, 'test':test}
model_name = 'Coconut-Not-Coconut'
with open('output/'+model_name+'_indices.p', 'wb') as f:
    pickle.dump(indices, f, protocol=2)
model = common.getModel()
model.compile(loss=loss_function,optimizer=optimizer, metrics=['accuracy'])

#note: model doesn't converge unless we re-scale pixels to range [0,1]
train_datagen = ImageDataGenerator(fill_mode='reflect',
                                   shear_range=0.3,
                                   rotation_range=90,
                                   vertical_flip=True,
                                   horizontal_flip=True,
                                   rescale=1. / 255)

train_generator = train_datagen.flow(dataset_h5['data'][train, :,:,:], dataset_h5['labels'][train,:],
batch_size=batch_size)
test_datagen = ImageDataGenerator(rescale=1. / 255)
validation_generator = test_datagen.flow(dataset_h5['data'][test,:,:,:], dataset_h5['labels'][test,:],
batch_size=batch_size)
filepath = "output/weights"+model_name+".h5"
checkpoint = callbacks.ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
reduce_lr = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.8,patience=5, min_lr=learning_rate_init, verbose=1)
callbacks_list = [checkpoint, reduce_lr]
history = model.fit_generator(train_generator,
    steps_per_epoch=len(train) // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=len(test) // batch_size, callbacks=callbacks_list, verbose=1)


# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
