import os
import time
import nltk
from bs4 import BeautifulSoup
import stopwords


def get_html_text(url):
    html = open(url, 'rb').read().decode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style"]):
        s.extract()
    text = ' '.join(soup.stripped_strings)
    return text


def search_all_pages(words, sites):
    postings = []
    for site in sites:
        url = 'data/' + site
        html_files = os.listdir(url)   # put all files names in that folder in list
        for i in range(1, len(html_files)):
            text = get_html_text(url + '/' + html_files[i])
            tokenized = nltk.word_tokenize(text, language="slovene")
            indexes = []
            for word in words:
                indexes += [str(j) for j, val in enumerate(tokenized) if val.lower() == word]
            frequency = len(indexes)
            if frequency == 0:
                continue
            postings.append((frequency, site + '/' + html_files[i], ','.join(indexes)))
    return postings


def basic_search(input, sites):
    print("Results for a query: \"" + input + "\"")
    tokenized = nltk.word_tokenize(input, language="slovene")
    words = []
    for el in tokenized:
        word = el.lower()  # all words need to be with small letters
        if word not in stopwords.stop_words_slovene:
            words.append(word)
    start_time = time.time()
    postings = search_all_pages(words, sites)
    stop_time = time.time()
    ms = str((stop_time - start_time) * 1000)
    if postings:
        print("Results found in " + ms + "ms.")
        print("Frequencies Document                                   Snippet")
        print("----------- ------------------------------------------ "
              "-----------------------------------------------------"
              "------")
        max_hits = 9
        hits = 0
        postings = sorted(postings, key=lambda x: int(x[0]), reverse=True)
        for el in postings:
            html_text = get_html_text('data/' + el[1])
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
    sites = ['e-prostor.gov.si', 'e-uprava.gov.si', 'evem.gov.si', 'podatki.gov.si']
    nltk.download('stopwords')
    nltk.download('punkt')
    input = "Sistem SPOT"
    basic_search(input, sites)
