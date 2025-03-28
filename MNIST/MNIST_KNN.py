# -*- coding: utf-8 -*-
"""K-NN_MINIST.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/118zB69Md1PXdYpJpZPR5o_VSrck9xuXP
"""

import sklearn.preprocessing as skp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import seaborn as sns


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer # For Normalization
from sklearn.preprocessing import StandardScaler # For Standardization
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA

mnist = tf.keras.datasets.mnist
(X_train, y_train), (X_test, y_test) = mnist.load_data()

print("X_train data: ", X_train.shape)
print("X_test data: ", X_test.shape)

print("y_train data: ", y_train.shape)
print("y_test data: ", y_test.shape)

X_full = tf.concat([X_train, X_test], axis=0)
y_full = tf.concat([y_train, y_test], axis=0)

subset = 10000
X_subset = X_full[:subset].numpy() # convert datas to numpy arrays
y_subset = y_full[:subset].numpy()

# Split train - test sets to 60% - 40%
X_train, X_test, y_train, y_test = train_test_split(X_subset, y_subset, test_size=0.4, random_state=0)

X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.5, random_state=0)

X_test = X_test / 255.0
X_train = X_train / 255.0
X_val = X_val / 255.0

X_train = X_train.reshape(X_train.shape[0], -1)
X_test = X_test.reshape(X_test.shape[0], -1)
X_val = X_val.reshape(X_val.shape[0], -1)

scaler = skp.StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
X_val = scaler.transform(X_val)

# pca for dimensionality reduction
pca_cifar = PCA(n_components=0.95)
X_train = pca_cifar.fit_transform(X_train)
X_val = pca_cifar.transform(X_val)
X_test = pca_cifar.transform(X_test)

print("X_train.shape: {}\ny_train.shape: {}\nX_test.shape: {}\ny_test.shape: {}\nX_val.shape: {}\ny_val.shape: {}".format(X_train.shape, y_train.shape,
                                                                                                                          X_test.shape, y_test.shape,
                                                                                                                          X_val.shape, y_val.shape))

accuracies = []
best_accuracy = 0
best_k = 0
yi = []

for i in range (1, 100):

  knn_model = KNeighborsClassifier(n_neighbors=i)
  knn_model.fit(X_train, y_train)
  knn_pred = knn_model.predict(X_test)
  acc = metrics.accuracy_score(y_test, knn_pred)
  accuracies.append(acc)
  yi.append(i)

  if acc > best_accuracy:
    best_accuracy = acc
    best_k = i

print(f"Best accuracy: {best_accuracy} with n_neighbors = {best_k}")

plt.plot( yi, accuracies)
plt.ylabel('Accuracy')
plt.xlabel('Neightbors')
plt.grid(True)
plt.show()

knn_model = KNeighborsClassifier()
param_grid1 = {
    'n_neighbors': range(1, 10),
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan']
}

grid_search = GridSearchCV(knn_model, param_grid1, cv=10, n_jobs=-1)

grid_search.fit(X_train, y_train)


best_knn_model = grid_search.best_estimator_
print("Best Hyperparameters:", best_knn_model)

# Validation set Accuracy
y_val_pred = best_knn_model.predict(X_val)
val_accuracy = accuracy_score(y_val, y_val_pred)
print("Validation Set Accuracy:", val_accuracy)

# Test set Accuracy
y_test_pred = best_knn_model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_test_pred)
print("Test Set Accuracy:", test_accuracy)

from sklearn.metrics import confusion_matrix, classification_report

cm = confusion_matrix(y_test, y_test_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=[str(i) for i in range(10)],
            yticklabels=[str(i) for i in range(10)])

print("Classification Report:\n", classification_report(y_test, y_test_pred))

knn_pred = best_knn_model.predict(X_test)
knn_results = knn_pred[:30]
yTest_results = y_test[:30]

# DataFrame with predicted and actual values
results_df = pd.DataFrame({
    'Prediction': knn_results,
    'Actual Value': yTest_results
})

# print the dataframe
print(results_df)

# Create lists for correct and incorrect predictions
correct_predictions = []
incorrect_predictions = []

for i in range(len(knn_results)):
    if knn_results[i] == yTest_results[i]:
        correct_predictions.append(i)
    else:
        incorrect_predictions.append(i)

print("Correct Predictions:", correct_predictions)
print("Incorrect Predictions:", incorrect_predictions)

"""KPCA + LDA"""

from sklearn.decomposition import KernelPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA


kernels = ['linear', 'poly', 'rbf']

results = {}

for kernel in kernels:

    # kpca
    kpca = KernelPCA(kernel=kernel)
    X_train_kpca = kpca.fit_transform(X_train)

    # cumulative explained variance
    eigenvalues = kpca.eigenvalues_
    explained_variance_ratio = np.cumsum(eigenvalues) / np.sum(eigenvalues)

    # number of compnents that explain the 95% of variance
    n_components_95 = np.argmax(explained_variance_ratio >= 0.95) +1

    kpca = KernelPCA(n_components_95, kernel=kernel)
    X_train_kpca = kpca.fit_transform(X_train)
    X_test_kpca = kpca.transform(X_test)

    lda = LDA(n_components=9)
    X_train_lda = lda.fit_transform(X_train_kpca, y_train)
    X_test_lda = lda.transform(X_test_kpca)


    knn = KNeighborsClassifier()


    param_grid = {
        'n_neighbors': range(1, 21),
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan']
    }


    grid_search = GridSearchCV(knn, param_grid, cv=5, n_jobs=-1)
    grid_search.fit(X_train_lda, y_train)


    results[kernel] = {
        'Best n_components': n_components_95,
        'Best Parameters for KNN': grid_search.best_params_,
        'Best Score for KNN': grid_search.best_score_
       }

results_df = pd.DataFrame(results)
results_df

"""Model with the best cross validation score (RBF KERNEL PCA)"""

# kpca
kpca = KernelPCA(kernel='rbf')
X_train_kpca = kpca.fit(X_train)

# cumulative explained variance
eigenvalues = kpca.eigenvalues_
explained_variance_ratio = np.cumsum(eigenvalues) / np.sum(eigenvalues)

# number of compnents that explain the 95% of variance
n_components_95 = np.argmax(explained_variance_ratio >= 0.95) +1

kpca = KernelPCA(n_components_95, kernel='rbf')
X_train_kpca = kpca.fit_transform(X_train)
X_test_kpca = kpca.transform(X_test)

lda = LDA(n_components=9)
X_train_lda = lda.fit_transform(X_train_kpca, y_train)
X_test_lda = lda.transform(X_test_kpca)

knn = KNeighborsClassifier(metric='euclidean', n_neighbors=10, weights='distance')
knn.fit(X_train_lda, y_train)

y_pred = knn.predict(X_test_lda)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

"""Confusion Matrix"""

# Confusion Matrix (Heatmap)
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=[str(i) for i in range(10)],
            yticklabels=[str(i) for i in range(10)])
plt.title('Confusion Matrix RBF Kernel PCA')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""Classification Report"""

print("Classification Report:\n", classification_report(y_test, y_pred))

"""KNN (POLY KPCA + LDA)"""

# kpca
kpca = KernelPCA(kernel='poly')
X_train_kpca = kpca.fit(X_train)

# cumulative explained variance
eigenvalues = kpca.eigenvalues_
explained_variance_ratio = np.cumsum(eigenvalues) / np.sum(eigenvalues)

# number of compnents that explain the 95% of variance
n_components_95 = np.argmax(explained_variance_ratio >= 0.95) +1

kpca = KernelPCA(n_components_95, kernel='poly', degree=5, coef0=1)
X_train_kpca = kpca.fit_transform(X_train)
X_test_kpca = kpca.transform(X_test)

lda = LDA(n_components=9)
X_train_lda = lda.fit_transform(X_train_kpca, y_train)
X_test_lda = lda.transform(X_test_kpca)

knn = KNeighborsClassifier(metric='euclidean', n_neighbors=9, weights='distance')
knn.fit(X_train_lda, y_train)

y_pred = knn.predict(X_test_lda)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)