# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 09:17:03 2014

@author: Rouchier
"""

from matplotlib import rc
rc("font", family="serif", size=16)
#rc("text", usetex=True)
# rc("./weaklensing.tex")

import daft

pgm = daft.PGM([4,4], origin=[0,0])

# Tout en bas
h = 0.5
pgm.add_node(daft.Node("obsT", r"$T^\mathrm{obs}$", 2.5, h, observed = True))
# Un cran au dessus
h = 1.5
pgm.add_node(daft.Node("T",   r"$T$",   2, h))
pgm.add_node(daft.Node("epsT", r"$\epsilon^T$", 3, h))
# Un cran au dessus
h = 2.5
pgm.add_node(daft.Node("lambda", r"$k$", 3, h))
pgm.add_node(daft.Node("xsensor", r"$x_s$", 2, h, fixed = True))
pgm.add_node(daft.Node("u", r"$u$", 1 , 2.5))
# Tout en haut
h = 3.5
pgm.add_node(daft.Node("obsU", r"$u^\mathrm{obs}$", 0.5 , h, observed = True))
pgm.add_node(daft.Node("epsU", r"$\epsilon^u$", 1.5 , h))

# Fleches
pgm.add_edge("obsU", "u")
pgm.add_edge("epsU", "u")
pgm.add_edge("u", "T")
pgm.add_edge("xsensor", "T")
pgm.add_edge("lambda", "T")
pgm.add_edge("T", "obsT")
pgm.add_edge("epsT", "obsT")

pgm.render()
pgm.ax.text(5.5,4,"deterministic", fontdict={'size':14, 'color':'green'})

"""
pgm = daft.PGM([4.7, 2.35], origin=[-1.35, 2.2])
pgm.add_node(daft.Node("Omega", r"$\Omega$", -1, 4))
pgm.add_node(daft.Node("gamma", r"$\gamma$", 0, 4))
pgm.add_node(daft.Node("obs", r"$\epsilon^{\mathrm{obs}}_n$", 1, 4, observed=True))
pgm.add_node(daft.Node("alpha", r"$\alpha$", 3, 4))
pgm.add_node(daft.Node("true", r"$\epsilon^{\mathrm{true}}_n$", 2, 4))
pgm.add_node(daft.Node("sigma", r"$\sigma_n$", 1, 3))
pgm.add_node(daft.Node("Sigma", r"$\Sigma$", 0, 3))
pgm.add_node(daft.Node("x", r"$x_n$", 2, 3, observed=True))
pgm.add_plate(daft.Plate([0.5, 2.25, 2, 2.25],
        label=r"galaxies $n$"))
        
# Fleches
pgm.add_edge("Omega", "gamma")
pgm.add_edge("gamma", "obs")
pgm.add_edge("alpha", "true")
pgm.add_edge("true", "obs")
pgm.add_edge("x", "obs")
pgm.add_edge("Sigma", "sigma")
pgm.add_edge("sigma", "obs")

pgm.render()
pgm.figure.savefig("weaklensing.pdf")
pgm.figure.savefig("weaklensing.png", dpi=150)
"""
