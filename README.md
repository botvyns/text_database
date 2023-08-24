# text_database
A project on creating database based on the text in Ukrainian (in my case, two databses were created based on [Narys_istorii_Ukrainy.txt](https://github.com/botvyns/text_database/blob/main/Narys_istorii_Ukrainy.txt)
and [stus_poetry.txt](https://github.com/botvyns/text_database/blob/main/stus_poetry.txt) texts. 

The text preprocessing is done in [prep_text.py](https://github.com/botvyns/text_database/blob/main/prep_text.py). The prerocessing includes segmentation of the text into sentences, tokenization of the text by
wordforms, lemmatization, and assignment of POS tags to lemmas. At the same timethe text was cleaned of various special characters.

Database creation is done in [two_db.py](https://github.com/botvyns/text_database/blob/main/two_db.py). Files that contain databases are [first_t.db](https://github.com/botvyns/text_database/blob/main/first_t.db) and
[second_t.db](https://github.com/botvyns/text_database/blob/main/second_t.db). Each database contains four tables:sentences, word_forms, lem_pos, texts.

To search for a word, run the [find_words.py](https://github.com/botvyns/text_database/blob/main/find_words.py) file. 
You will be will be asked to enter three parameters separated by a space:
а) The word in lowercase letters
б) L -> search by lemma OR F -> search by word form
в) Name of the text (database) : first_t.db OR second_t.db
For example, possible variants: життя L second_t.db, пече F
second_t.db, українського F first_t.db, etc.
The query will return:

1) the search word;
2) the sentence in which the corresponding wordform occurs (both when
you specify the lemma, and when you specify the word form as the first
parameter);
3) the sentence number in the corresponding text.

An example of searching by lemma (L) for lemma життя in the second text (second_t.db)

![some text](https://github.com/botvyns/text_database/blob/main/Screenshot%202023-08-24%20at%2020.05.26.png)


An example of searching by wordform (F) for wordform українського in the first text (first_t.db)

![some text](https://github.com/botvyns/text_database/blob/main/Screenshot%202023-08-24%20at%2020.04.47.png)
