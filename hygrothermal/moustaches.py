
a = np.array([lambda_0_samples, lambda_m_samples, lambda_t_samples, cp_samples,
              dp_p1_samples, dp_p2_samples, xi_p1_samples, xi_p2_samples, xi_p3_samples])
b = a[:,6500:]

VRAI = np.array([0.05, 0.5, 1e-4, 2000, 5e-11, 1e-10, 17, 19, 47])

CMA = np.array([0.04872, 0.514, 1.029e-4, 1963.148, 5.16e-11, 9.947e-11,
                20.703, 18.844, 50.068])


CMA_norm = CMA/VRAI
BAY_norm = a / np.column_stack([VRAI]*10000)

MAP = a.mean(axis=1)

plt.boxplot(BAY_norm.T)
plt.plot(np.arange(1,10),CMA_norm, 'ro')