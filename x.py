# I want to write a model that recommends 5 new songs by interpreting the audio features and analysis data of a song received from the user.

# Importing libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
import random
import time
import requests
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_recall_curve

# Importing data

data = pd.read_csv('archive\SpotifyAudioFeaturesApril2019.csv')
data.head()

# Data cleaning

data.isnull().sum()
data.dropna(inplace=True)
data.info()
data.describe()

# Data visualization

for i in data.columns:
    plt.figure(figsize=(20, 10))
    sns.distplot(data[i])

# Data preprocessing

data.drop(['artist_name', 'track_name', 'track_id'], axis=1, inplace=True)
data.head()

# Data scaling

scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)
data_scaled = pd.DataFrame(data_scaled, columns=data.columns)
data_scaled.head()

# Data clustering

kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(data_scaled)
data_scaled['cluster'] = kmeans.labels_
data_scaled.head()

# Data visualization

for i in data_scaled.columns:
    plt.figure(figsize=(20, 10))
    sns.distplot(data_scaled[i])

# Recommendation system

import pandas as pd

columns_to_normalize = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']

for column in columns_to_normalize:
    data[column] = (data[column] - data[column].min()) / (data[column].max() - data[column].min())

data.head()

from sklearn.metrics.pairwise import cosine_similarity

song1_features = data.loc[data['id'] == 'şarkı_1_id'][columns_to_normalize].values
song2_features = data.loc[data['id'] == 'şarkı_2_id'][columns_to_normalize].values

similarity_score = cosine_similarity(song1_features, song2_features)

def recommend_similar_songs(song_id, data, num_recommendations=10):
   
    song_features = data.loc[data['id'] == song_id][columns_to_normalize].values

    similarity_scores = cosine_similarity(data[columns_to_normalize].values, song_features)

    similar_songs_indices = similarity_scores.argsort(axis=0)[:-num_recommendations-1:-1]
    
    recommended_song_ids = data.iloc[similar_songs_indices]['id'].values

    return recommended_song_ids
