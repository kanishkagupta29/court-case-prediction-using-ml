# -*- coding: utf-8 -*-
"""Courtroom Judgement Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XLNWINFVSIp_Ppw6-mbZqye1m2s-EqJz

#Importing libraries
"""

import  pandas  as  pd
import  numpy  as  np
import  matplotlib.pyplot  as  plt
import  seaborn  as  sns
import warnings
warnings.filterwarnings('ignore')

import os
os.environ['KAGGLE_USERNAME']=  "jyotiaggarwal2"
os.environ['KAGGLE_KEY']=  "7b2a1a1b5c224e6325824c621e0025c4"
!kaggle datasets download -d deepcontractor/supreme-court-judgment-prediction

!unzip supreme-court-judgment-prediction

"""#Reading dataset

"""

data=pd.read_csv('/content/justice.csv',encoding='latin',)

data.head()

data.columns

data.dtypes

"""#DATA PREPROCESSING

Managing null and duplicate values if any
"""

data.isna().sum()

print(data.duplicated().sum())

data.dropna(inplace=True)

"""#Removing unwanted columns"""

data=data.drop(columns=['first_party','second_party'])

data.isna().sum()

plt.figure(figsize=(25,10))
sns.countplot(x='decision_type', hue='disposition', data=data)
plt.xlabel("Decision type")
plt.ylabel("Count")
plt.show()

"""The above graph shows the distribution of decision type.It shows that the most of cases were in favour of majority opinion."""

plt.figure(figsize=(10,5))
sns.countplot(x='decision_type', hue='issue_area', data=data)
plt.xlabel("Decision type")
plt.ylabel("Count")
plt.show()

"""The above graph shows the distribution of decision type and the distribution of number of cases in each decision type.In the majority opinion decision type,the number of cases with each issue area are comparatively larger than that for other decision types.The number of cases of criminal procedure are the highest in different decision types especially forr majority opinion."""

plt.figure(figsize=(25,10))
sns.countplot(x='decision_type', hue='majority_vote', data=data)
plt.xlabel("Decision type")
plt.ylabel("Count")
plt.show()

"""The above graph shows the variation of the majority votes for each decision type."""

plt.figure(figsize=(25,10))
sns.countplot(x='decision_type', hue='minority_vote', data=data)
plt.xlabel("Decision type")
plt.ylabel("Count")
plt.show()

"""The above graph shows how minority votes varies in each decision type"""

plt.figure(figsize=(10,5))
sns.countplot(x='decision_type', hue='first_party_winner', data=data)
plt.xlabel("Decision type")
plt.ylabel("Count")
plt.show()

"""The above graph shows number of cases of each decision type in which either first party is winner or not.In all the decision types the first party is the winner as can be seen from the orange bar in each decision type"""

plt.figure(figsize=(20,10))
sns.countplot(x='disposition', hue='decision_type', data=data)
plt.xlabel("Disposiion")
plt.ylabel("Count")
plt.show()

"""The above graph shows the variation of each disposition with the decision type

#Splitting the data into train-test

TfidfVectorizer is a term frequency-inverse document frequency (TF-IDF) vectorization technique used in NLP.It automates the process of converting a collection of text documents into a matrix of TF-IDF features. It tokenizes the text, calculates the TF-IDF values for each term in each document, and constructs a matrix where each row represents a document and each column represents a term with its corresponding TF-IDF value.
"""

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

text_data = data['facts']

# Split the data into features (X) and target (y)
X_text = text_data.values
y = data['facts']

# Split data into training and testing sets
X_train_text, X_test_text, y_train, y_test = train_test_split(X_text, y, test_size=0.2, random_state=42)

# Text vectorization using TF-IDF
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train_text)
X_test_tfidf = vectorizer.transform(X_test_text)

# Convert the TF-IDF matrix to a dense numpy array
X_train_tfidf = X_train_tfidf.toarray()
X_test_tfidf = X_test_tfidf.toarray()

"""#Feature Engineering"""

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
y = encoder.fit_transform(data['first_party_winner'])

data['decision_type'] = encoder.fit_transform(data['decision_type'])

target=data['first_party_winner']
target.reset_index(drop=True, inplace=True)
target=encoder.fit_transform(target)
data['first_party_winner']=pd.DataFrame(target, columns=['first_party_winner'])

"""#Finding the accuracy using SVM model

SVM stands for Support Vector Machine, which is a machine learning algorithm used for both classification and regression tasks. It's particularly effective in scenarios where the data points are not linearly separable and need to be transformed into a higher-dimensional space to make them separable.
"""

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Preprocessing
X = data['facts']
y = data['first_party_winner']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Text vectorization using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # You can adjust the max_features parameter
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Train a support vector machine (SVM) classifier
clf = SVC()
clf.fit(X_train_tfidf, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test_tfidf)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

"""#Finding the accuracy of model using different models

#1. Naive Bayes
"""

from sklearn.naive_bayes import MultinomialNB
model=MultinomialNB()
model.fit(X_train_tfidf, y_train)
y_pred = model.predict(X_test_tfidf)
model.score(X_test_tfidf,y_test)

"""Evaluaion Matrices"""

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

"""#2. Decision Tree

Creating and training the model
"""

from sklearn.tree import DecisionTreeClassifier
model=DecisionTreeClassifier()
model.fit(X_train_tfidf, y_train)

"""model evaluation"""

y_pred = model.predict(X_test_tfidf)
model.score(X_test_tfidf,y_test)

"""Evaluation matrices"""

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

"""#CONCLUSION

The accuracy of this dataset is calculated using 3 models i.e. SVM, Naive Bayes and Decision Trees.The accuracy calculated using SVM and Naive Bayes is same that is 67 percent and is higher than that from Decision trees.This model has fairly good accuracy but not that high.
"""