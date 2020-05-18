import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams
from matplotlib import rc

from scipy import stats

# parameters
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rc('text', usetex=True)

font_size = 30
axis_label_size = 45
arrow_size = 1
markers_left = [""]
markers_center = [""]
markers_bottom = ["L2212A"]
markers_va_center = [""]


def place_marker_label(ax, label, pos_x, pos_y, size, color, args):
    ha = 'left'
    va = 'bottom'
    if label in markers_left:
        ha = 'right'
    if label in markers_center:
        ha = 'center'
    if label in markers_bottom:
        va = 'top'
    if label in markers_va_center:
        va = 'center'
    ax.annotate(label, (pos_x, pos_y), fontsize=size, color=color, ha=ha, va=va)


# read in data
exp = pd.read_csv('spr_data_3e6.csv', header=None)
calc = pd.read_csv('energies_3e6.csv', header=None)

# sort using labels
exp.sort_values(by=[exp.columns[0]], inplace=True)
calc.sort_values(by=[calc.columns[0]], inplace=True)

# merge tables on labels
data = exp.merge(calc, how='inner', on=[calc.columns[0]])

labels = list(data[data.columns[0]])

# experimental
x = list(data[data.columns[1]])
# predicted
y = list(data[data.columns[2]])

fig = plt.figure(figsize=(24, 18))
ax = fig.add_subplot(111)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.scatter(x, y)

# slope, intercept, rp_value, pp_value, std_err = stats.linregress(y, x)
# rs_value, ps_value = stats.spearmanr(y, x)

arrow_length = arrow_size * 0.15
arrow_head_length = arrow_size * 0.05
arrow_head_size = arrow_size * 0.2

# set graph limits
xcut = 3
plt.xlim(-1, xcut)
plt.ylim(min(y) - 2, max(y) + 5)

for l, p0, p1 in zip(labels, x, y):
    place_marker_label(ax, l, p0, p1, font_size, 'black', None)

    # add arrows for values off the graph
    if p0 > xcut:
        ax.arrow(xcut - arrow_length - arrow_head_length, p1, arrow_length, 0, head_width=arrow_head_size,
                 head_length=arrow_head_length, color='black')
        place_marker_label(ax, l, xcut - arrow_length - arrow_head_length, p1, font_size, 'black', None)

# set font size of axis
plt.tick_params(axis='both', which='major', labelsize=font_size)
plt.xlabel("changes in binding energy, experimental($\\triangle\\triangle$G in kcal/mol)", fontsize=axis_label_size)
plt.ylabel("changes in binding energy, predicted($\\triangle\\triangle$G in kcal/mol)", fontsize=axis_label_size)


# plt.show()
plt.savefig('3e6_plot_v2.png')
