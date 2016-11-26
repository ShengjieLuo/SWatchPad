'''
__author__ = 'lab126'

A=[
[1,0,T,0],
[0,1,0,T],
[0,0,1,0],
[0,0,0,1]]
B=[
[0.5*T*T,0],
[0,0.5*T*T],
[T,0],
[0,T]]
'''
import numpy as np
def xp_update(A,xr,B,u):
    xp=A*xr+B*u
    return xp

def pp_update(A,pr,Q):
    pp=A*pr*A.T+Q
    return pp

def k_update(pp,R):
    k=pp/(R+pp)
    return k

def pr_update(k,pp):
    pr=(1-k)*pp
    return pr

def xr_update(A,xp,k,z):
    xr=A*xp+k*(z-xp)
    return xr

def kalman(xr,pr,u,z,Q,R):
    T=0.1
    A=np.matrix([[1,0,T,0],[0,1,0,T],[0,0,1,0],[0,0,0,1]])
    B=np.matrix([[0.5*T*T,0],[0,0.5*T*T],[T,0],[0,T]])

    xp=xp_update(A,xr,B,u)
    pp=pp_update(A,pr,Q)

    k=k_update(pp,R)

    pr=pr_update(k,pp)
    xr=xr_update(A,xp,k,z)

    return xr,pr
'''
a=np.matrix([5,6])
print a*T
'''