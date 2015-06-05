


from matplotlib import rc
rc("font", family="serif", size=16)
#rc("text", usetex=True)
# rc("./weaklensing.tex")

import daft

pgm = daft.PGM([4,4], origin=[0,0])

# Tout en bas
h = 0.5
pgm.add_node(daft.Node("obsT", r"$T^\mathrm{obs}$", 2.5, h, observed = True, aspect = 1.5))
# Un cran au dessus
h = 1.5
pgm.add_node(daft.Node("T",   r"$T$",   2, h))
pgm.add_node(daft.Node("epsT", r"$\sigma^T$", 3, h, plot_params = {"ec": "#ff0000"}))
# Un cran au dessus
h = 2.5
pgm.add_node(daft.Node("lambda", r"$k$", 3, h, plot_params = {"ec": "#ff0000"}))
pgm.add_node(daft.Node("xsensor", r"$x_s$", 2, h, plot_params = {"ec": "#ff0000"}))
pgm.add_node(daft.Node("u", r"$u$", 1 , h))
# Tout en haut
h = 3.5
pgm.add_node(daft.Node("obsU", r"$u^\mathrm{obs}$", 0.5 , h, aspect = 1.5, fixed = True))
pgm.add_node(daft.Node("epsU", r"$\sigma^u$", 1.5 , h, plot_params = {"ec": "#ff0000"}))

# Fleches
pgm.add_edge("obsU", "u")
pgm.add_edge("epsU", "u")
pgm.add_edge("u", "T")
pgm.add_edge("xsensor", "T")
pgm.add_edge("lambda", "T")
pgm.add_edge("T", "obsT")
pgm.add_edge("epsT", "obsT")

pgm.render()
#pgm.ax.text(5.5,4,"deterministic", fontdict={'size':14, 'color':'green'})
pgm.figure.savefig("drawing_conductivity.pdf")
pgm.figure.savefig("drawing_conductivity.png", dpi=300)
