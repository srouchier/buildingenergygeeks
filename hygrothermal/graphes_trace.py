
from matplotlib import rc
rc("font", family="serif", size=20)
rc("text", usetex=True)


# Graphes
plt.plot(xi_p1_samples, 'k-', linewidth=1.5)

# Axes
plt.xlabel('Samples')
plt.ylabel(r'$\xi_{25\%}$')

#plt.xlim([0.045, 0.055])
#plt.ylim([4e-11, 5.5e-11])


fig = plt.gcf()
fig.savefig('graph_xi_p1_trace.pdf', format='pdf', bbox_inches='tight')
#fig.savefig('graph_'+name_in_file+'.png', format='png', bbox_inches='tight', dpi=300)
