#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Basic imports for all datasets
import numpy as np 
import pandas as pd   # for data reading 
import matplotlib.pyplot as plt
import sklearn
import sklearn.linear_model
import sklearn.tree
import sklearn.ensemble
import sklearn.naive_bayes
import sklearn.neural_network
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import sklearn.metrics           # For accuracy_score
import sklearn.model_selection   # For GridSearchCV and RandomizedSearchCV
import scipy
import scipy.stats               # For reciprocal distribution
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)  # Ignore sklearn deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)       # Ignore sklearn deprecation warnings
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, RationalQuadratic, ExpSineSquared


# In[2]:


#Dataset 2 : Default of credit card clients

#Loading dataset
data = np.loadtxt('australian.dat',dtype = 'str', delimiter=' ')

df = pd.DataFrame({'A1':data[:, 0], 'A2':data[:, 1], 'A3':data[:, 2], 'A4':data[:, 4], 'A5':data[:, 5], 
                   'A6':data[:, 5], 'A7':data[:, 6], 'A8':data[:, 7], 'A9':data[:, 8], 'A10':data[:, 9], 
                   'A11':data[:, 10], 'A12':data[:, 11], 'A13':data[:, 12], 'A14':data[:, 13], 'Class attribute':data[:, 14] })

df.sample(5)


# In[3]:


#Splitting training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    data[:,:14], 
    df['Class attribute'] , 
    test_size=0.2, 
    random_state=0)
X_train = X_train.astype(np.float)
X_test = X_test.astype(np.float)


# In[4]:


#k-Nearest neighbours classification
knn_model = sklearn.neighbors.KNeighborsClassifier(n_jobs=-1)
param_grid = {'n_neighbors':(np.arange(2,52, 5))}

mdls = sklearn.model_selection.GridSearchCV(knn_model, param_grid, verbose=1,cv=5).fit(X_train, y_train)
print(mdls.best_estimator_)
y_pred = mdls.best_estimator_.predict(X_test)
sklearn.metrics.accuracy_score(y_test, y_pred)


# In[5]:


#Logistic regression (for classification)
#Fit_intercept is set to True because we don't have bias
# logistic_model = sklearn.linear_model.LogisticRegression(fit_intercept=True)
logistic_model = sklearn.linear_model.LogisticRegression(n_jobs=-1)
param_grid = { "fit_intercept":[True], "solver":['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'], 
             "max_iter":np.arange(100,400, 100)}


mdls = sklearn.model_selection.GridSearchCV(logistic_model, param_grid, verbose=1,cv=5).fit(X_train, y_train)
print(mdls.best_estimator_)

y_pred = mdls.best_estimator_.predict(X_test)
sklearn.metrics.accuracy_score(y_test, y_pred)


# In[6]:


#Decision tree classification
DTC_model = sklearn.tree.DecisionTreeClassifier(random_state=0)
Max_features = ['auto', 'sqrt', 'log2']
Max_depths = np.arange(1,34,2)
Min_samples_splits = np.linspace(0.1, 1.0, 10, endpoint=True)
Min_samples_leafs = np.linspace(0.01, 0.05, 5, endpoint=True)
param_grid = {'max_features': Max_features, 'max_depth': Max_depths,  'min_samples_split': Min_samples_splits, 'min_samples_leaf': Min_samples_leafs}

mdls = sklearn.model_selection.GridSearchCV(DTC_model, param_grid, verbose=1,cv=5).fit(X_train, y_train)
print(mdls.best_estimator_)

y_pred = mdls.best_estimator_.predict(X_test)
sklearn.metrics.accuracy_score(y_test, y_pred)


# In[7]:


#Random forest classification
RFC_model = sklearn.ensemble.RandomForestClassifier(random_state=0)
Estimators = np.arange(100,105,1)
Max_features = ['auto', 'sqrt', 'log2']
param_grid = {'n_estimators': Estimators,'max_features': Max_features, }

mdls = sklearn.model_selection.GridSearchCV(RFC_model, param_grid, verbose=1,cv=5).fit(X_train, y_train)
print(mdls.best_estimator_)

y_pred = mdls.best_estimator_.predict(X_test)
sklearn.metrics.accuracy_score(y_test, y_pred)


# In[8]:


#AdaBoost classification
ABC_model = sklearn.ensemble.AdaBoostClassifier(random_state=0)
Estimators = np.arange(50,100,10)
Learning_rates = [0.01,0.05,0.1,0.3,1]
algorithm = ['SAMME', 'SAMME.R']
param_grid = {'n_estimators': Estimators, 'learning_rate': Learning_rates, 'algorithm': algorithm}

mdls = sklearn.model_selection.GridSearchCV(ABC_model, param_grid, verbose=1,cv=5).fit(X_train, y_train)
print(mdls.best_estimator_)

y_pred = mdls.best_estimator_.predict(X_test)
sklearn.metrics.accuracy_score(y_test, y_pred)


# In[9]:


#Gaussian naive Bayes classification

zero_prob = y_train[y_train == 0].shape[0]/y_train.shape[0]
one_prob = 1 - zero_prob
prob = np.array([zero_prob,one_prob])
GNB_model = sklearn.naive_bayes.GaussianNB(priors = prob)
GNB_model.fit(X_train, y_train)
# mdls = sklearn.model_selection.GridSearchCV(GNB_model, param_grid, verbose=1,cv=5).fit(X_train, y_train)
# print(mdls.best_estimator_)

y_pred = GNB_model.predict(X_test)
sklearn.metrics.accuracy_score(y_test, y_pred)


# In[10]:


#Neural network classification
NNC_model = sklearn.neural_network.MLPClassifier()
# batch_size = [10, 20, 40, 60, 80, 100]
batch_size = [100]
# epochs = [10, 50, 100]
epochs = [10]
learn_rate = [0.001, 0.01, 0.1]
momentum = [0.0, 0.2, 0.4, 0.6, 0.8]
neurons = [1, 5, 10, 15, 20, 25, 30] 
activation = ['identity', 'logistic', 'tanh', 'relu']
alpha = [0.0001,0.002]
param_grid = {'batch_size':batch_size,  'momentum':momentum, 
              'activation' : activation, }

mdls = sklearn.model_selection.GridSearchCV(NNC_model, param_grid, verbose=1,cv=5).fit(X_train, y_train)
print(mdls.best_estimator_)

y_pred = mdls.best_estimator_.predict(X_test)
sklearn.metrics.accuracy_score(y_test, y_pred)


# In[11]:


#SVM classifier
svm_model = sklearn.svm.SVC()
Kernels = ['linear', 'poly', 'rbf', 'sigmoid']
Epsilons = [0.1,0.2,0.5,0.3]
Cs = [0.001, 0.01, 0.1, 1, 10]
Gammas = [0.001, 0.01, 0.1, 1]
param_grid = {'C': Cs, 'gamma' : Gammas}

mdls = sklearn.model_selection.GridSearchCV(svm_model, param_grid, verbose=1,cv=3).fit(X_train, y_train)
print(mdls.best_estimator_)

y_pred = mdls.best_estimator_.predict(X_test)
sklearn.metrics.accuracy_score(y_test, y_pred)


# In[ ]:


print('According to our methods, we find that the most of the models (Adaboost, Logisitic regression and Random forest) have the same test accuaracy (roughly 88%). Hence, we suggest going for Logisitic regression because it provides the same level of accuracy with a much simpler model which so there\'s little chance to overfit')

