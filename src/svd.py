import functools
from typing import Dict, List
from src.tf_idf import *


def create_svd_table(tf_table, idf_table) -> Dict[str, Dict[str, float]]:
    # Use singular value decomposition to create tf-idf table
    svd_table: Dict[str, Dict[str, float]] = dict()

    for key, value in tqdm(tf_table.items()):
        word_value_sentences = dict()
        for sentence, word_value in value.items():
            svd_calculate = word_value * idf_table[key]
            word_value_sentences[sentence] = svd_calculate

        svd_table[key] = word_value_sentences

    return svd_table


def get_key_words(svd_table: Dict[str, Dict[str, float]], num_words: int = 3) -> List[str]:
    list_len = num_words if len(svd_table) > num_words else len(svd_table)
    sorted_svd = sorted(svd_table.items(), key=lambda item: sum(item[1].values()), reverse=True)

    words_list = list()
    i = 0
    while len(words_list) < list_len:
        word = sorted_svd[i][0]
        flag = True
        # Check if word is connector
        if word not in connectors_list:

            # Check if copy of the word already in keywords
            for inc_w in words_list:

                # Check if difference between two words is minimal
                if word in inc_w or inc_w in word:
                    if abs(len(word) - len(inc_w)) <= 2:
                        flag = False
                        break

            if flag:
                words_list.append(word)
        i += 1

    return words_list


def get_key_sentences(svd_table: Dict[str, Dict[str, float]], key_words: List[str], num_sentences: int = 3) -> List[str]:
    sentences_to_value = dict()
    for key_word in key_words:
        sentences_to_value = {k: sentences_to_value.get(k, 0) + svd_table[key_word].get(k, 0)
                              for k in set(sentences_to_value) | set(svd_table[key_word])}
    sentences_to_value = dict(sorted(sentences_to_value.items(), key=lambda item: item[1], reverse=True))
    return list(sentences_to_value.keys())[:num_sentences]
