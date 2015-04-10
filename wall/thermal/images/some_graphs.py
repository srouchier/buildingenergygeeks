
"""
Quelques graphes qui apparaissent sur le wordpress mais pas dans les notebooks
"""

ax = plt.subplot(121)

plt.plot(time_file, u_file, '-k')

plt.xlabel("Time (s)")


plt.hist(lambda_1_samples, histtype='stepfilled', bins=30, alpha=0.85,
         label="posterior of $\lambda_1$", color="#A60628", normed=True)


plt.legend(loc="upper left")
plt.title(r"""Posterior distributions of the variables
    $\lambda_1,\;\lambda_2,\;\tau$""")
plt.xlim([15, 30])
