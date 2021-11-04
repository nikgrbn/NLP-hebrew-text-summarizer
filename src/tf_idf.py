import re
import math
import nltk
from nltk import tokenize


def create_tf_table(text):
    # Create 'Term-Frequency' table
    sentences = create_sentence_array(text)
    words = list(dict.fromkeys(create_words_array(text)))

    tf_table = dict()
    for word in words:
        sentence_to_value = dict()
        for sentence in sentences:
            words_in_sentence = create_words_array(sentence)
            sentence_to_value[sentence] = words_in_sentence.count(word) / len(words_in_sentence)
        tf_table[word] = sentence_to_value

    return tf_table


def create_idf_table(text):
    # Create 'Inverse Document Frequency' table
    sentences = create_sentence_array(text)
    words = create_words_array(text)

    IDF_table = dict()
    for i in range(len(words)):
        # create element with the word and the IDF equation with log
        # number of sentences divide the numbers of sentences that include specific word from the text words
        num_sentences_word_include = count_word_from_sentences(words[i], sentences)
        IDF_equation = math.log(len(sentences) / num_sentences_word_include)
        IDF_table[words[i]] = IDF_equation
    return IDF_table


def create_sentence_array(text):
    return tokenize.sent_tokenize(text)


def create_words_array(text):
    # remove punctuation from text
    return re.sub(r'[^\w\d\s\'\-]+', '', text).split()


def count_word_from_sentences(word, sentences):
    count = 0
    for i in range(len(sentences)):
        if word in sentences[i]:
            count += 1

    return count
