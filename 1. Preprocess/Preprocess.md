# **1.Preprocess**
## 1.1 preprocess
This file preprocesses the data set, this process chooses the data of interest from each data set, labels the activities and binarizes the classes. It also performs downsampling (Dataset_Donwsampling) and unification of the accelerometer and gyroscope units. There is an individual file for preprocessing each of the data sets.

## 1.2 fall_Label
This file labels the falls for the UMA Fall and WEDA Fall sets, since these data sets do not have their csv files labeled. Labeling is done for each data set, it is also possible to do individual labeling per csv file (depending on the criteria used for labeling, some cases can be misinterpreted and individual labeling is necessary) using the individual_falls_Label file. The graphics file allows you to generate images of the csv and their scrolling ranges.

## 1.3 Normalization
In this file, the data scale is normalized by homogenizing the accelerometer and gyroscope scale to [-1;1]. This step is optional in order to see how performance can be changed by normalization.
