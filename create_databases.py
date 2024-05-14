import sqlite3
import prep_text

def create_fill_db(file_name: str, db_name: str):
    """
    Creates and fills an SQLite database with data extracted from a text file.

    Args:
        file_name (str): The path to the input text file.
        db_name (str): The name of the SQLite database to be created.

    Returns:
        None
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Drop existing tables if they exist
    c.execute("""DROP TABLE IF EXISTS sentences""")
    c.execute("""DROP TABLE IF EXISTS word_forms""")
    c.execute("""DROP TABLE IF EXISTS lem_pos""")
    c.execute("""DROP TABLE IF EXISTS texts""")

    # Create tables
    c.execute("""CREATE TABLE IF NOT EXISTS sentences (
        id integer primary key,
        sentence text,
        sent_numb integer,
        text_numb integer,
        FOREIGN KEY (text_numb) REFERENCES texts(id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS word_forms (
        id integer primary key,
        word_form varchar(50),
        sent_id integer,
        text_numb integer,
        FOREIGN KEY (sent_id) REFERENCES sentences(sent_numb),
        FOREIGN KEY (text_numb) REFERENCES texts(id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS lem_pos (
        word_form_id integer,
        word_form varchar(50),
        lemma varchar(50),
        pos varchar(10),
        sent_id integer,
        text_numb integer,
        FOREIGN KEY (sent_id) REFERENCES sentences(sent_numb),
        FOREIGN KEY (word_form_id) REFERENCES word_forms(id),
        FOREIGN KEY (text_numb) REFERENCES texts(id))
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS texts(
        id integer,
        text_body text)
        """)

    conn.commit()

    # Read text file
    text = prep_text.read_files(file_name)

    # Insert text into 'texts' table
    c.execute("INSERT INTO texts (id, text_body) VALUES (?, ?)", (1, text))

    # Extract sentences from text file and insert into 'sentences' table
    sentences = prep_text.text_to_sentences(file_name)
    count = 1
    for index, sentence in sentences:
        c.execute("INSERT INTO sentences (id, sentence, sent_numb, text_numb) VALUES (?, ?, ?, ?)", (count, sentence, index, 1))
        count += 1
        conn.commit()

    # Extract word forms from sentences and insert into 'word_forms' table
    word_forms = prep_text.sentences_to_wordforms(sentences)
    count = 1
    for sent_id, *words in word_forms:
        for word in words:
            c.execute("INSERT INTO word_forms (id, word_form, sent_id, text_numb) VALUES (?, ?, ?, ?)", (count, word, sent_id, 1))
            count += 1
            conn.commit()

    # Extract lemmas from word forms and insert into 'lem_pos' table with part-of-speech tags
    lemmas = prep_text.wordforms_to_lemmas(word_forms)
    pos_tags = prep_text.set_pos_tags(lemmas)
    count = 1
    for sent_id, words, lemmas, tags in zip(sentences, word_forms, lemmas, pos_tags):
        for word, lemma, pos in zip(words[1:], lemmas[1:], tags[1:]):
            c.execute("INSERT INTO lem_pos(word_form_id, word_form, lemma, pos, sent_id, text_numb) VALUES (?, ?, ?, ?, ?, ?)", (count, word, lemma, pos, sent_id[0], 1))
            count += 1
            conn.commit()

    conn.close()

create_fill_db('Narys_istorii_Ukrainy.txt', 'first_text.db')
create_fill_db('stus_poetry.txt', 'second_text.db')