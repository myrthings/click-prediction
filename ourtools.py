#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:29:39 2020

@author: Myriam
"""
from copy import deepcopy
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.utils import shuffle
from sklearn.metrics import classification_report,confusion_matrix,roc_auc_score,roc_curve,cohen_kappa_score,precision_score,recall_score,accuracy_score
import pandas as pd
import numpy as np


'''
These 3 first functions are created by our teacher at IE @frandiego (https://github.com/frandiego)
'''
## map encoder
def map_encoder_categorical(x):
    set_ = sorted(set(x))
    range_ = list(range(1,len(set_)+1))
    return dict(zip(set_,range_))

def map_encoder_fit(df,categorical_features):
    return {i:map_encoder_categorical(df[i]) for i in categorical_features}

def map_encoder_transform(df,map_encoder):
    df_ = deepcopy(df) 
    for i in map_encoder.keys():
        map_encoder_variable = map_encoder[i]
        fill_ = int(max(map_encoder_variable.values()) + 1)
        df_[i] = df_[i].map(map_encoder_variable).fillna(fill_).astype(int)
    return df_

'''
These other functions where created by us to make a faster analysis
'''

def visual(category,dataset):
    grouped=dataset.groupby([category,'clicks'])[['date']].count().rename(columns={'date':'interactions'}).reset_index()
    grouped['percent']=grouped.apply(lambda x: round(x['interactions']/grouped.loc[grouped[category]==x[category],'interactions'].sum(),2),axis=1)
    #display(grouped.set_index([category,'clicks']))

    #display(grouped[['Device','percent','Clicks']].set_index(['Device','Clicks']).unstack().fillna(0))

    fig, (ax1, ax2)=plt.subplots(1,2,figsize=(15,6))
    sns.set()
    for_plot=grouped[[category,'percent','clicks']].set_index([category,'clicks']).unstack().fillna(0)
    for_plot.columns=for_plot.columns.droplevel()
    
    grouped=grouped.reset_index().groupby(category)['interactions'].sum().sort_values().plot(kind='barh',ax=ax1)
    for_plot.sort_values(1).plot(kind='barh',stacked='True',ax=ax2)
    
    fig.suptitle(category)
    ax1.set_ylabel('Nº interactions')
    ax2.set_xlabel('')
    ax1.set_xlabel('')
    ax2.set_ylabel('% of interactions')

    #sns.barplot(x="Device", y="percent", data=grouped,hue='Clicks',stacked=True)
    plt.plot()
    
    
    
def undersample(dataset,label,proportion_test=0.01,max_cut_label=0.1):
    df=deepcopy(dataset)
    
    #get the categorie with less values
    min_cat=df[label].value_counts().tail(1)
    min_label=min_cat.index[0]
    min_value=min_cat[min_label]
    
    #get the df for every value
    df1=df[df[label]==1]
    df0=df[df[label]==0]
    
    #get the numbers of the proportion we want
    value=round(abs((1-proportion_test)*len(df1) + proportion_test*len(df0)) / (1-2*proportion_test))
    if value/min_value>max_cut_label:
        cut_label=max_cut_label
    else:
        cut_label=value/min_value
    
    
    test1=int(min_value*cut_label)-1
    train1=int(min_value-test1)
    train0=int(train1)
    test0=int(test1/proportion_test)-1
    
    
    # cut the datasets with the numbers
    df1=shuffle(df1).reset_index(drop=True)
    df_test1=df1.iloc[:test1]
    df_train1=df1.iloc[test1:]
    
    df0=shuffle(df0).reset_index(drop=True)
    df_test0=df0.iloc[:test0]
    df_train0=df0.iloc[test0:test0+train0]
    
    # concat the dataset
    df_train=shuffle(pd.concat([df_train0,df_train1],axis=0)).reset_index(drop=True)
    df_test=shuffle(pd.concat([df_test0,df_test1],axis=0)).reset_index(drop=True)

    return df_train,df_test,abs(len(df_test0)+len(df_train0))/len(df0),abs(len(df_test1)+len(df_train1))/len(df1)
    
    
def apply_models(models,X_train,y_train,X_test,y_test):
    df_metrics=pd.DataFrame([])
    feature_imp=pd.DataFrame([])

    for model_name in models.keys():
        print(model_name)
        pos=0
        metrics={}
        model=models[model_name]
        model.fit(X_train,y_train)
        y_pred=model.predict(X_test)
        try:
            probs=model.predict_proba(X_test)
            pos=1
        except:
            pos=0
        conf=confusion_matrix(y_test,y_pred)
        #metrics['recall_0']=conf[0][0]/(conf[0][0]+conf[1][0])
        #metrics['precision_0']=conf[0][0]/(conf[0][0]+conf[0][1])
        #metrics['recall_1']=conf[1][1]/(conf[1][1]+conf[1][0])
        #metrics['precision_1']=conf[0][1]/(conf[0][0]+conf[0][1])
        metrics['accuracy']=accuracy_score(y_test,y_pred)
        metrics['cohen_kappa']=cohen_kappa_score(y_test,y_pred)
        if pos==1:
            metrics['roc_auc']=roc_auc_score(y_test,[item for _,item in probs])
        else:
            metrics['roc_auc']=np.nan

        df_metrics=pd.concat([df_metrics,pd.DataFrame(metrics,index=[model_name]).T],axis=1)
        try:
            feature_imp=pd.concat([feature_imp,pd.DataFrame({'variable':X_train.columns,'imp_'+model_name:model.feature_importances_}).set_index('variable')],axis=1)
        except:
            None
    return df_metrics, feature_imp
    
    
    