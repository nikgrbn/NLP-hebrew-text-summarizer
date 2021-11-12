import numpy as np
import matplotlib.pyplot as plt


def visualize_tf_idf(tf_idf_table):
    # Divide tf-idf to rows, columns, values
    rows = list(key[::-1] for key in tf_idf_table.keys())
    columns = list('...%s' % col[10::-1] for col in list(tf_idf_table.values())[0].keys())
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

    # Save table as png
    fig.tight_layout()
    plt.savefig('utils/res/tf_idf_table.pdf', bbox_inches='tight')




