from collections import defaultdict
import pymorphy2
import pymorphy2_dicts_uk
import string
import tokenize_uk
import re

morph = pymorphy2.MorphAnalyzer(lang="uk")


def text_to_sentences(file_name: str) -> list:
    """
    Converts text from a file into a list of sentences.

    Args:
        file_name (str): The path to the input text file.

    Returns:
        list: A list of tuples where each tuple contains the sentence index and the sentence text.
    """
    sentences = []

    with open(file_name, "r", encoding="utf-8") as f:
        file = [line.strip() for line in f]

    split_sentences = tokenize_uk.tokenize_sents(' '.join(file))

    for index, sentence in enumerate(split_sentences, start=1):
        sentences.append((index, sentence))

    return sentences


def sentences_to_wordforms(sentences_list: list) -> list:
    """
    Tokenizes sentences into word forms.

    Args:
        sentences_list (list): A list of tuples where each tuple contains the sentence index and the sentence text.

    Returns:
        list: A list of tuples where each tuple contains the sentence index and word forms.
    """
    word_forms = []

    for sent in sentences_list:
        word_forms.append((sent[0],) + tuple([word.lower() for word in tokenize_uk.tokenize_words(sent[1]) if re.match(r"[А-ЩЬЮЯҐЄІЇа-щьюяґєії'`’ʼ]", word)]))

    return word_forms


def wordforms_to_lemmas(word_forms_sequence: list) -> list:
    """
    Converts word forms into lemmas.

    Args:
        word_forms_sequence (list): A list of tuples where each tuple contains the sentence index and word forms.

    Returns:
        list: A list of tuples where each tuple contains the sentence index and lemmas.
    """
    lemmas = []

    for wordforms_seq in word_forms_sequence:
        lemmas.append((wordforms_seq[0],) + tuple([morph.parse(wordform)[0].normal_form for wordform in wordforms_seq[1:]]))

    return lemmas


def set_pos_tags(lemmas_sequence: list) -> list:
    """
    Sets part-of-speech tags for lemmas.

    Args:
        lemmas_sequence (list): A list of tuples where each tuple contains the sentence index and lemmas.

    Returns:
        list: A list of tuples where each tuple contains the sentence index and part-of-speech tags.
    """
    pos = []

    for lemmas_seq in lemmas_sequence:
        pos.append((lemmas_seq[0],) + tuple([morph.parse(lemma)[0].tag.POS for lemma in lemmas_seq[1:]]))

    return pos


def read_files(file_name: str) -> str:
    """
    Reads the content of a file.

    Args:
        file_name (str): The path to the input text file.

    Returns:
        str: The content of the file as a string.
    """
    with open(file_name, encoding="utf-8") as f:
        return f.read()