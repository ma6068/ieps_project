import sys
import time
import nltk
from bs4 import BeautifulSoup
import db
import stopwords


def get_html_text(url):
    html = open("data/" + url, 'rb').read().decode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style"]):
        s.extract()
    text = ' '.join(soup.stripped_strings)
    return text


def db_search(input):
    print("Results for a query: \"" + input + "\"")
    tokenized = nltk.word_tokenize(input, language="slovene")
    words = []
    for el in tokenized:
        word = el.lower()  # all words need to be with small letters
        if word not in stopwords.stop_words_slovene:
            words.append(word)
    start_time = time.time()
    postings = db.get_postings_by_words(words)
    stop_time = time.time()
    ms = str((stop_time - start_time) * 1000)
    if postings:
        print("Results found in " + ms + "ms.")
        print("Frequencies Document                                   Snippet")
        print("----------- ------------------------------------------ "
              "----------------------------------------------------- "
              "------")
        max_hits = 9
        hits = 0
        for el in postings:
            html_text = get_html_text(el[1])
            tokenized = nltk.word_tokenize(html_text, language="slovene")
            indexes = el[2].split(",")
            snippet = ''
            for j in range(len(indexes)):
                i = int(indexes[j])
                if i + 3 < len(tokenized):
                    snippet += tokenized[i] + " " + tokenized[i + 1] + " " + tokenized[i + 2] + " " + tokenized[i + 3] \
                               + " ... "
                else:
                    snippet += "..." + tokenized[i - 3] + " " + tokenized[i - 2] + " " \
                               + tokenized[i - 1] + " " + tokenized[i]
            spaces1 = ' ' * (12 - len(str(el[0])))
            spaces2 = ' ' * (43 - len(str(el[1])))
            print(str(el[0]) + spaces1 + el[1] + spaces2 + snippet)
            hits += 1
            if hits == max_hits:
                break
    else:
        print("Word not found!")


if __name__ == "__main__":
    nltk.download('stopwords')
    nltk.download('punkt')
    db = db.DB()
    db_search(" ".join(sys.argv[1:]))
    # db.disconnectDB()
