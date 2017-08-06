![e-farmerce Platform](http://e-farmerce.com/logo.jpg)

Deep learning & satellite imagery are changing the way we look at agriculture. Our Primary goal is Make the Crops Searchable from Satellite Imagery and identify the Geo Location of the crops with Crop Based Deep learning Models.We explain the e-farmerce Platform Implementation of Deep Learning in Satellite Imagery for Coconut Crop Identification

In the area where our Deep Learning codes for coconut model has been tested, we show the Crop Health from the Multispectral Satellite Imagery which represents relative chlorophyll content, which correlates with vegetation vigor and productivity

This shows  our Implentation can be used to Identify a Specific Crop and assess productivity of crops in the same geolocation to identify site-specific issues that can be addressed by corrective management decisions.

We have Used NASA WorldWind for Data Visualisation and Interpretation

## Video Tutorial
[![Deep Learning in Agriculture Crop Identification ](https://user-images.githubusercontent.com/30501155/28919964-6422f546-786d-11e7-9267-97361f0df49c.png)](https://youtu.be/u87eDKkTmNU "Deep Learning in Agriculture Crop Identification ")

## Underlying Technology
![slide5](https://user-images.githubusercontent.com/30501155/28920256-9d9ea2a6-786e-11e7-9239-59ae8ae8ffe5.PNG)
![slide7](https://user-images.githubusercontent.com/30501155/28920279-b32886e6-786e-11e7-9ae6-3f24b12393d8.PNG)

The satellite imagery is retrieved using Google Static Maps API using Ruby and GeoJSON. The details on how to achieve this are mentioned in the ```README``` in the ```download_area``` directory.

These images are labelled using the labelling tool provided ```(gui.py)```. The tool allows a user to classify images as ```coconut farm, not coconut farm, partly coconut farm```, 

The labels and the images are then converted into a Keras friendly format, i.e., into an HDF5 file.

This HDF5 file is fed to a Convolutional Neural Network, which is a Sequential Keras model. The trained model can then be used to make predictions.

These predictions are saved to a ```.csv``` file so that they can be easily exported for visualization in other software, such as [NASA WorldWind.](
https://worldwind.arc.nasa.gov//)

## Getting Started

	git clone <this repo> 

	cd download_area/

	ruby download_area.rb 
	#to get the satellite images


If you are downloading the images for a new area, you will need to label those images. 
Labelling images will be done by using 

	python gui.py <images directory>/

The output of ```gui.py``` is a pickled python dictionary, named ```Classifications.p```.

	python create_hdf5.py <images directory>/
	#will create the HDF5 file, dataset.h5, using the images and ground truths.

	python model_train.py 
	#will train the model.

The train and validation indices of ```model_train.py``` are pickled into a dictionary in the ```output/``` folder. This folder will also contain the weights of the trained model after training is complete.

Currently, the model is configured to reduce learning rate by 0.2 if the loss plateaus for 5 epochs.
The model was trained for 250 epochs on a 3:1 train:test split, and achieved 92% accuracy on the validation set, with 80% on test set.

The train/validation/test sets for Cumbum can be visualized [here](http://bl.ocks.org/anonymous/raw/d8757753ccf9996543f2a046a5d86e8e/), or by using the ```Cumbum.json``` file.



	python model_predict.py <test images directory>/
	#will generate predictions as a .csv file.

## Deep Learning Coconut Crop Identification Result

img width="620" alt="output image 1" src="https://user-images.githubusercontent.com/30501155/29003930-5db2b35a-7add-11e7-93db-aed0abdee2de.png">


Our Deep Learning coconut model can able to predict the coconut farm in a specified area with 80% accuracy, still work in progress on the neural network architecture to achieve greater prediction accuracy with more coverage area.

To show and demonstrate the power of Deep Learning in satellite imagery we have used Google maps satellite imagery, work in progress for using other commercial satellite imagery. 



## Notes

The Neural Network was trained using [Floydhub's](http://floydhub.com) free GPU offering. On average, it took 1 hour for our models, which were roughly 10MB in size.
