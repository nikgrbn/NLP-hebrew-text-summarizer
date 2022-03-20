import re
import math
from typing import Dict, List
from src.connectors_dataset import connectors_list
import nltk
from nltk import tokenize
from tqdm import tqdm


def create_tf_table(text):
    # Create 'Term-Frequency' table
    sentences = create_sentence_array(text)
    words = create_words_array(text)

    tf_table = dict()
    for word in tqdm(words):
        sentence_to_value = dict()
        for sentence in sentences:
            words_in_sentence = create_words_array(sentence)
            if words_in_sentence:  # check if the list is empty
                sentence_to_value[sentence] = count_word_in_doc(word, sentence) / len(words_in_sentence)
        tf_table[word] = sentence_to_value

    return tf_table


def create_idf_table(text):
    # Create 'Inverse Document Frequency' table
    paragraphs = create_paragraph_array(text)
    words = create_words_array(text)

    idf_table = dict()
    for word in tqdm(words):
        # create element with the word and the IDF equation with log
        # number of sentences divide the numbers of sentences that include specific word from the text words
        num_sentences_word_include = count_word_from_paragraphs(word, paragraphs)
        idf_equation = math.log(len(paragraphs) / num_sentences_word_include)
        idf_table[word] = idf_equation
    return idf_table


def count_word_in_doc(word: str, document: str):
    counter = 0
    k = 0.3

    d_words = create_words_array(document)
    for d_word in d_words:
        if word is d_word:
            counter += 1
        elif word in d_word:
            if len(d_word) * k <= len(word):
                counter += 1

    return counter


def text_preparation(text):
    # Removes nikud from text
    text = re.sub(r'[\u0591-\u05BD\u05BF-\u05C2\u05C4-\u05C7]', '', text)
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    # text = text.replace('"', ' ')
    return text


def create_sentence_array(text) -> List[str]:
    text = text_preparation(text)
    return tokenize.sent_tokenize(text)


def create_words_array(text) -> List[str]:
    text = text_preparation(text)
    # remove punctuation from text
    words = list(dict.fromkeys(re.sub(r'[^\w\d\s\'\"\-]+', '', text).split()))
    # remove one-letter words and connectors
    words = list(word for word in words if len(word) > 1 and word not in connectors_list)
    return words


def create_paragraph_array(text) -> List[str]:
    text = text_preparation(text)
    return text.split("\n")


def count_word_from_paragraphs(word, paragraphs):
    count = 0
    for paragraph in paragraphs:
        # Removes side symbols
        paragraph = re.sub(r'[^\w\d\s\'\"\-]+', '', paragraph)
        if word in paragraph:
            count += 1
    return count
