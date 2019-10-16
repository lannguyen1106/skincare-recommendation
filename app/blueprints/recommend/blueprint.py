from flask import Blueprint, render_template, jsonify, request, redirect
import tensorflow as tf
from tensorflow.keras.models import Model

import numpy as np
import pandas as pd

recommend_api = Blueprint('recommend', __name__)

user_embedding = None
product_embedding = None
skin_average_embedding = None
model = None
products = pd.read_csv('static/feature_embeddings/products.csv')

USER_EMBEDDING = 'user_embedding.npy'
PRODUCT_EMBEDDING = 'product_embedding.npy'
USER_EMBEDDING_DL = 'user_embedding_dl.npy'
PRODUCT_EMBEDDING_DL = 'product_embedding_dl.npy'
SKIN_EMBEDDING = 'skin_average_embedding.npy'
DOT = 'dot'
COSINE = 'cosine'
MODEL = 'my_model.h5'

sktypes = ['normal', 'combination', 'dry', 'oily']
sktones = ['light', 'deep', 'olive', 'fair', 'medium', 'dark']

def load_embeddings():
   global user_embedding, product_embedding, skin_average_embedding

   user_embedding = np.load("static/feature_embeddings/" + USER_EMBEDDING, allow_pickle=True)
   product_embedding = np.load("static/feature_embeddings/" + PRODUCT_EMBEDDING, allow_pickle=True)
   skin_average_embedding = np.load("static/feature_embeddings/" + SKIN_EMBEDDING, allow_pickle=True)

def load_model():
   global model

   model = tf.keras.models.load_model('/static/models/' + MODEL)

   layer_name = 'embedding_4'
   model = Model(inputs=model.input, outputs=model.get_layer(layer_name).output)


def compute_scores(query_embedding, item_embeddings, measure=DOT):
   u = query_embedding
   V = item_embeddings
   if measure == COSINE:
      V = V / np.linalg.norm(V, axis=1, keepdims=True)
      u = u / np.linalg.norm(u)
   scores = u.dot(V.T)
   return scores

def user_recommendations(user_id, user_embedding, product_embedding, measure=DOT, exclude_rated=True, k=6):
   scores = compute_scores(
      user_embedding[user_id], product_embedding, measure)
   score_key = measure + ' score'
   
   df = pd.DataFrame({
      score_key: list(scores),
      'product_id': products['product_id'],
      'title': products['title'],
      'category': products['category'],
   })
   if exclude_rated:
      # remove products that are already rated
      rated_products = ratings[ratings.user_id == user_id]["product_id"].values
      df = df[df.product_id.apply(lambda product_id: product_id not in rated_products)]
   
   return df.values.tolist()

def new_user_recommendations(user_embedding, product_embedding, measure=DOT, k=5):
   scores = compute_scores(
      user_embedding, product_embedding, measure)
   score_key = measure + ' score'
   
   df = pd.DataFrame({
      score_key: list(scores),
      'product_id': products['product_id'],
      'title': products['title'],
      'category': products['category'],
      'image_url': products['image_url']
   })
   
   return df.sort_values([score_key], ascending=False).head(k)

def product_neighbors(product_embedding, title_substring, measure=DOT, k=6):
   # Search for product ids that match the given substring.
   ids =  products[products['title'].str.contains(title_substring)].index.values
   titles = products.iloc[ids]['title'].values
   
   if len(titles) == 0:
      raise ValueError("Found no products with title %s" % title_substring)
   print("Nearest neighbors of : %s." % titles[0])
   if len(titles) > 1:
      print("[Found more than one matching product. Other candidates: {}]".format(
         ", ".join(titles[1:])))
   product_id = ids[0]
   scores = compute_scores(
      product_embedding[product_id], product_embedding,
      measure)
   score_key = measure + ' score'
   df = pd.DataFrame({
      score_key: list(scores),
      'title': products['title'],
      'category': products['category']
   })
   
   return df.values.tolist()

@recommend_api.route('/recommend', methods=['GET', 'POST'])  
def compute_recommendation():

   if user_embedding is None or product_embedding is None or skin_average_embedding is None:
      load_embeddings()

   if request.method == 'GET':
      return redirect("/")

   if request.method == 'POST':
      
      # data = request.form

      skin_type = request.form['options_skin_type']
      skin_tone = request.form['options_skin_tone']

      user_profile = {'skin_type' : skin_type, 'skin_tone': skin_tone}

      # calculate feature vectors of user from input data
      index = len(sktones) * sktypes.index(skin_type) + sktones.index(skin_tone)
      feature_vector = skin_average_embedding[index]

      # recommendation
      df = new_user_recommendations(feature_vector, product_embedding, measure='COSINE', k=10)
      headers = list(df)

      products = []

      for index, row in df.iterrows():
         obj = {}

         for idx, item in enumerate(row):
            obj[headers[idx]] = item
         
         products.append(obj)

   return render_template('recommend.html', user_profile=user_profile, products=products, tables=[df.to_html(classes='data')], titles=df.columns.values)
