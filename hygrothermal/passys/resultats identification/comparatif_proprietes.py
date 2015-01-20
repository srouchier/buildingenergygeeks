

from copy import deepcopy
import numpy as np
import pylab as P

from hamopy import ham_library as ham
from hamopy.materials.standard import wood_fibre

WF_carac = wood_fibre
WF_prior = deepcopy(wood_fibre)
WF_bestf = deepcopy(wood_fibre)
WF_solut = deepcopy(wood_fibre)


# Prior
WF_prior.set_capacity(cp_0 = 1250, cp_t = 11.271)
WF_prior.set_conduc(lambda_0 = 0.05, lambda_m = 0.25, lambda_t = 1.25e-4)
WF_prior.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                                  "XI" : [22, 20, 62.5] })
WF_prior.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                     "dp" : [4.75e-11, 8e-11] } )

# Best fit
WF_bestf.set_capacity(cp_0 = 2105.53, cp_t = 11.271)
WF_bestf.set_conduc(lambda_0 = 0.0228, lambda_m = -0.112, lambda_t = 9.052e-4)
WF_bestf.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                                  "XI" : [-24.7, 5.68, 17.88] })
WF_bestf.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                     "dp" : [1.992e-10, 2.312e-10] } )

# Solution alpha = 100
WF_solut.set_capacity(cp_0 = 1072.19, cp_t = 11.271)
WF_solut.set_conduc(lambda_0 = 0.0335, lambda_m = 0.196, lambda_t = 1.56e-4)
WF_solut.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                                  "XI" : [21.22, 16.95, 17.14] })
WF_solut.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                     "dp" : [6.471e-11, 1.402e-10] } )

"""

# D_t(T) pour HR fixe de 50%

HR = 0.5
T = np.linspace(0, 25, num = 26) + 273.15
PC = ham.p_c(HR, T)

Dt_carac = WF_carac.conduc(PC,T) / ( WF_carac.rho * WF_carac.cp(T) )
Dt_prior = WF_prior.conduc(PC,T) / ( WF_prior.rho * WF_prior.cp(T) )
Dt_bestf = WF_bestf.conduc(PC,T) / ( WF_bestf.rho * WF_bestf.cp(T) )
Dt_solut = WF_solut.conduc(PC,T) / ( WF_solut.rho * WF_solut.cp(T) )
#Dt_1 = ( wood_fibre.lambda_0 + (T-273.15)*wood_fibre.lambda_t ) / ( wood_fibre.rho * wood_fibre.cp(T) )
#Dt_2 = ( wood_fibre2.lambda_0 + (T-273.15)*wood_fibre2.lambda_t ) / ( wood_fibre2.rho * wood_fibre2.cp(T) )

"""

# D_w(HR) pour T fixe de 20 degC
T = 293.15
HR = np.linspace(0.4,0.9, num = 26)
PC = ham.p_c(HR, T)

#Dw_carac = ham.p_sat(T) * WF_carac.delta_p(PC, T) * HR / (WF_carac.c_w(PC, T) * ham.rho_liq * ham.Rv * T)
#Dw_prior = ham.p_sat(T) * WF_prior.delta_p(PC, T) * HR / (WF_prior.c_w(PC, T) * ham.rho_liq * ham.Rv * T)
#Dw_bestf = ham.p_sat(T) * WF_bestf.delta_p(PC, T) * HR / (WF_bestf.c_w(PC, T) * ham.rho_liq * ham.Rv * T)
#Dw_solut = ham.p_sat(T) * WF_solut.delta_p(PC, T) * HR / (WF_solut.c_w(PC, T) * ham.rho_liq * ham.Rv * T)

Dp_carac = WF_carac.delta_p(PC, T)
Dp_prior = WF_prior.delta_p(PC, T)
Dp_bestf = WF_bestf.delta_p(PC, T)
Dp_solut = WF_solut.delta_p(PC, T)


# Esthetique
P.rc('text', usetex=True)
P.rc('font', **{'family' : 'serif',
                'size'   : 18 })

# Traces
P.hold(True)

a = [HR]*4
b = [Dp_carac, Dp_prior, Dp_bestf, Dp_solut]
colors = ['r-', 'k:', 'k--', 'k-']

for i in range(4):
    P.plot(a[i], b[i], colors[i], linewidth = 1.5)
    
P.xlabel(r'Relative humidity')
P.ylabel(r'Vapour permeability (s)')
P.legend(('Measured', 'Prior', 'Best fit', 'Solution'), loc='upper left', ncol=2, fontsize=16)

#P.xlim((0.1, 0.9))
P.ylim((0, 3.2e-10))


fig1 = P.plt.gcf()
fig1.savefig('vapour_perm.pdf', format='pdf', bbox_inches='tight')
