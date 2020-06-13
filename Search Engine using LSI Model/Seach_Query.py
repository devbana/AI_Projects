
from numpy import *
from numpy import dot
from numpy.linalg import norm
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


def cosine_distance(a, b):
    return 1 - cosine_similarity(a,b)


def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))


def find_end_points(point, angle, length):
    # unpack the first point
    x, y = point

    # find the end point
    endy = length * math.sin(math.radians(angle))
    endx = length * math.cos(math.radians(angle))

    # plot the points
    # fig = plt.figure()
    # ax = plt.subplot(111)

    return ([x, endx], [y, endy])
    # ax.plot([x, endx], [y, endy])

    # return fig


column_header = ['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10']
row_header = ['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10']
doc_term = array([
    # D0   D1   D2   D3   D4   D5   D6   D7   D8   D9   D10  D11
    [0.1, 0.1, 0.0, 0.1, 0.2, 0.0, 0.1, 0.9, 0.9, 0.3, 0.0, 0.8],
    [0.1, 0.1, 0.0, 0.1, 0.0, 0.0, 0.1, 0.9, 0.0, 0.3, 0.0, 0.8],
    [0.0, 0.0, 0.9, 0.0, 0.3, 0.1, 0.7, 0.0, 0.2, 0.7, 0.5, 0.5],
    [0.0, 0.0, 0.9, 0.1, 0.0, 0.1, 0.9, 0.3, 0.8, 0.4, 0.1, 0.4],
    [0.0, 0.0, 0.0, 0.0, 0.5, 0.9, 0.3, 0.7, 0.4, 0.6, 0.0, 0.3],
    [0.5, 0.6, 0.0, 0.7, 0.3, 0.3, 0.9, 0.1, 0.0, 0.0, 0.0, 0.3],
    [0.0, 0.0, 0.8, 0.0, 0.6, 0.6, 0.0, 0.1, 0.4, 0.9, 0.3, 0.1],
    [0.35, 0.4, 0.0, 0.5, 0.5, 0.1, 0.7, 0.1, 0.5, 0.3, 0.8, 0.1],
    [0.3, 0.3, 0.0, 0.2, 0.8, 0.7, 0.7, 0.8, 0.0, 0.6, 0.8, 0.0],
    [0.0, 0.0, 0.5, 0.0, 0.2, 0.0, 0.0, 0.1, 0.0, 0.4, 0.5, 0.3]
])

cos_similarity_list = []
pd_cols_cos_similarity = []
cos_distance_list = []
pd_cols_cos_distance = []

for i in range(0, 11):
    for j in range(0, 11):
        cos_value = cosine_similarity(transpose(doc_term[:, [i]]), doc_term[:, [j]])
        cos_distance = 1.0 - cos_value
        cos_distance_list.append(asscalar(around(cos_distance, decimals=3)))
        cos_similarity_list.append(
            asscalar(around(math.degrees(math.acos(min(max(cos_value, -1.0), 1.0))), decimals=1)))
    pd_cols_cos_similarity.append(cos_similarity_list)
    pd_cols_cos_distance.append(cos_distance_list)

    cos_similarity_list = []
    cos_distance_list = []

df_cos_sim = pd.DataFrame(pd_cols_cos_similarity, columns=column_header, index=row_header)
print(df_cos_sim)

df_cos_dist = pd.DataFrame(pd_cols_cos_distance, columns=column_header, index=row_header)
print(df_cos_dist)

fig = plt.figure()
ax = plt.subplot(111)
ax.set_ylim([0, 1.75])
ax.set_xlim([0, 1.75])

ref_doc = 0
for i in range(0, 11):
    X, Y = find_end_points([0, 0], df_cos_sim.iloc[ref_doc][i], norm(doc_term[:, [i]]))
    ax.plot(X, Y)
    ax.annotate("", xy=(X[1], Y[1]), xytext=(0, 0), arrowprops=dict(arrowstyle="->"))
    ax.text(X[1], Y[1], "D" + str(ref_doc) + "-" + "D" + str(i) + "-(" + str(df_cos_sim.iloc[ref_doc][i]) + u"\u00b0" + ")")
fig.show()
query = "D" + str(ref_doc)
rank_order = df_cos_sim.sort_values(query)
print("\n\nDocument Rank for the query ", query)
print(rank_order[query])