# import numpy as np
# import seaborn as sb
# import pandas as pd
# import matplotlib as matplotlib
# import matplotlib.colors as mc
# import matplotlib.pyplot as plt
#
# data = np.random.rand(4, 4)
# sorted_version_labels = ["1.0.1", "1.1.1", "1.1.3", "1.2.0"]
# df = pd.DataFrame(data, columns=sorted_version_labels)
#
# def NonLinCdict(steps, hexcol_array):
#     cdict = {'red': (), 'green': (), 'blue': ()}
#     for s, hexcol in zip(steps, hexcol_array):
#         rgb = matplotlib.colors.hex2color(hexcol)
#         cdict['red'] = cdict['red'] + ((s, rgb[0], rgb[0]),)
#         cdict['green'] = cdict['green'] + ((s, rgb[1], rgb[1]),)
#         cdict['blue'] = cdict['blue'] + ((s, rgb[2], rgb[2]),)
#     return cdict
#
# hc = ["White", "Cyan", "lime", "Yellow", "Red"]
# th = [0, 0.25, 0.5, 0.75, 1.0]
#
# cdict = NonLinCdict(th, hc)
# cm = mc.LinearSegmentedColormap('test', cdict)
#
# heat_map = sb.heatmap(data, xticklabels=sorted_version_labels, yticklabels=list(reversed(sorted_version_labels)), vmin=0, vmax=1.0, cmap=cm, cbar_kws = dict(use_gridspec=False,location="bottom"))
# plt.show()

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import json

fileObject = open("data.json", "r")
jsonContent = fileObject.read()
parsed_version_info = json.loads(jsonContent)

for key, value in parsed_version_info.items():
    parsed_version_info[key] = int(value)

versions = parsed_version_info.keys()
locs = parsed_version_info.values()

y_pos = np.arange(len(versions))

col = []
for v in versions:
    if v.startswith('1.'):
        col.append('Blue')
    elif v.startswith('2.'):
        col.append('Purple')
    else:
        col.append('Orange')

plt.bar(y_pos, locs, color=col)
plt.xticks(y_pos, versions)
plt.ylabel('LOC')
plt.xlabel('jQuery version')
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
plt.show()

# from matplotlib import pyplot as plt
# import numpy as np
#
# # prepare the data
# data = np.arange((100))
# data = np.reshape(data, (10,10))
# num_columns = 10
# datas = []
# for i in range(0, num_columns):
#     datas.append(data[i:i+1, :])
# data1=data[0:5,:]
# data2=data[5:10,:]
#
# # create the figure and a single axis
# fig, ax = plt.subplots()
#
# # common arguments to imshow
# kwargs = dict(
#         origin='lower', interpolation='nearest', vmin=np.amin(data),
#         vmax=np.amax(data), aspect='auto')
#
# # i = 0
# # for d in datas:
# #     ax.imshow(d, extent=[i, i+1, i, i+1], **kwargs)
# #     ax.axhline(i, color='k')
# #     ax.axvline(i, color='k')
# #     i = i + 1
# # draw the data
# # ax.imshow(data1, extent=[0, 10, 0, 5], **kwargs)
# # ax.imshow(data2, extent=[0, 10, 5, 7.5], **kwargs)
# ax.imshow(data1, extent=[0, 7.5, 0, 7.5], **kwargs)
# ax.imshow(data2, extent=[7.5, 10, 0, 7.5], **kwargs)
#
# # optional black line between data1 and data2
# ax.axhline(5, color='k')
#
# # set the axis limits
# ax.set_ylim(0, 7.5)
# ax.set_xlim(0, 10)
#
# # set the xticklabels
# xticks = np.arange(0,10)
# ax.set_xticks(xticks + 0.5)
# ax.set_xticklabels(map(str, xticks))
#
# # set the yticks and labels
# yticks = np.concatenate((
#         np.arange(0, 5) + 0.5,
#         np.arange(5, 7.5, 0.5) + 0.25
#         ))
# ax.set_yticks(yticks)
# ax.set_yticklabels(map(str, xticks))
#
# # show the figure
# plt.show()