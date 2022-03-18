import time
import threading
from collections import OrderedDict

from src.model import model_connectors
from src.svd import *
from src.tf_idf import *
from src.abstractor import *
from src.utils.visualization import *


TXT_FILE_PATH = "test_text.txt"
model: gensim.models.fasttext.FastText


def thread_load_model():
    global model
    model = load_model()
    print("\nModel loaded successfully.")


# define the countdown func.
def countdown(stop):
    t = 0
    dc = 0
    while True:
        mins, secs = divmod(t, 60)
        timer = 'Loading model{:<4}- {:02d}:{:02d}'.format('.'*(dc % 4), mins, secs)
        print("\r" + timer, end="", flush=True)
        time.sleep(1)
        t += 1
        dc += 1

        if stop():
            break


def main():
    global model
    str_inp = input("Use abstraction in summary? (y/n): ")

    if str_inp == 'y':
        th_load = threading.Thread(target=thread_load_model)
        stop_timer = False
        th_timer = threading.Thread(target=countdown, args=(lambda: stop_timer,))
        th_load.start()
        th_timer.start()

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
    summary = order_sentences(test_text, key_sentences)

    if str_inp == 'y':
        # Wait for model to load
        th_load.join()
        stop_timer = True
        th_timer.join()

        # Abstract sentences
        summary = add_connectors_m1(summary)
        # summary = add_connectors_m2(summary, key_words)

    print("Keywords:{}\n".format(key_words))
    print(*summary, sep='\n')


def add_connectors_m1(sentences):
    split_sentences = list(sent.split() for sent in sentences)
    for n, sent in enumerate(split_sentences):
        cn = model_connectors.adding_connectors
        if n == 0:
            cn = model_connectors.opening_connectors
        elif n == len(split_sentences)-1:
            cn = model_connectors.ending_connectors
        connector = get_most_similar_connector(model, sent[0], cn)
        if sent[0] != connector:
            sent.insert(0, connector)

    return list(' '.join(sent) for sent in split_sentences)


def add_connectors_m2(sentences, key_words):
    # Get connectors list by key words
    all_cn_list = model_connectors.all_connectors
    res_cn_dict = OrderedDict(get_connectors_list_by_key_words(model, key_words, all_cn_list))
    print("Connectors:{}\n".format(res_cn_dict))

    # Insert connectors into sentences
    split_sentences = list(sent.split() for sent in sentences)
    res_cn_list = list(res_cn_dict.keys())
    for sent in split_sentences:
        if sent[0] != res_cn_list[0]:
            sent.insert(0, res_cn_list[0])
        res_cn_list.pop(0)

    return list(' '.join(sent) for sent in split_sentences)


def order_sentences(text, key_sentences) -> List[str]:
    text_sentences = tokenize.sent_tokenize(text)
    sentences = []
    for sent in text_sentences:
        if sent in key_sentences:
            sentences.append(sent)

    for sent in key_sentences:
        if sent not in sentences:
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
