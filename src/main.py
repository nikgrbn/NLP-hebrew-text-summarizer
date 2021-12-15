from src.svd import *
from src.tf_idf import *
from src.utils.visualization import *

TXT_FILE_PATH = "test_text.txt"


def main():
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

    print(key_words)
    print(key_sentences)


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
