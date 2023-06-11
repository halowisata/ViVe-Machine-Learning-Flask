# app\models\collaborative_filtering\prediction.py

# Functions for model prediction
# This file contains functions to make predictions using trained ML models
# Implement prediction functions that take input data and return model predictions
# Customize these functions based on the specific ML models and prediction requirements of your project


import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import Callback

user = pd.read_csv("./datasets/raw/user.csv")
rat = pd.read_csv("./datasets/raw/tourism_rating.csv")
update = pd.read_csv('./datasets/raw/tourism_with_id_updated.csv')


user_ids = rat['User_Id'].unique().tolist()
user_to_user_encoded = {x: i for i, x in enumerate(user_ids)}
user_encoded_to_user = {i: x for i, x in enumerate(user_ids)}
place_ids = rat['Place_Id'].unique().tolist()
place_to_place_encoded = {x: i for i, x in enumerate(place_ids)}
place_encoded_to_place = {i: x for i, x in enumerate(place_ids)}
collfil = rat.copy()
collfil['user'] = collfil['User_Id'].map(user_to_user_encoded)
collfil['place'] = collfil['Place_Id'].map(place_to_place_encoded)
num_users = len(user_to_user_encoded)
num_places = len(place_encoded_to_place)

collfil['rating'] = collfil['Place_Ratings'].values.astype(np.float32)

min_rating = min(collfil['rating'])
max_rating = max(collfil['rating'])

x = collfil[['user', 'place']].values

y = collfil['rating'].apply(lambda x: (
    x - min_rating) / (max_rating - min_rating)).values

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.33, random_state=42)


class RecommenderNet(tf.keras.Model):

    # Insialisasi fungsi
    def __init__(self, num_users, num_places, embedding_size, **kwargs):
        super(RecommenderNet, self).__init__(**kwargs)
        self.num_users = num_users
        self.num_places = num_places
        self.embedding_size = embedding_size
        self.user_embedding = layers.Embedding(  # layer embedding user
            num_users,
            embedding_size,
            embeddings_initializer='he_normal',
            embeddings_regularizer=keras.regularizers.l2(1e-6)
        )
        self.user_bias = layers.Embedding(
            num_users, 1)  # layer embedding user bias
        self.places_embedding = layers.Embedding(  # layer embeddings places
            num_places,
            embedding_size,
            embeddings_initializer='he_normal',
            embeddings_regularizer=keras.regularizers.l2(1e-6)
        )
        self.places_bias = layers.Embedding(
            num_places, 1)  # layer embedding places bias

    def call(self, inputs):
        user_vector = self.user_embedding(
            inputs[:, 0])  # memanggil layer embedding 1
        user_bias = self.user_bias(inputs[:, 0])  # memanggil layer embedding 2
        places_vector = self.places_embedding(
            inputs[:, 1])  # memanggil layer embedding 3
        # memanggil layer embedding 4
        places_bias = self.places_bias(inputs[:, 1])

        dot_user_places = tf.tensordot(user_vector, places_vector, 2)

        x = dot_user_places + user_bias + places_bias

        return tf.nn.sigmoid(x)  # activation sigmoid


class myCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        if logs['val_root_mean_squared_error'] <= 0.25:
            self.model.stop_training = True


def training(num_users, num_places, x_train, y_train, x_test, y_test):
    model = RecommenderNet(num_users, num_places, 50)  # inisialisasi model
    model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(),
        optimizer=keras.optimizers.Adam(learning_rate=0.0004),
        metrics=[tf.keras.metrics.RootMeanSquaredError()]
    )

    # Memulai training
    history = model.fit(
        x=x_train,
        y=y_train,
        epochs=100,
        validation_data=(x_test, y_test),
        callbacks=[myCallback()]
    )

    # Save the trained model weights
    model.save_weights("model_weights.h5")


def give_scoring(df):
    # this function will return score for each user recommended items
    df['score'] = 1
    return df


def prediction(user_to_user_encoded, place_encoded_to_place, model, user_id):
    place_df = update[['Place_Id', 'Place_Name',
                       'new_category', 'Rating', 'Price']]
    place_df.columns = ['id', 'place_name', 'category', 'rating', 'price']
    df = rat.copy()


    place_visited_by_user = df[df.User_Id == user_id]

    # Membuat data lokasi yang belum dikunjungi user
    place_not_rated = place_df[~place_df['id'].isin(
        place_visited_by_user.Place_Id.values)]['id']
    place_not_rated = list(
        set(place_not_rated).intersection(set(place_to_place_encoded.keys()))
    )

    place_not_rated = [
        [place_to_place_encoded.get(x)] for x in place_not_rated]

    user_encoder = user_to_user_encoded.get(int(user_id))
    if user_encoder is not None:
        user_place_array = np.hstack(
            ([[user_encoder]] * len(place_not_rated), place_not_rated)
        )
    else:
        return

    if user_place_array is not None:
        ratings = model.predict(user_place_array).flatten()
    else:
        ratings = None
    top_ratings_indices = ratings.argsort()[-5:][::-1]
    recommended_place_ids = [
        place_encoded_to_place.get(place_not_rated[x][0]) for x in top_ratings_indices
    ]

    cf_recommendation = place_df[place_df['id'].isin(recommended_place_ids)]

    cf_recommendation.drop(
        ["place_name", "category", "rating", "price"], axis=1, inplace=True)

    cf_recommendation.rename(columns={'id': 'Place_Id'}, inplace=True)

    return cf_recommendation


def cf_main(user_id):
    # Check if the model weights file exists
    try:
        with open("model_weights.h5"):
            model_weights_exist = True
    except FileNotFoundError:
        model_weights_exist = False

    if model_weights_exist:

        # If model weights exist, load them and perform prediction
        model = RecommenderNet(num_users, num_places, 50)
        _ = model.predict(np.zeros((1, 2)))
        model.load_weights("model_weights.h5")
        recommendation = prediction(
            user_to_user_encoded, place_encoded_to_place, model, user_id)
    else:
        # If model weights don't exist, perform training and then prediction

        training(num_users, num_places, x_train, y_train, x_test, y_test)
        model = RecommenderNet(num_users, num_places, 50)
        _ = model.predict(np.zeros((1, 2)))
        model.load_weights("model_weights.h5")
        recommendation = prediction(
            user_to_user_encoded, place_encoded_to_place, model, user_id)

    if recommendation is None:
        return None

    recommendation = give_scoring(recommendation)

    return recommendation
