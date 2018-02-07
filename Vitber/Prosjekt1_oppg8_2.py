# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 14:09:42 2018

@author: helen
"""

import matplotlib.pyplot as plt
from prosjekt1_formler import chebyshev, fredholm_lhs, rho , K , Lagrange, fredholm_rhs, Newton_Cotes


import numpy as np
filename = 'q8_2.npz '
f = open( filename, 'rb' )
npzfile = np.load(f)
#print(npzfile.files)
#print(npzfile['a'] , npzfile['b'] , npzfile['d'])
#print(npzfile['xc'])
#print(npzfile['F'])

a = npzfile['a']
print('Detter er verdien vi har hentet inn for a: ',a)
b = npzfile['b']
print('Dette er verdien vi har hentet inn for b: ',b)
d = npzfile['d']
print('Dette er verdien vi har hentet inn for d: ',d)
xc = npzfile['xc']
print('Dette er xc ',xc,'lengden til xc er ',len(xc))
F = npzfile['F']

lamb = 10**(-4)

N_eval = len(xc)
Nq = N_eval**2

xq_old,w_old = np.polynomial.legendre.leggauss(Nq)
xq = (1/2)*(xq_old +1)*(b-a) + a
w = (1/2)*w_old
xs = chebyshev(a,b,N_eval)
    

def losning(lamb):
    A = fredholm_lhs(xc, xs, xq, w, d)
    A_t = np.transpose(A)
    venstre_side = np.add(np.matmul(A_t,A),np.multiply(lamb,np.eye(N_eval)))
    hoyre_side = np.dot(A_t,F)
    losning = np.linalg.solve(venstre_side,hoyre_side)
    return losning

plt.figure()
plt.plot(xs,losning(lamb))
plt.show()