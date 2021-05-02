import Minimization
from iminuit import Minuit
from scipy.stats import norm
from scipy.optimize import minimize
from scipy.stats import rv_continuous,poisson
from iminuit.util import describe, make_func_code
import numpy as np
import math,sys
import matplotlib.pyplot as plt
import Minimization
print (Minimization.chi2)
import optparse

#I give you the model:

class sum_function(rv_continuous):
    
    def set_pars(self,mean,sigma,l,sig,bkg):
        self.mean=mean
        self.sigma=sigma
        self.l=l
        self.sig=sig
        self.bkg=bkg
    
    def _pdf(self, x):
        f1=self.sig/(self.sig+self.bkg) 
        f2=self.bkg/(self.sig+self.bkg)
        
        sigpdf = np.exp(-(x-self.mean)**2 / (2.*self.sigma**2)) / (self.sigma*np.sqrt(2.0 * np.pi))
        bkgpdf = 1/self.l*np.exp(-(x/self.l) )
        
        return f1*sigpdf+f2*bkgpdf

def main(argv):

    postfix=""
    if(len(argv)>1):postfix = argv[1]
    fin = open("generated_events"+str(postfix)+".txt","r")
    numlist=[]
    for l in fin.readlines():
        numlist.append(float(l))

    print(numlist)



    #2.1 let's write the likelihood by hand:
    #set some initial values of the parameters
    
    mean = 200
    sigma = 100
    l = 200
    s = 10
    b= len(numlist)-s
    
    nll=0
    sum_pdf=sum_function(a=0.,b=3000.)
    sum_pdf.set_pars(mean=mean,sigma=sigma,l=l,sig=s,bkg=b)

    for n in numlist:
        spdf=sum_pdf.pdf(n)
        nll+=-2*np.log(spdf)
        if np.isnan(nll) or nll>10000000:return
        
    print ("log likelihood",nll)

    #is this enough? 
    #This doesn't take into account the fluctuation of the number of events!
    nexpected=len(numlist)#for exercise, we take n expected = n observed
    print("n expected events", nexpected)
    nobserved=nexpected
    p=0
    pois = poisson(nexpected)
    p = -2*np.log(pois.pmf(nobserved))
    
    print ("new log likelihood",p+nll)
   
    #Now we need to maximize this function! How do we do?
    
    # We need first to write the function to maximize!
    #2.2 The unbinned maximum likelihood needs to be 
    def extendedNLLfunction(x,mean,sigma,l,sig,bkg):
        negll=0
        sum_pdf=sum_function(a=0,b=3000)
        sum_pdf.set_pars(mean=mean,sigma=sigma,l=l,sig=sig,bkg=bkg)
        pois=poisson(sig+bkg)
        for xi in x:
            negll+=-2*np.log(sum_pdf.pdf(xi))
        p=-2*np.log(pois.pmf(len(x)))+negll
        p=p+negll
        print("nll",p,"pars",mean,sigma,l,sig,bkg)
        return p

    #what is the correct function to use? nl or chi2? A: neither!!!! 
    
    from Minimization import extendednll

    exnll = extendednll(extendedNLLfunction,numlist)

    print(exnll(mean,sigma,l,s,b))


    m3=Minuit(exnll,mean,sigma,l,s,b)
    for e in range(len(m3.errors)):
        m3.errors[e]=m3.values[e]*0.3

    print(Minuit.LEAST_SQUARES)
    m3.errordef=Minuit.LIKELIHOOD
    m3.strategy= 0
    m3.scan()
    m3.strategy= 1
    m3.scan()

    fig, ax = plt.subplots(1, 1)
    
    m3.draw_profile("x3")
    m3.draw_profile("x4")

    plt.savefig("simplescanplot+"+postfix+".png")

    prof3x,prof3y=m3.profile("x3")
    prof4x,prof4y=m3.profile("x4")
    print(m3.params, m3.values, m3.errors,m3.covariance)


    m3.strategy= 2
    m3.migrad()
    print(m3.params, m3.values, m3.errors,m3.covariance)

    m3.draw_profile("x3")
    m3.draw_profile("x4")
    plt.savefig("migrad_both"+postfix+".png")

    plt.clf()
    m3.draw_profile("x3")
    m3.draw_profile("x4")
    plt.savefig("migrad_only"+postfix+".png")

    print(prof3x,prof3y)
    print("\n\n\n")
    print(prof4x,prof4y)

    
if __name__ == "__main__":
    main(sys.argv)

