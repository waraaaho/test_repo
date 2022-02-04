import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.metrics import roc_auc_score, r2_score
from sklearn.pipeline import Pipeline

from feature_engine.selection import (
    RecursiveFeatureElimination,
    DropConstantFeatures,
    DropDuplicateFeatures,
)

def feature_selection(input): #input type: pd dataframe
    # load dataset
    data = input
    #data.shape
    
    # separate train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        data.drop(data.columns[-1], axis=1), #drop last column
        data.iloc[:,-1], test_size=0.3, random_state=0)
    
    # Remove constant, quasi-constant and duplicated features
    pipe = Pipeline([
        ('constant', DropConstantFeatures(tol=0.998)),
        ('duplicated', DropDuplicateFeatures()),
    ])
    
    pipe.fit(X_train)
    
    # remove features
    
    X_train = pipe.transform(X_train)
    X_test = pipe.transform(X_test)
    
    # recursive feature elimination
    # the ML model for which we want to select features
    
    model = GradientBoostingClassifier(
        n_estimators=10,
        max_depth=2,
        random_state=10,
    )
    
    # Setup the RFE selector
    
    sel = RecursiveFeatureElimination(
        variables=None, # automatically evaluate all numerical variables
        estimator = model, # the ML model
        scoring = 'roc_auc', # the metric we want to evalute
        threshold = 0.0005, # the maximum performance drop allowed to remove a feature
        cv=2, # cross-validation
    )
    
    # this may take quite a while, because
    # we are building a lot of models with cross-validation
    sel.fit(X_train, y_train)
    
    # sort all importance in ascending order
    feat_importances = pd.Series(sel.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    
    #select top k features which meet threshold
    i, threshold = 0, 0.005
    while feat_importances[i]>threshold:
        i+=1
    print('cumulative selected features importance: ',feat_importances[:i].sum())
    selected_features = list(feat_importances.index[:i])
    
    return selected_features

