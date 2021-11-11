import numpy as np
import matplotlib.pyplot as plt
from bidi import algorithm as bidi_alg
import textwrap


def visualize_tf_idf(tf_idf_table):
    # Divide tf-idf to rows, columns, values
    rows = list(key for key in tf_idf_table.keys())
    columns = []
    for column in list(col[::-1] for col in list(tf_idf_table.values())[0].keys()):
        columns.append(textwrap.fill(column, 15))

    cell_values: list[list[float]] = []
    for row in rows:
        cell_values.append(list('%.4f' % val for val in tf_idf_table[row[::-1]].values()))

    fig, ax = plt.subplots()

    # Hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    # Create table
    table = ax.table(cellText=cell_values, rowLabels=rows, colLabels=columns, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)

    fig.tight_layout()
    plt.savefig('foo.pdf', bbox_inches='tight')




