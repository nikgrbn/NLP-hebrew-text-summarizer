import gensim
from gensim.models import FastText
from gensim.models.fasttext import load_facebook_model
from gensim.test.utils import datapath
from src.model.model_connectors import model_connectors

MODEL_PATH = "model\\cc.he.100.bin"


def load_model() -> gensim.models.fasttext.FastText:
    fb_model = load_facebook_model(MODEL_PATH)
    return fb_model


def get_most_similar_connector(model: gensim.models.fasttext.FastText, word: str) -> str:
    res = model.wv.most_similar_to_given(word, model_connectors)
    return res
