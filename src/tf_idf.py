import re
import math
from typing import Dict, List
from src.connectors_dataset import connectors_list
import nltk
from nltk import tokenize
from tqdm import tqdm


def create_tf_table(text: str):
    # Create 'Term-Frequency' table
    sentences = create_sentence_array(text)
    words = create_words_array(text)

    tf_table = dict()
    for word in tqdm(words):
        sentence_to_value = dict()
        for sentence in sentences:
            words_in_sentence = create_words_array(sentence)
            if words_in_sentence:  #check if the list is empty
                sentence_to_value[sentence] = count_words_in_doc(word, sentence) / len(words_in_sentence)
        tf_table[word] = sentence_to_value

    return tf_table


def create_idf_table(text: str):
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


def text_preparation(text: str):
    # Removes nikud from text
    text = re.sub(r'[\u0591-\u05BD\u05BF-\u05C2\u05C4-\u05C7]', '', text)
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    # text = text.replace('"', ' ')
    return text


def count_words_in_doc(word: str, document: str):
    k = 0.5
    volume_count = 0
    include_words_list = list()

    for inside_word in document:
        if word in inside_word:
            if word is inside_word:
                volume_count += 1
            else:
                include_words_list.append(inside_word)

    # Check if including word is a variation of same word or different one
    for included_word in include_words_list:
        if len(included_word) * k <= len(word):
            volume_count += 1

    return volume_count


def create_sentence_array(text) -> List[str]:
    text = text_preparation(text)
    return tokenize.sent_tokenize(text)


def create_words_array(text) -> List[str]:
    text = text_preparation(text)
    # remove punctuation from text
    words = list(dict.fromkeys(re.sub(r'[^\w\d\s\'\"\-]+', '', text).split()))
    words = remove_connectors(words)
    words = list(word for word in words if len(word) > 1)
    return words


def create_paragraph_array(text) -> List[str]:
    text = text_preparation(text)
    return text.split("\n")


def remove_connectors(words) -> List[str]:
    updated_words = words
    for word in updated_words:
        if word in connectors_list:
            updated_words.remove(word)
    return updated_words


def count_word_from_paragraphs(word, paragraphs) -> int:
    count = 0
    for paragraph in paragraphs:
        # Removes side symbols
        paragraph = re.sub(r'[^\w\d\s\'\"\-]+', '', paragraph)
        if word in paragraph:
            count += 1
    return count
