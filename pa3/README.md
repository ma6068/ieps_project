You have to install packages: nltk, os, bs4, stopwords

Running the python program "data_processing.py" will result in an error if the "inverted-index.db" database already exists.

In order for the database to be filled up, the python code "data_processing.py" needs to be run.

Running the SQLite search: python run-sqlite-search.py "query"

Running the Basic search: python run-basic-search.py "query"

The way the program is coded, you need an argument each time you run the Basic or SQLite search. With that being said, running the program with the "Run" function prints a clearer result.

Note: in some cases the nltk package gives an error because the resources needed for that package cannot be downloaded at first. In order to fix this error, the line "nltk.download('stopwords')", which is the first line in both main functions needs to be moved right under the "import nltk" line which can be found at the top of the document. Once the program has downloaded this resource, you can revert changes and continue using the program as it was meant to be used.