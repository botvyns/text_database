import sqlite3

def find_by_lemma(base_form: str, database: str):
    """
    Find sentences containing the given lemma in the specified database.

    Args:
        base_form (str): The base form of the word to search for.
        database (str): The name of the SQLite database.

    Returns:
        list: A list of tuples containing the lemma, sentence, and sentence number.
              If no matching lemma is found, returns a message indicating so.
    """
    conn = sqlite3.connect(database)
    c = conn.cursor()

    result = c.execute("SELECT DISTINCT lemma, sentence, sentences.sent_numb FROM lem_pos INNER JOIN sentences ON lem_pos.sent_id=sentences.sent_numb  WHERE lemma=?", (base_form,)).fetchall()

    c.close()

    if result:
        return result
    return [('Такої леми у тексті немає',)]

def find_by_wordform(form: str, database: str):
    """
    Find sentences containing the given word form in the specified database.

    Args:
        form (str): The word form to search for.
        database (str): The name of the SQLite database.

    Returns:
        list: A list of tuples containing the word form, sentence, and sentence number.
              If no matching word form is found, returns a message indicating so.
    """
    conn = sqlite3.connect(database)
    c = conn.cursor()

    result = c.execute("SELECT DISTINCT word_form, sentence, sentences.sent_numb FROM lem_pos INNER JOIN sentences ON lem_pos.sent_id=sentences.sent_numb WHERE word_form=?", (form,)).fetchall()

    c.close()

    if result:
        return result
    return [('Такої словоформи у тексті немає',)]

def user_input(word: str, word_type: str, database: str):
    """
    Process user input and perform the corresponding search.

    Args:
        word (str): The word (base form or word form) to search for.
        word_type (str): 'F' for word form search, 'L' for lemma search.
        database (str): The name of the SQLite database.

    Returns:
        list: A list of tuples containing the search results.
    """
    if word_type == 'F':
        return find_by_wordform(word, database)
    elif word_type == 'L':
        return find_by_lemma(word, database)
    else:
        return [('Неправильно вказаний тип слова для пошуку',)]