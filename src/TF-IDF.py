import re
import math
import nltk

nltk.download('punkt')
from nltk import tokenize


def create_TF_table(text):
    # Create 'Term-Frequency' table
    sentences = create_sentence_array(text)
    TF_table = dict()

    for sentence in sentences:
        words = create_words_array(sentence)

        for word in words:
            count = words.count(word)
            TF_table[word] = count / len(words)
    
    return TF_table


def create_IDF_table(text):
    # Create 'Inverse Document Frequency' table
    sentences = create_sentence_array(text)
    words = create_words_array(text)
    num_sentences = len(sentences)

    IDF_table = dict()
    for i in range(len(words)):
        #create element with the word and the IDF equation with log
        #number of sectences divide the numbers of sentences that include specific word from the text words
        num_sentences_word_include = count_word_from_sentences(words[i], sentences)
        IDF_equation = math.log(len(sentences) / num_sentences_word_include)
        IDF_table[words[i]] = IDF_equation
    return IDF_table


def create_sentence_array(text):
    return tokenize.sent_tokenize(text)

def create_words_array(text):
    #remove punctuation from text
    return re.sub(r'[^\w\d\s\'\-]+','', text).split()


def count_word_from_sentences(word, sentences):
    count = 0
    for i in range(len(sentences)):
        if word in sentences[i]:
            count += 1
            
    return count


test_text = "Fyodor Mikhailovich Dostoevsky. Sometimes transliterated as Dostoyevsky, was a Russian novelist, short story writer, essayist, and journalist. Dostoevsky's literary works explore human psychology in the troubled political, social, and spiritual atmospheres of 19th-century Russia, and engage with a variety of philosophical and religious themes. His most acclaimed novels include Crime and Punishment (1866), The Idiot (1869), Demons (1872), and The Brothers Karamazov (1880). Dostoevsky's body of works consists of 12 novels, four novellas, 16 short stories, and numerous other works. Many literary critics rate him as one of the greatest novelists in all of world literature, as multiple of his works are considered highly influential masterpieces. [4] His 1864 novella Notes from Underground is considered to be one of the first works of existentialist literature. As such, he is looked upon as a philosopher and theologian as well"

print("\n\nIDF TABLE: \n")
[print(key,': %.3f' % value) for key, value in create_IDF_table(test_text).items()]

print("\n\nTF TABLE: \n")
[print(key,': %.3f' % value) for key, value in create_TF_table(test_text).items()]
