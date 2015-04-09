

from matplotlib import rc
rc("font", family="serif", size=16)
rc("text", usetex=True)

import daft

pgm = daft.PGM([6.5,4], origin=[0,0])

# Colors.
in_color = {"ec": "#007200"}
out_color = {"ec": "#ff0000"}

# Tout en bas
h = 0.5
pgm.add_node(daft.Node("out_obs", r"$T,\mathrm{RH},Q$", 2.5, h,
                       aspect = 3., observed = True, plot_params = out_color))

# Un cran au dessus
h = 1.5
pgm.add_node(daft.Node("out_calc", r"$T,\mathrm{RH},Q$", 2.5, h,
                       aspect = 3., plot_params = out_color))

# Un cran au dessus
h = 2.5
pgm.add_node(daft.Node("in_calc", r"$T,\mathrm{RH}$", 2.5, h,
                       aspect = 2., plot_params = in_color))

pgm.add_node(daft.Node("noise", r"$\sigma$", 0.5, h, aspect = 1.))
pgm.add_node(daft.Node("parameters", r"$\theta$", 4.5, h, aspect = 1))

# Tout en haut
h = 3.5
pgm.add_node(daft.Node("in_obs", r"$T,\mathrm{RH}$", 2.5, h,
                       aspect = 2., observed = True, plot_params = in_color))

pgm.add_edge("in_obs", "in_calc")
pgm.add_edge("in_calc", "out_calc")
pgm.add_edge("out_calc", "out_obs")
pgm.add_edge("noise", "in_calc")
pgm.add_edge("noise", "out_obs")
pgm.add_edge("parameters", "out_calc")

pgm.render()
pgm.ax.text(6.55,0.5,"observed", fontdict={'size':14})
pgm.ax.text(6.55,2.5,"calculated", fontdict={'size':14})
pgm.ax.text(6.,4.5,"real", fontdict={'size':14})
pgm.ax.text(6.,6.5,"observed", fontdict={'size':14})

pgm.figure.savefig("arbre HAM.pdf")
pgm.figure.savefig("arbre HAM.png", dpi=200)