import time
import threading

from src.svd import *
from src.tf_idf import *
from src.abstractor import *
from src.utils.visualization import *

TXT_FILE_PATH = "test_text.txt"
model: gensim.models.fasttext.FastText


def thread_load_model():
    global model
    print("Loading model,")
    model = load_model()
    print("Model loaded successfully.")


def main():
    global model
    th = threading.Thread(target=thread_load_model)
    th.start()

    # Read input text
    with open(TXT_FILE_PATH, "r", encoding="UTF-8") as f:
        test_text = f.read()

    # Perform Singular Value Decomposition
    tf = create_tf_table(test_text)
    idf = create_idf_table(test_text)
    svd = create_svd_table(tf, idf)

    # Retrieve key words and sentences
    key_words = get_key_words(svd, 5)
    key_sentences = get_key_sentences(svd, key_words, 3)

    # Order sentences for abstraction
    sentences = order_sentences(test_text, key_sentences)

    # Wait for model to load
    th.join()

    # Abstract sentences
    summary = add_connectors(sentences)

    print("Keywords:{}\n".format(key_words))
    print(summary)


def add_connectors(sentences):
    split_sentences = list(sent.split() for sent in sentences)
    for sent in split_sentences:
        connector = get_most_similar_connector(model, sent[0])
        if sent[0] != connector:
            sent.insert(0, connector)

    return list(' '.join(sent) for sent in split_sentences)


def order_sentences(text, key_sentences) -> List[str]:
    text_sentences = tokenize.sent_tokenize(text)
    sentences = []
    for sent in text_sentences:
        if sent in key_sentences:
            sentences.append(sent)
    return sentences


def print_svd(svd):
    print("\n\nSVD TABLE: \n")
    [print(key, value) for key, value in svd.items()]


def print_idf(idf):
    print("\n\nIDF TABLE: \n")
    [print(key, ': %.3f' % value) for key, value in idf.items()]


def print_tf(tf):
    print("\n\nTF TABLE: \n")
    [print(key, value) for key, value in tf.items()]


if __name__ == "__main__":
    main()
