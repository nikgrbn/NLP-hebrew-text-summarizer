from typing import List

import gensim
from gensim.models import FastText
from gensim.models.fasttext import load_facebook_model
from gensim.test.utils import datapath


MODEL_PATH = "model\\cc.he.100.bin"


def load_model() -> gensim.models.fasttext.FastText:
    fb_model = load_facebook_model(MODEL_PATH)
    return fb_model


def get_most_similar_connector(model: gensim.models.fasttext.FastText, word: str, connectors_list: List[str]) -> str:
    res = model.wv.most_similar_to_given(word, connectors_list)
    return res


def get_connectors_list_by_key_words(model: gensim.models.fasttext.FastText,
                                     key_words: List[str], connectors_list: List[str]):
    arr: dict[str, int] = {}

    for k_word in key_words:
        # Get list of most similar connectors to each key word
        nearest_arr: List[str] = []
        tmp_list = list(connectors_list)  # Shallow copy con. list
        for i in range(10):
            word = get_most_similar_connector(model, k_word, tmp_list)
            nearest_arr.append(word)
            tmp_list.remove(word)

        # Add for each connector occurrence
        for con in nearest_arr:
            if con in arr:
                arr[con] += 1
            else:
                arr[con] = 1

    return sorted(arr.items(), key=lambda item: item[1], reverse=True)
