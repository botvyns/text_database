import sqlite3
import prep_text

def create_fill_db(file_name, db_name):

    conn = sqlite3.connect(db_name)

    c = conn.cursor()

    # колонка з номером вибірки або її назвою

    c.execute("""DROP TABLE IF EXISTS sentences""")
    c.execute("""DROP TABLE IF EXISTS word_forms""")
    c.execute("""DROP TABLE IF EXISTS lem_pos""")
    c.execute("""DROP TABLE IF EXISTS texts""")

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

    text = prep_text.read_files(file_name)


    c.execute("INSERT INTO texts (id, text_body) VALUES (?, ?)", (1, text))


    sent = prep_text.text_to_sentences(file_name)

    count = 1

    for i in sent:
        c.execute("INSERT INTO sentences (id, sentence, sent_numb, text_numb) VALUES (?, ?, ?, ?)", (count, i[1], i[0], 1))
        count += 1
        conn.commit()


    forms = prep_text.sentences_to_wordforms(sent)


    count = 1

    for s in forms:
        for f in s[1:]:
            c.execute("INSERT INTO word_forms (id, word_form, sent_id, text_numb) VALUES (?, ?, ?, ?)", (count, f, s[0], 1))
            count += 1
            conn.commit()

            conn.commit()

    lemmas = prep_text.wordforms_to_lemmas(forms)


    pos = prep_text.set_pos_tags(lemmas)


    count = 1

    for s in forms:
        temp = zip(s[1:], lemmas[forms.index(s)][1:], pos[forms.index(s)][1:])
        for f in temp:
            c.execute("INSERT INTO lem_pos(word_form_id, word_form, lemma, pos, sent_id, text_numb) VALUES (?, ?, ?, ?, ?, ?)", (count, f[0], f[1], f[2], s[0], 1))
            count += 1
            conn.commit()

    conn.commit()

    conn.close()

create_fill_db('Narys_instorii_Ukrainy.txt', 'first_t.db')

create_fill_db('stus_poetry.txt', 'second_t.db')
