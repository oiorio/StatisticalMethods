#Part 1: fitting with minuit

from iminuit import Minuit
from scipy.stats import norm
from scipy.optimize import minimize
from scipy.stats import rv_continuous
from iminuit.util import describe, make_func_code
import numpy as np
import math


#Let's first define the metrics, chi2 
def chi2(model,x,y,sigma,*par):
    return ((model(x,*par)-y)/sigma)**2

class leastsquares:
    def __init__(self,model,xs,ys,sigmas):
        self.model=model
        self.xs=xs
        self.ys=ys
        self.sigmas=sigmas
    def __call__(self, *par):
        chitot=0
        for i in range(len(self.xs)):
            chitot=chitot+chi2(self.model,self.xs[i],self.ys[i],self.sigmas[i],*par)
        return chitot

class gaussian_gen(rv_continuous):
    
    def set_pars(self,mean,sigma):
        self.mean=mean
        self.sigma=sigma
    
    def _pdf(self, x):
        return np.exp(-(x-self.mean)**2 / (2.*self.sigma**2)) / (self.sigma*np.sqrt(2.0 * np.pi))


#And Negative Log Likelihood to minimize 
class nll:
    def __init__(self,model,x):
        self.x=x
        self.model=model
    def __call__(self, *par):
#        for xi in self.x:
#            print(self.model(xi,*par))
        return np.sum([-2*math.log(self.model(xi,*par)) for xi in self.x])

if __name__ == "__main__":

    print("Simple Fitting procedure!")

    #Let's now make an example: 
    #Linear function      
    linear = lambda x,a,b : a+b*x
    gaussian = lambda x,mu,sigma : 1/(sigma*np.sqrt(2*math.pi)) * np.exp(-(x-mu)*(x-mu) / (2* sigma*sigma) )
    #Those are equivalent to:
    def linear_func(x,a,b):
        return a +b*x
    def gaussian_func (x,mu,sigma,n):
        return 1/(sigma*math.sqrt(2*math.pi)) * math.exp(-(x-mu)*(x-mu) / (2* sigma*sigma) )
   
    #Example #1.1 linear fit 
    a=2
    b=1
 
    #let's make some numbers 
    xsm=[0,1.1,4]
    xss=[.1,.1,.1]

    ys=[linear(norm(x[0],x[1]).rvs(),a,b) for x in zip(xsm,xss)] #We generate ys from the parameters a and b, but by fluctuating them.

    ls=leastsquares(linear,xsm,ys,xss)
    
    print(ls(a,b))

    m1 = Minuit(ls,a,b) 
    m1.migrad()
    m1.hesse()
    
    print ( m1.params )
    print ( m1.values )
    print ( m1.errors )


    #Example 1.2: Gaussian fit: 

    #We could use a gaussian defined like this
    gau=gaussian_gen(a=-1000,b=1000,name="custom_gaussian") 
    gau.set_pars(mean=104,sigma=10)
    values=[]
    for i in range(10):
        values.append(gau.rvs() )
    
    #Norm is more efficient:
    values=norm(104,10).rvs(1000)

    nl=nll(gaussian,values)
    mu = 50
    sigma = 5
    print(nl(mu,sigma))

    #Check some of the features:
    mea=np.mean(values)
    ndof= 1
    print ("# Generated points:",len(values)," mean ", mea," error on the mean ",np.std(values,ddof=ndof)/math.sqrt(len(values)))
       
    m2 = Minuit(nl,mu,sigma)
    m2.migrad()
    m2.hesse()
    m2.minos()

    print(m2.params, m2.values, m2.errors)

    

