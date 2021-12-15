import re
import math
from src.connectors_dataset import connectors_list
import nltk
from nltk import tokenize


def create_tf_table(text):
    # Create 'Term-Frequency' table
    sentences = create_sentence_array(text)
    words = create_words_array(text)

    tf_table = dict()
    for word in words:
        sentence_to_value = dict()
        for sentence in sentences:
            words_in_sentence = create_words_array(sentence)
            sentence_to_value[sentence] = sentence.count(word) / len(words_in_sentence)
        tf_table[word] = sentence_to_value

    return tf_table


def create_idf_table(text):
    # Create 'Inverse Document Frequency' table
    sentences = create_sentence_array(text)
    words = create_words_array(text)

    idf_table = dict()
    for i in range(len(words)):
        # create element with the word and the IDF equation with log
        # number of sentences divide the numbers of sentences that include specific word from the text words
        num_sentences_word_include = count_word_from_sentences(words[i], sentences)
        idf_equation = math.log(len(sentences) / num_sentences_word_include)
        idf_table[words[i]] = idf_equation
    return idf_table


def text_preparation(text):
    text = re.sub(r'[\u0591-\u05BD\u05BF-\u05C2\u05C4-\u05C7]', '', text)
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = text.replace('"', ' ')
    return text


def create_sentence_array(text):
    text = text_preparation(text)
    return tokenize.sent_tokenize(text)


def create_words_array(text):
    text = text_preparation(text)
    # remove punctuation from text
    words = list(dict.fromkeys(re.sub(r'[^\w\d\s\'\"\-]+', '', text).split()))
    words = remove_connectors(words)
    return words


def remove_connectors(words):
    updated_words = words
    for word in updated_words:
        if word in connectors_list:
            updated_words.remove(word)
    return updated_words


def count_word_from_sentences(word, sentences):
    count = 0
    for i in range(len(sentences)):
        if word in sentences[i]:
            count += 1

    return count
