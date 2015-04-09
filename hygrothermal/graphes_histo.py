
from matplotlib import rc
rc("font", family="serif", size=20)
rc("text", usetex=True)

x = R.trace('lambda_0')[6500:]
name_on_graph = r'$k_0$'
name_on_file = 'lambda_0'
value_real = 0.05
value_CMA = 0.04872

import pandas
foo = pandas.read_csv('resultats_benchmark.txt', delimiter = '\t')
N = len(foo)

weights = np.ones_like(x)/len(x)
import pylab as plt

# Graphes
plt.hist(x, weights = weights, bins = 10,
         color = '#777777', edgecolor = '#000000')
plt.plot([value_real]*2, [0, 1], 'r-', linewidth = 1.5, linestyle = 'dashed')
plt.plot([value_CMA]*2, [0, 1], 'b-', linewidth = 1.5)

# Axes
plt.xlabel(name_on_graph)
#plt.xticks((0.0485, 0.049, 0.0495, 0.050))
plt.xlim([0.045, 0.055])
plt.ylim([0, 0.62])

ax = plt.gca()
ax.xaxis.get_major_formatter().set_powerlimits((-2, 4))

"""
x_formatter = mticker.ScalarFormatter(useOffset=False)
x_formatter.set_scientific(True)
ax.xaxis.set_major_formatter(x_formatter)
"""

#fig = plt.gcf()
#fig.savefig('graph_'+name_on_file+'.pdf', format='pdf', bbox_inches='tight')
#fig.savefig('graph_'+name_in_file+'.png', format='png', bbox_inches='tight', dpi=300)
