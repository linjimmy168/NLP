from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import json
import numpy as np

# Text Data Features
def generateTextFromDataSeries(dataFrameData):
    return ["".join(val).lower() for val in dataFrameData]

tfidf = TfidfVectorizer(binary=True)
def tfidf_features(txt, flag):
    if flag == "train":
    	x = tfidf.fit_transform(txt)
    else:
	    x = tfidf.transform(txt)
    x = x.astype('float32')
    return x 

# Dataset Preparation
print ("Read Dataset ... ")
df = pd.read_excel('D:/NLPExcel/total.xlsx',sheet_name='sheet1')
df = df[df.iloc[:,1] != -1]

df = df[:25000]

train,test = train_test_split(df, test_size = 0.2)
print ("Prepare text data of Train and Test ... ")
train_text,test_text = generateTextFromDataSeries(train.iloc[:,0]), generateTextFromDataSeries(test.iloc[:,0])
target = [doc for doc in train.iloc[:,1]]
# Feature Engineering 
print ("TF-IDF on text data ... ")
X = tfidf_features(train_text, flag="train")
X_test = tfidf_features(test_text, flag="test")

# Label Encoding - Target 
print ("Label Encode the Target Variable ... ")
lb = LabelEncoder()
y = lb.fit_transform(target)
# Model Training 
print ("Train the model ... ")
# classifier = SVC(C=100, # penalty parameter
# 	 			 kernel='rbf', # kernel type, rbf working fine here
# 	 			 degree=3, # default value
# 	 			 gamma=1, # kernel coefficient
# 	 			 coef0=1, # change to 1 from default value of 0.0
# 	 			 shrinking=True, # using shrinking heuristics
# 	 			 tol=0.001, # stopping criterion tolerance 
# 	      		 probability=False, # no need to enable probability estimates
# 	      		 cache_size=200, # 200 MB cache size
# 	      		 class_weight=None, # all classes are treated equally 
# 	      		 verbose=False, # print the logs 
# 	      		 max_iter=-1, # no limit, let it run
#           		 decision_function_shape=None, # will use one vs rest explicitly 
#           		 random_state=None)

# model = OneVsRestClassifier(classifier, n_jobs=4)

model = GaussianNB()
model.partial_fit(X.toarray(), y, np.unique(y))

model.fit(X.toarray(), y)

# Predictions 
print ("Predict on test data ... ")
y_test = model.predict(X_test.toarray())
y_pred = lb.inverse_transform(y_test)

# Submission
print ("Generate Submission File ... ")
sentence = [doc.encode('utf-8') for doc in test.iloc[:,0]]
sub = pd.DataFrame({'sentence': sentence, 'classify': y_pred}, columns=['sentence', 'classify'])
sub.to_csv('svm_output.csv', index=False)


#Score
y_true = test.iloc[:,1]
print("Accuracy Score")
print(accuracy_score(y_true, y_pred))