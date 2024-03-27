# **3. Feature_selection and classification**

## 3.1 Data separation.

The data_split code divides the data sets into training and test folders, organizing the files according to the size of the data sampling window into corresponding subfolders, and guarantees that the same activity of a subject is not simultaneously in both sets.

## 3.2 Feature_Selection,

Variable selection is performed by the ***feature_selection*** function as follows:
1. First, three different models are trained to evaluate the importance of variables:
- An Extra Trees Classifier model.
- An RFE (Recursive Feature Elimination) model with decision tree.
- A LinearSVC model with L2 penalty.

2. For each model, the 30 most important variables are identified.

3. Then, these sets of variables are intersected to find those that are common to at least two of the three models.

4. Of these common variables, up to the 28th best in terms of importance are selected.

5. Finally, a Random Forest model is trained with the selected variables, and accuracy is calculated as the number of variables increases from the first to the last selected. This allows you to visualize how the model's accuracy varies with the number of selected variables.

## 3.3 Data Classification

1. The **best_parameter** function optimizes hyperparameters for SVM and ANN models using Bayesian hyperparameter search. It prints the best parameters found based on the AUC-ROC value for both models in each dataset.

2. The **svm_model** function creates, trains, and evaluates an SVM model for classification by calculating various performance metrics, including precision, recall, F1-score, specificity, and AUC-ROC.

3. The **ann** function trains and evaluates a neural network model with adjustable hyperparameters, calculating performance metrics and displaying the normalized confusion matrix for each model.
