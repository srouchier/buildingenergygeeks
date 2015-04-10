
"""
Quelques graphes qui apparaissent sur le wordpress mais pas dans les notebooks
"""

#%%
from matplotlib import rc
rc("font", family="serif", size=14)

#%%
""" Pour tracer u et T """

figsize(10, 4)

ax = plt.subplot(121)

plt.plot(time_file, u_file, '-k')
plt.xlabel("Time (s)")
plt.ylabel(r"Heat flow (W/m$^2$)")
plt.legend(loc="upper right")
plt.xticks([0, 2000, 4000, 6000, 8000])
plt.ylim([-50, 1600])

ax = plt.subplot(122)

plt.plot(time_file, T_file, '-k')
plt.xlabel("Time (s)")
plt.ylabel("Temperature (C)")
plt.xticks([0, 2000, 4000, 6000, 8000])
plt.legend(loc="lower right")

fig = plt.gcf()
fig.savefig('fig_input_output.png', format='png', dpi = 300)

#%%
""" Pour tracer les priors """

figsize(10, 8)

ax = plt.subplot(221)

lambda_prior = np.random.uniform(0.1, 1, size = 10000)
plt.hist(lambda_prior, bins = 30, normed = True, color="#990022", alpha = 0.5,
         label = "Prior")
plt.plot([0.3, 0.3],[0, 2], 'k--', linewidth = 2, label = 'True')
plt.legend(loc = "lower right")
plt.xlabel(r'Thermal conductivity $k$')
plt.xlim([0, 1.1])
plt.ylim([0, 1.5])

ax = plt.subplot(222)

xc_prior = np.random.normal(0.025, 0.001, size = 10000)
plt.hist(xc_prior, bins = 30, normed = True, color="#77AA00", alpha = 0.5,
         label = "Prior")
plt.plot([0.025, 0.025],[0, 500], 'k--', linewidth = 2, label = 'True')
plt.legend(loc = "upper right")
plt.xlabel(r'Sensor position $x_c$')
plt.xticks([0.021, 0.023, 0.025, 0.027, 0.029])
plt.xlim([0.021, 0.029])
plt.ylim([0,450])

ax = plt.subplot(223)

sigmaT_prior = np.random.exponential(1, size = 10000)
plt.hist(sigmaT_prior, bins = 50, normed = True, color="#ffab00", alpha = 0.5,
         label = "Prior")
plt.plot([0.2, 0.2],[0, 1], 'k--', linewidth = 2, label = 'True')
plt.legend(loc = "upper right")
plt.xlabel(r'Temperature noise $\sigma_T$')
#plt.xticks([0.021, 0.023, 0.025, 0.027, 0.029])
plt.xlim([0, 3])
plt.ylim([0, 1])

ax = plt.subplot(224)

sigmaU_prior = np.random.uniform(0, 20, size = 10000)
plt.hist(sigmaU_prior, bins = 30, normed = True, color="#660099", alpha = 0.5,
         label = "Prior")
plt.plot([4, 4],[0, 1], 'k--', linewidth = 2, label = 'True')
plt.legend(loc = "lower right")
plt.xlabel(r'Heat flow noise $\sigma_u$')
#plt.xticks([0.021, 0.023, 0.025, 0.027, 0.029])
plt.xlim([-1, 22])
plt.ylim([0, 0.06])

fig = plt.gcf()
fig.savefig('fig_priors.png', format='png', dpi = 300)

#%%
""" Pour tracer les posteriors """

figsize(10, 8)

ax = plt.subplot(221)

plt.hist(lambda_samples, bins = 20, normed = True, color="#990022", alpha = 0.5,
         label = "Post.")
plt.plot([0.3, 0.3],[0, 40], 'k--', linewidth = 2, label = 'True')
plt.legend(loc = "upper right")
plt.xlabel(r'Thermal conductivity $k$')
plt.xlim([0.25, 0.35])
plt.ylim([0, 40])

ax = plt.subplot(222)

plt.hist(xc_samples, bins = 20, normed = True, color="#77AA00", alpha = 0.5,
         label = "Post.")
plt.plot([0.025, 0.025],[0, 2500], 'k--', linewidth = 2, label = 'True')
plt.legend(loc = "upper right")
plt.xlabel(r'Sensor position $x_c$')
plt.xlim([0.024, 0.026])
plt.ylim([0, 2500])

ax = plt.subplot(223)

plt.hist(eps_T_samples, bins = 20, normed = True, color="#ffab00", alpha = 0.5,
         label = "Post.")
plt.plot([0.2, 0.2],[0, 18], 'k--', linewidth = 2, label = 'True')
plt.legend(loc = "upper right")
plt.xlabel(r'Temperature noise $\sigma_T$')
plt.xlim([0.15, 0.45])
plt.ylim([0, 18])

ax = plt.subplot(224)

plt.hist(eps_u_samples, bins = 20, normed = True, color="#660099", alpha = 0.5,
         label = "Post.")
plt.plot([10, 10], [0, 0.25], 'k--', linewidth = 2, label = 'True')
plt.legend(loc = "upper left")
plt.xlabel(r'Heat flow noise $\sigma_u$')
plt.xlim([8, 20])
plt.ylim([0, 0.25])

fig = plt.gcf()
fig.savefig('fig_posteriors.png', format='png', dpi = 300)

