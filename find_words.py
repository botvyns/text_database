import sqlite3

def find_by_lemma(base_form, database):

    conn = sqlite3.connect(database)

    c = conn.cursor()

    result = c.execute("SELECT DISTINCT lemma, sentence, sentences.sent_numb FROM lem_pos INNER JOIN sentences ON lem_pos.sent_id=sentences.sent_numb  WHERE lemma=?", (base_form,)).fetchall()

    c.close()

    if result:
        return [print(res, ('\n')) for res in result]
    return 'Такої леми у тексті немає'

def find_by_wordform(form, database):

    conn = sqlite3.connect(database)

    c = conn.cursor()

    result = c.execute("SELECT DISTINCT word_form, sentence, sentences.sent_numb FROM lem_pos INNER JOIN sentences ON lem_pos.sent_id=sentences.sent_numb WHERE word_form=?", (form,)).fetchall()

    c.close()

    if result:
        return [print(res, ('\n')) for res in result]
    return 'Такої словоформи у тексті немає'

def user_input(word, word_type, database):

    return find_by_wordform(word, database) if word_type == 'F' else find_by_lemma(word, database)

user = input("""Введіть три параметри для пошуку слів:
                1. Слово малими літерами
                2. L -> пошук за лемою АБО F -> пошук за словоформою
                3. Назва тексту (базою даних) : first_t.db АБО second_t.db
    """)

word, word_type, database = user.split()

print(user_input(word, word_type, database))


