#coding:utf-8

import math

def Co_delta(ci,cj):
    ret=[1,2]
    ret[0]=ci[0]-cj[0]
    ret[1]=ci[1]-cj[1]

    return ret

def Co_dis(ci):
    return math.sqrt(ci[0]*ci[0]+ci[1]*ci[1])

'''

revise 输入 上一次的坐标cj=[xj,yj] ， deltaPSK PSK的距离差，deltaDoppler多普勒的距离差 , cPSK 这一次PSK测出的坐标,alpha为PSK校正项系数，beta为doppler校正项系数

输出为 这一次校正后的坐标ci=[xi,yi]

'''
def _revise(cj,deltaPSK,deltaDoppler,cPSK,alpha,beta):


    ci=[0,0]
    #ci[0]=rx
    #ci[1]=ry

    #func=(Co_dis(Co_delta(ci,cj))-deltaPSK)*(Co_dis(Co_delta(ci,cj))-deltaPSK)+(Co_dis(Co_delta(ci,cj))-deltaDoppler)*(Co_dis(Co_delta(ci,cj))-deltaDoppler)

    maxx=cPSK[0]+5
    if(cPSK[0]-5>0):
        minx=cPSK[0]-5
    else :
        minx=0

    maxy=cPSK[1]+5
    miny=cPSK[1]-5

    x=minx
    y=miny

    rmin=100000
    print "maxx is "+str(maxx)
    while ( x<=maxx):
        y=miny
        print "now x is "+str(x)
        while(y<maxy):
            ci[0]=x
            ci[1]=y
            func=alpha*Co_dis((Co_delta(Co_delta(ci,cj),deltaPSK)))+beta*Co_dis(Co_delta(Co_delta(ci,cj),deltaDoppler))

            print "now func is " + str(func) + "x and y is " + str(x) + " " + str(y)+" but rmin is "+str(rmin) + " "+str(Co_delta(ci,cj))+" "

            if(func<=rmin):
                rmin=func
                xi=x
                yi=y
            y=y+0.1
        x=x+0.1


    ci[0]=xi
    ci[1]=yi
    print rmin
    return ci
'''
Vx
Vy是多普勒算出来的速度
cj是上一次计算出的坐标
cPSK是这一次PSK测出来的坐标
alpha为PSK校正项系数，beta为doppler校正项系数
返回ci 这一次计算出来的坐标
'''
def revise(Vx,Vy,cj,cPSK,alpha,beta):
    deltaDoppler=[0,0]
    deltaDoppler[0]=Vx*0.1
    deltaDoppler[1]=Vy*0.1
    deltaPSK=Co_dis(Co_delta(cPSK,cj))

    deltaPSK=[0,0]
    deltaPSK[0]=cPSK[0]-cj[0]
    deltaPSK[1]=cPSK[1]-cj[1]
    print cj
    print deltaPSK
    print deltaDoppler
    print cPSK
    print alpha
    print beta
    return _revise(cj,deltaPSK,deltaDoppler,cPSK,alpha,beta)

#print revise([5,5],1,1.5,[5,6],1,1)
#print revise(10,10,[5,5],[5,6],1,1)


