
"""
Code for plotting the graphs displayed in the notebook
"""

from matplotlib import rc
rc("font", family="serif", size=14)

import pandas
data_ = pandas.read_csv('../input_file.txt', delimiter='\t')
time_ = np.array(data_['t (s)'])
T1    = np.array(data_['T(e/4)'])
T2    = np.array(data_['T(e/2)'])
T3    = np.array(data_['T(3e/4)'])
u     = np.array(data_['U (W/m2)'])

# Plotting the measurements of u and T


figsize(13, 4)

ax = plt.subplot(121)

plt.plot(time_, T1, linewidth=2)
plt.plot(time_, T2, linewidth=2)
plt.plot(time_, T3, linewidth=2)

plt.xlabel("Time (s)")
plt.ylabel(r"Temperature ($^\circ$C)")
plt.xticks([0, 2000, 4000, 6000, 8000])
plt.ylim([-1, 40])
plt.legend(('T(e/4)', 'T(e/2)', 'T(3e/4)'),loc="lower right")

ax = plt.subplot(122)

plt.plot(time_, u, '-k', linewidth = 2)
plt.xlabel("Time (s)")
plt.ylabel(r"Heat flow (W/m$^2$)")
plt.legend(loc="upper right")
plt.xticks([0, 2000, 4000, 6000, 8000])
plt.ylim([-50, 1600])


fig = plt.gcf()
fig.savefig('input_output.png', format='png', dpi = 300)
