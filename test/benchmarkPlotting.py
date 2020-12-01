import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from statistics import mean, stdev


def round2(x):
    return round(x, 2)

# ############################# fig 1
s1PAA = [
    0.024217605590820312,
    0.0272371768951416,
    0.027811288833618164,
    0.029182910919189453,
    0.0264585018157959
]
s1PA = [
    0.10976934432983398,
    0.11318039894104004,
    0.11037588119506836,
    0.11297416687011719,
    0.10670232772827148
]
s1PC = [
    0.7940895557403564,
    0.7615773677825928,
    0.8705184459686279,
    0.8336830139160156,
    0.7870488166809082
]
s1FA = [
    2.789379358291626,
    2.6724846363067627,
    2.6838324069976807,
    2.7036166191101074,
    2.801419496536255
]
##########
s2PAA = [
    0.5495929718017578,
    0.566368579864502,
    0.5576992034912109,
    0.5620498657226562,
    0.5746228694915771
]
s2PA = [
    0.6063697338104248,
    0.5941851139068604,
    0.6079471111297607,
    0.6099033355712891,
    0.5959274768829346
]
s2PC = [
    0.9184565544128418,
    0.931067943572998,
    0.9142539501190186,
    0.9278504848480225,
    0.9280312061309814
]
s2FA = [
    2.9767096042633057,
    2.7801096439361572,
    2.8027851581573486,
    2.857680559158325,
    2.842818021774292
]


labels = ["PAA", "PA", "PC", "FA"]
s1Means = list(map(round2, [mean(s1PAA), mean(s1PA), mean(s1PC), mean(s1FA)]))
s2Means = list(map(round2, [mean(s2PAA), mean(s2PA), mean(s2PC), mean(s2FA)]))
s1Stds = list(map(round2, [stdev(s1PAA), stdev(s1PA), stdev(s1PC), stdev(s1FA)]))
s2Stds = list(map(round2, [stdev(s2PAA), stdev(s2PA), stdev(s2PC), stdev(s2FA)]))

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, s1Means, width, label='Schema 1', yerr=s1Stds, align='center')
rects2 = ax.bar(x + width/2, s2Means, width, label='Schema 2', yerr=s2Stds, align='center')

ax.set_ylabel('Time cost/s')
ax.set_title('Time cost for positioning data query: 5 tags for 3 days')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.text(-0.45, 2.25, "Num of records fetched:\nPAA: 4808   PA: 23786\nPC: 196334 FA: 943203",
        bbox={'facecolor': 'white', 'alpha': 0.2, 'pad': 5})
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 10),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.show()


# longer period: 2 weeks from 2 weeks data - 5 tags
# s1: [19.26, 13.91]
# s2: [19.34, 18.96]
# raw: 17.8




############################# fig 2
# s1time = [
#     18.61064887046814,
#     19.0884370803833,
#     20.3336820602417,
#     17.98045825958252,
#     20.309824466705322
# ]
#
# s2time = [
#     19.40457844734192,
#     19.57641577720642,
#     19.013787984848022,
#     19.298017740249634,
#     19.397727012634277
# ]
# #
# # labels = ["Time cost", "Space cost"]
# s1space = 13.91
# s2space = 18.96
# rawspace = 17.80
# s1m = [round2(mean(s1time)), s1space]
# s2m = [round2(mean(s2time)), s2space]
# s1t = [round2(stdev(s1time)), 0]
# s2t = [round2(stdev(s2time)), 0]
#
# print(s1m)
# print(s2m)
# print(rawspace)

#
# x = np.arange(len(labels))  # the label locations
# width = 0.35  # the width of the bars
#
# fig, ax = plt.subplots()
# rects1 = ax.bar(x - width/2, s1m, width, label='Schema 1', yerr=s1t, align='center')
# rects2 = ax.bar(x + width/2, s2m, width, label='Schema 2', yerr=s2t, align='center')
#
# ax.set_ylabel('Time cost/s')
# ax.set_title('Time cost for positioning data query: 2 weeks')
# ax.set_xticks(x)
# ax.set_xticklabels(labels)
# ax.legend()
# ax.text(-0.45, 2.25, "Num of records fetched:\nPAA: 4808   PA: 23786\nPC: 196334 FA: 943203",
#         bbox={'facecolor': 'white', 'alpha': 0.2, 'pad': 5})
# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(height),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 10),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')
#
# autolabel(rects1)
# autolabel(rects2)
#
# fig.tight_layout()
#
# plt.show()

