import gensim
from gensim.models import FastText
from gensim.models.fasttext import load_facebook_model
from gensim.test.utils import datapath

MODEL_PATH = "model\\cc.he.100.bin"


def load_model() -> gensim.models.fasttext.FastText:
    fb_model = load_facebook_model(MODEL_PATH)
    return fb_model


def get_most_similar_connector(model: gensim.models.fasttext.FastText, word: str, connectors_list) -> str:
    res = model.wv.most_similar_to_given(word, connectors_list)
    return res
