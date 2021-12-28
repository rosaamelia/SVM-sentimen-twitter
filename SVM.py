# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qb4u-72VBC6JJaJHtKu5acTCOqjRzj0q
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import string
import re
# from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
df = pd.read_csv('datatoken2.csv')
df.head(30)

print(df.shape)

df_preprocessed = df.copy()
df_preprocessed = df_preprocessed.drop(columns=['no', 'tweet','tweetbaru'])
df_preprocessed.head()

s_1 = df_preprocessed[df_preprocessed['Jenis']==0]
s_2 = df_preprocessed[df_preprocessed['Jenis']==1]
# s_3 = df_preprocessed[df_preprocessed['Jenis']==-1].sample(14,replace=True)
df_preprocessed = pd.concat([s_1, s_2])

print(df_preprocessed.shape)
print(df_preprocessed['Jenis'].value_counts(normalize=True))

from wordcloud import WordCloud
import matplotlib.pyplot as plt


# Polarity == negative
train_s0 = df_preprocessed[df_preprocessed["Jenis"] == 0]
all_text_s0 = ' '.join(word for word in train_s0["TOKENIZATION"])
wordcloud = WordCloud(colormap='Reds', width=1000, height=1000, mode='RGBA', background_color='white').generate(all_text_s0)
plt.figure(figsize=(20,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()

# Polarity == 1 positive
train_s1 = df_preprocessed[df_preprocessed["Jenis"] == 1]
all_text_s1 = ' '.join(word for word in train_s1["TOKENIZATION"])
wordcloud = WordCloud(width=1000, height=1000, colormap='Blues', background_color='white', mode='RGBA').generate(all_text_s1)
plt.figure( figsize=(20,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()

!pip install Sastrawi

import Sastrawi
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

 
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()
# lakukan pada data kita

review = []
for index, row in df_preprocessed.iterrows():
    review.append(stopword.remove(row["TOKENIZATION"]))
    
df_preprocessed["TOKENIZATION"] = review
df_preprocessed["TOKENIZATION"].head()

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# implementasi pada data kita
review = []
for index, row in df_preprocessed.iterrows():
    review.append(stemmer.stem(row["TOKENIZATION"]))
    
df_preprocessed["TOKENIZATION"] = review
df_preprocessed["TOKENIZATION"]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(df_preprocessed['TOKENIZATION'], df_preprocessed['Jenis'], 
                                                    test_size=0.2, stratify=df_preprocessed['Jenis'], random_state=45)

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

#contoh
d = [
      'hari ini daring semangat',
      'semangat daring lagi semua',
      'semangat aku masih daring'
]
vectorizer = TfidfVectorizer(norm = None)
x = vectorizer.fit_transform(d)
x.toarray()

# implementasi pada dokumen kita
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print(X_train)
print(X_test)

from sklearn import svm
from sklearn.model_selection import cross_val_score

clf = svm.SVC(kernel="linear")

# lakukan prediksi pada data test
clf.fit(X_train,y_train)
predict = clf.predict(X_test)
# print(X_test)
print(y_test)



# import library evaluation
from sklearn.metrics import f1_score, recall_score, precision_score, confusion_matrix, accuracy_score
# f1_score
print("f1 score hasil prediksi adalah: ")
print(f1_score(y_test, predict))

# accuracy score
print("accuracy score hasil prediksi adalah: ")
print(accuracy_score(y_test, predict))

# precision score
print("precision score hasil prediksi adalah: ")
print(precision_score(y_test, predict))

# recall score
print("recall score hasil prediksi adalah: ")
print(recall_score(y_test, predict))

# confusion matrix
tn, fp, fn, tp = confusion_matrix(y_test, predict).ravel()
tn, fp, fn, tp

import string, re

def cleansing(data):
    # lower text
    data = data.lower()
    
    # hapus punctuation
    remove = string.punctuation
    translator = str.maketrans(remove, ' '*len(remove))
    data = data.translate(translator)
    
    # remove ASCII dan unicode
    data = data.encode('ascii', 'ignore').decode('utf-8')
    data = re.sub(r'[^\x00-\x7f]',r'', data)
    
    # remove newline
    data = data.replace('\n', ' ')
    
    return data

def preprocess_data(data):
    # cleansing data
    data = cleansing(data)
    
    # hapus stopwords
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    data = stopword.remove(data)
    
    # stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    data = stemmer.stem(data)
    
    # count vectorizer
    data = vectorizer.transform([data])
    
    return data

review =[]

for index, row in df.iterrows():
    hasil = clf.predict(preprocess_data(df['tweet'][index]))
    if hasil == [1]:
      review.append(1)
    else:
      review.append(0)
# print('review negatif sebanyak:',len(review))

import numpy as np
y = np.array(review)

print('Review positif sebanyak:',np.count_nonzero(y == 1))

print('Review negatif sebanyak:',np.count_nonzero(y == 0))