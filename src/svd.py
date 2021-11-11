def create_svd_table(tf_table, idf_table):
    #Use singular value decomposition to create tf-idf table
    svd_table = dict()

    for key, value in tf_table.items():
        word_value_sentences = dict()
        for sentence, word_value in value.items():
            svd_calculate = word_value * idf_table[key]
            word_value_sentences[sentence] = svd_calculate

        svd_table[key] = word_value_sentences

    return svd_table
