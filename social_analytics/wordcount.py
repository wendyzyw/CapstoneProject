import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

with open('/Users/yuhan/Desktop/data.json') as f:
    data = json.loads(f.read())
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
word_tokenizer = nltk.tokenize.regexp.WordPunctTokenizer()

file_text = open('/Users/yuhan/Desktop/profile.txt', 'r')
with open('/Users/yuhan/Desktop/data.json') as f:
    data = json.loads(f.read())
    
BOW = {}
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

    # line=re.split(r'\W+',line)
    wo = line.split(' ')
    for word in wo:
        # print (word)
        word = lemmatizer.lemmatize(word.lower())
        if word not in stop_words and word != '':
            BOW[word] = BOW.get(word, 0) + 1

string_list = []
string_list_new = []
import json
import json

for word in BOW:
    word = word.encode('ascii')
    string = "{text: '" + word + "', size: " + str(BOW[word]) + "}"
    # print string
    string_list.append(string)
