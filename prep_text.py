from collections import defaultdict
import pymorphy2
import pymorphy2_dicts_uk
import string
import tokenize_uk
import re

morph = pymorphy2.MorphAnalyzer(lang="uk")

def text_to_sentences(file_name: str):

    sentences = []

    with open(file_name, "r", encoding="utf-8") as f:
        file = []
        for line in f:
            file.append(line.strip())

    split_sentences = tokenize_uk.tokenize_sents(' '.join(file))

    for index, sentence in enumerate(split_sentences, start=1):
        sentences.append((index, sentence))

    return sentences


def sentences_to_wordforms(sentences_list):

    word_forms = []

    for sent in sentences_list:
        word_forms.append((sent[0],) +  tuple([word.lower() for word in tokenize_uk.tokenize_words(sent[1]) if re.match(r"[А-ЩЬЮЯҐЄІЇа-щьюяґєії'`’ʼ]", word)]))

    return word_forms

    wordforms_to_lemmas(word_forms)


def wordforms_to_lemmas(word_forms_sequence):

    lemmas = []

    for wordforms_seq in word_forms_sequence:
        lemmas.append((wordforms_seq[0],) + tuple([morph.parse(wordform)[0].normal_form for wordform in wordforms_seq[1:]]))

    return lemmas


def set_pos_tags(lemmas_sequence):

    pos = []

    for lemmas_seq in lemmas_sequence:
        pos.append((lemmas_seq[0],) + tuple([morph.parse(lemma)[0].tag.POS for lemma in lemmas_seq[1:]]))

    return pos

def read_files(file_name):
    with open(file_name, encoding="utf-8") as f:
        return f.read()




