import os
import nltk
from bs4 import BeautifulSoup
import stopwords
import db
from more_itertools import locate

sites = ['e-prostor.gov.si', 'e-uprava.gov.si', 'evem.gov.si', 'podatki.gov.si']
nltk.download('stopwords')
nltk.download('punkt')
db = db.DB()
db.createTable()

for site in sites:
    url = 'data/' + site
    html_files = os.listdir(url)   # put all files names in that folder in list
    for i in range(1, len(html_files)):
        html = open(url + '/' + html_files[i], 'rb').read().decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        for s in soup(["script", "style"]):
            s.extract()
        # text = soup.body.get_text()
        text = ' '.join(soup.stripped_strings)
        # tokenization (we put all words/symbols in a list)
        tokenized = nltk.word_tokenize(text, language="slovene")
        print(tokenized)
        for el in tokenized:
            word = el.lower()  # all words need to be with small letters
            if word not in stopwords.stop_words_slovene:
                # add the word in table IndexWord
                db.insert_index_word(word)
                # find all indexes of a word in the text
                indexes = [j for j, val in enumerate(tokenized) if val == el]
                print(indexes)
                for lala in indexes:
                    print(tokenized[lala])
                print("kraj")
        break
    break


