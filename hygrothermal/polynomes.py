# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 08:53:31 2015

@author: simon
"""

w = np.zeros_like(xi_p1_samples)
for i in range(len(xi_p1_samples)):
    
    poly2 = np.polyfit([0.25, 0.5, 0.75], [xi_p1_samples[i], xi_p2_samples[i], xi_p3_samples[i]], deg = 2)
    poly3 = np.polyint(poly2)
    w[i] = np.polyval(poly3, 0.5)
