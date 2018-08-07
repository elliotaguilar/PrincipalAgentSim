#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 18:03:41 2018

@author: elliotaguilar
"""

#Important parameter conditions
#rho*R-c>0
#alpha + rho<1
#
import numpy as np
import matplotlib.pyplot as plt
#--------------------------------------------    
#---------------Parameters-------------------
#-------------------------------------------- 
n=15
p=.1 #must be less that 1-a
a=.01 #must be less than 1
R=10
c=10
gamma=.3
gamma_0=1
N=100
margin=.01
T=1000
runs=100
max_d=False #determines whether compensation is determined by max d or 1/n
#--------------------------------------------    
#---------------Functions-------------------
#-------------------------------------------- 

def set_physician_dist(n):
    x=np.ndarray.flatten(np.random.rand(1,n))
    dist=[i/sum(x) for i in x]
    #print('length of d is ',len(dist))
    return dist

def fixed_wage_rule(effort,comp,dist,max_d):  #for fixed wage rule, determine the rent and revenue received by agent and principal, respectively
    if max_d==True: d=max(dist)
    else:d=1/len(dist)
    if effort==1: sales=sum([(a+p*prop)*prop for prop in dist])*N
    elif effort==2: sales=(a+p)*d*N
    elif effort==3:
        x=np.ndarray.flatten(np.random.rand(1,n))
        e=[i/sum(x) for i in x]
        sales=sum([(a+p*e[i])*dist[i]  for i in range(len(dist))])*N
    else: sales=a*N
    rent=comp-c
    revenue=R*sales-comp
    #print('comp = ',comp,' revenue = ',R*sales)
    return rent,revenue
    
def commission_rule(effort,comp,dist,max_d):
    if max_d==True: d=max(dist)
    else:d=1/len(dist)
    if effort==1: sales=sum([(a+p*prop)*prop for prop in dist])*N
    elif effort==2: sales=(a+p)*d*N
    elif effort==3: 
        x=np.ndarray.flatten(np.random.rand(1,n))
        e=[i/sum(x) for i in x]
        sales=sum([(a+p*e[i])*dist[i]  for i in range(len(dist))])*N
    else: sales=a*N
    rent=comp*sales-c
    revenue=sales*(R-comp)
    #print('comp = ',comp*sales,' revenue = ',R*sales)
    #print(' units sold ',sales)
    return rent,revenue    

def quota_rule(effort,comp,dist,max_d):  #assumes that quota is set by the max physician weight
    if max_d==True: d=max(dist)
    else:d=1/len(dist)
    q=a+p*max(dist)
    if effort==1: sales=sum([(a+p*prop)*prop for prop in dist])*N
    elif effort==2: sales=(a+p)*d*N
    elif effort==3: 
        y=np.ndarray.flatten(np.random.rand(1,n))
        e=[i/sum(y) for i in y]
        sales=sum([(a+p*e[i])*dist[i] for i in range(len(dist))])*N
    else: sales=a*N
    if sales>=q*N: 
        rent=comp-c
        revenue=sales*(R-comp)
    else: 
        rent=0
        revenue=R*sales
    return rent,revenue     

def choose_comp_rule(gamma,revenues,dist): #this functionn should return a compensation for agents?
    if np.random.rand()<=gamma:
        rule=np.random.randint(1,4)
    else:
        r=np.random.rand()
        if sum(revenues)==0: rule=np.random.randint(1,4)
        elif r<=revenues[0]/sum(revenues): rule=1 
        elif revenues[0]/sum(revenues)<r<=sum(revenues[:2])/sum(revenues): rule=2            
        else: rule=3            
    if rule==1:
        comp=c #fixed wage
    elif rule==2: 
        comp=(1-margin)*(c/(p*max(dist)*N))+margin*R #commission plan
    else: 
        comp=(1-margin)*c+margin*R*(a+p*max(dist))*N # quota-based
    return rule,comp

def choose_agent_effort(rents):  #this funcion takes in the rule and compensation, chooses an effort allocation, and returns the rent and revenue
    if np.random.rand()<=gamma:
        effort=np.random.randint(1,5)
    else:
        r=np.random.rand()
        if sum(rents)==0: effort=np.random.randint(1,5)
        elif r<=rents[0]/sum(rents): 
            #print('prop allocation')
            effort=1
        elif rents[0]/sum(rents)<r<=sum(rents[:2])/sum(rents): 
            #print('max allocation')
            effort=2
        elif sum(rents[:2])/sum(rents)<r<=sum(rents[:3])/sum(rents): 
            #print('random allocation')
            effort=3
        else: 
            #print('zero allocation')
            effort=4
    return effort

def compensation_and_revenue(rule,comp,effort,dist,max_d):
    if rule==1: 
        #print('fixed wage rule in effect')
        return fixed_wage_rule(effort,comp,dist,max_d)
    elif rule==2:
        #print('commission rule in effect')
        return commission_rule(effort,comp,dist,max_d)
    else: 
        #print('quota-based rule in effect')
        return quota_rule(effort,comp,dist,max_d)

def track_efforts(effort,Prop_hist,Max_hist,Random_hist,Zero_hist):
    if effort==1: 
        Prop_hist.append(1)
        Max_hist.append(0)
        Random_hist.append(0)
        Zero_hist.append(0)
    elif effort==2:
        Prop_hist.append(0)
        Max_hist.append(1)
        Random_hist.append(0)
        Zero_hist.append(0)        
    elif effort==3:
        Prop_hist.append(0)
        Max_hist.append(0)
        Random_hist.append(1)
        Zero_hist.append(0)
    else:
        Prop_hist.append(0)
        Max_hist.append(0)
        Random_hist.append(0)
        Zero_hist.append(1)
    return   Prop_hist,Max_hist,Random_hist,Zero_hist    

def track_rules(rule,Fixed_hist,Commission_hist,Quota_hist):
    if rule==1:
        Fixed_hist.append(1)
        Commission_hist.append(0)
        Quota_hist.append(0)
    elif rule==2:
        Fixed_hist.append(0)
        Commission_hist.append(1)
        Quota_hist.append(0)
    else:
        Fixed_hist.append(0)
        Commission_hist.append(0)
        Quota_hist.append(1)
    return Fixed_hist,Commission_hist,Quota_hist
        
def simulation_round(n,p,a,R,c,gamma,N,margin,rents,revenues,max_d):
    dist=set_physician_dist(n)
    rule,comp=choose_comp_rule(gamma,revenues,dist)
    effort=choose_agent_effort(rents)
    rent,revenue=compensation_and_revenue(rule,comp,effort,dist,max_d)
    revenues[rule-1]+=revenue
    rents[effort-1]+=rent
    revenue_hist.append(revenue)
    rent_hist.append(rent)
    track_efforts(effort,Prop_hist,Max_hist,Random_hist,Zero_hist) #Prop_hist,Max_hist,Random_hist,Zero_hist=
    track_rules(rule,Fixed_hist,Commission_hist,Quota_hist) #Fixed_hist,Commission_hist,Quota_hist=
    return rent_hist,revenue_hist,rents,revenues,Prop_hist,Max_hist,Random_hist,Zero_hist,Fixed_hist,Commission_hist,Quota_hist
    
def param_sweep(start,stop,increment):
    newlist=[]
    while start<stop:
        start+=increment
        newlist.append(start)
    return newlist

def rho_sweep(start,alphas,increment):
    totallist=[]
    for a in alphas:
        row_list=[]
        first=start
        while first<a:
            first+=increment
            row_list.append(first)
        totallist.append(row_list)
    return totallist
                
#--------------------------------------------    
#---------------Simulation-------------------
#-------------------------------------------- 

#initial values     

data_rent=np.array([[0]*T])
data_revenue=np.array([[0]*T])
Fixed_wage=np.array([[0]*T])
Commission_wage=np.array([[0]*T])
Quota_wage=np.array([[0]*T])
Prop_allocation=np.array([[0]*T])
Max_allocation=np.array([[0]*T])
Random_allocation=np.array([[0]*T])
Zero_allocation=np.array([[0]*T])
#rule_hist
for r in range(0,runs):
    revenues=[0]*3 
    rents=[0]*4 
    revenue_hist=[]
    rent_hist=[]
    Fixed_hist=[]
    Commission_hist=[]
    Quota_hist=[]
    Prop_hist=[]
    Max_hist=[]
    Random_hist=[]
    Zero_hist=[]
    for t in range(0,T):
        gamma=gamma_0*np.exp(-.05*t)
        rent_hist,revenue_hist,rents,revenues,Prop_hist,Max_hist,Random_hist,Zero_hist,Fixed_hist,Commission_hist,Quota_hist=simulation_round(n,p,a,R,c,gamma,N,margin,rents,revenues,max_d)
    new_rent=np.array([rent_hist])
    new_revenue=np.array([revenue_hist])
    fixed=np.array([Fixed_hist])
    commission=np.array([Commission_hist])
    quota=np.array([Quota_hist])
    prop=np.array([Prop_hist])
    maxa=np.array([Max_hist])
    randa=np.array([Random_hist])
    zeroa=np.array([Zero_hist])
    data_rent=np.concatenate((data_rent,new_rent),axis=0)
    data_revenue=np.concatenate((data_revenue,new_revenue),axis=0)
    Fixed_wage=np.concatenate((Fixed_wage,fixed),axis=0)
    Commission_wage=np.concatenate((Commission_wage,commission),axis=0)
    Quota_wage=np.concatenate((Quota_wage,quota),axis=0)
    Prop_allocation=np.concatenate((Prop_allocation,prop),axis=0)
    Max_allocation=np.concatenate((Max_allocation,maxa),axis=0)
    Random_allocation=np.concatenate((Random_allocation,randa),axis=0)
    Zero_allocation=np.concatenate((Zero_allocation,zeroa),axis=0)
    
mean_rents=np.mean(data_rent,axis=0)
mean_revenues=np.mean(data_revenue,axis=0)       
