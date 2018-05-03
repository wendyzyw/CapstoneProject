from django.shortcuts import render
from .forms import LoginForm,ChangepassForm,EdituserinfoForm,RegisterForm,MyPasswordResetForm
from django.contrib import auth
import nltk
import re
import json
import nltk.stem.WordNetLemmatizer

lemmatizer = nltk.stem.WordNetLemmatizer()
word_tokenizer = nltk.tokenize.regexp.WordPunctTokenizer()
file_text = open('/Users/yuhan/Desktop/profile.txt', 'r')
def word_count(file):
    BOW = {}
    string_list = []
    for line in file_text:
        line = line.rstrip()
        line = line.replace('#', '')
        line = line.replace(',', '')
        line = line.replace('.', '')
        line = line.replace(':', '')
        line = line.replace('--', '')
        line = line.replace('"', '')
        line = line.replace('?', '')
        line = line.replace('(', '')
        line = line.replace(')', '')
        wo = line.split(' ')
        for word in wo:
            word = lemmatizer.lemmatize(word.lower())
            if word != '':
                BOW[word] = BOW.get(word, 0) + 1
        for word in BOW:
            word = word.encode('ascii')
            # print (word)
            # print ("{text: '"+word+"\', size: "+str(BOW[word])+"},")
            string = "{text: '" + word + "', size: " + str(BOW[word]) + "}"
            # print string
            string_list.append(string)

    return string_list
print (word_count(file_text))
