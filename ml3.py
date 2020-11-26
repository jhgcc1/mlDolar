from sklearn.model_selection import GridSearchCV,RandomizedSearchCV
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, MinMaxScaler, QuantileTransformer, MaxAbsScaler, RobustScaler, PowerTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator
from sklearn.ensemble import BaggingRegressor
def mlModel2(df):
    class MyClassifier(BaseEstimator):

        def __init__(self, classifier_type: str = 'MinMaxScaler'):
            """
            A Custome BaseEstimator that can switch between classifiers.
            :param classifier_type: string - The switch for different classifiers
            """
            self.classifier_type = classifier_type


        def fit(self, X,y=None):
            if self.classifier_type == 'StandardScaler':
                self.classifier_ = StandardScaler()
            elif self.classifier_type == 'MinMaxScaler':
                self.classifier_ = MinMaxScaler()
            else:
                raise ValueError('Unkown classifier type.')

            self.classifier_.fit(X)
            return self

        def transform(self,X,y=None):
            return self.classifier_.transform(X)
            

    l1_space = np.linspace(0, 1, 5)
    alpha=np.logspace(-1,1,5)
    param_grid = {"clf__base_estimator__alpha":alpha,'clf__base_estimator__l1_ratio': l1_space,"norm__classifier_type":["MinMaxScaler","StandardScaler"]}
    model = BaggingRegressor(ElasticNet(tol=1), n_estimators=20)

    pipe = Pipeline([('norm', MyClassifier()), ('clf', model)])

    #gm_cv = RandomizedSearchCV(pipe, param_distributions=param_grid,cv=5,refit=True)
    gm_cv = GridSearchCV(pipe, param_grid, cv=4,refit=True)
    for param in gm_cv.get_params().keys():
        print(param)
    X = df.loc[:,df.columns!="usd_brl"] # here we have 2 input variables for multiple regression. If you just want to use one variable for simple linear regression, then use X = df['Interest_Rate'] for example.Alternatively, you may add additional variables within the brackets
    Y = df['usd_brl']# output variable (what we are trying to predict)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.4, random_state=42)
    gm_cv.fit(X_train, y_train)



    # Setup the GridSearchCV object: gm_cv
    
    # Fit it to the training data

    # Predict on the test set and compute metrics
    y_pred = gm_cv.predict(X_test)
    residual = (y_test - y_pred)
    r2 = gm_cv.score(X_test, y_test)
    mse = mean_squared_error(y_test, y_pred)
    betspar = gm_cv.best_params_
    est = gm_cv.best_estimator_.named_steps['clf']
    norm = gm_cv.best_estimator_.named_steps['norm']
    coef = "est.coef_"
    intercept = "est.intercept_"
    #estimator="gm_cv.estimator.estimators_"
    print("Tuned ElasticNet l1 ratio: {}".format(betspar))
    print("Tuned ElasticNet R squared: {}".format(r2))
    print("Tuned ElasticNet MSE: {}".format(mse))
    print("Coeficients: {}".format(coef))
    print("Intercept: {}".format(intercept))
    return gm_cv,betspar,r2,mse,coef,intercept,residual,est,norm
