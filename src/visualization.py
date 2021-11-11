import numpy as np
import matplotlib.pyplot as plt


def visualize_tf_idf(tf_idf_table):
    columns = list(tf_idf_table.keys())
    rows = list(list(tf_idf_table.values())[0].keys())

    print(columns)
    print(rows)



