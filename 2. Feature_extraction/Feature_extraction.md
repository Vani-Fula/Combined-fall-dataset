# **2.Feature_extraction**
This folder performs the extraction of features using data from the accelerometer and gyroscope.
1. fCalculation performs the calculation of all features;
2. SFt_List lists the sensors used as well as the features to be calculated;
## 2.1 featuresExtraction
It is the file responsible for extracting the features of each subject, determines the time windows to be used (they can be changed, in this example we chose a duration of 3 seconds with 50% overlap), each data set has a individual file that can be changed as needed, changing parameters such as number of subjects, activities or attempts.
Extraction can be done for the original data and for the normalized data, depending on the need.
