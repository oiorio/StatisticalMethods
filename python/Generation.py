import Minimization
from iminuit import Minuit
from scipy.stats import norm
from scipy.optimize import minimize
from scipy.stats import rv_continuous,poisson
from iminuit.util import describe, make_func_code
import numpy as np
import math,sys
import matplotlib.pyplot as plt

class sum_function(rv_continuous):
    
    def set_pars(self,mean,sigma,l,sig,bkg):
        self.mean=mean
        self.sigma=sigma
        self.l=l
        self.sig=sig
        self.bkg=bkg
    
    def _pdf(self, x):
        sigpdf = np.exp(-(x-self.mean)**2 / (2.*self.sigma**2)) / (self.sigma*np.sqrt(2.0 * np.pi))
        bkgpdf = 1/self.l*np.exp(-(x/self.l) )

        
        f1=self.sig/(self.sig+self.bkg) 
        f2=self.bkg/(self.sig+self.bkg)
        
        return f1*sigpdf+f2*bkgpdf


def main(argv):
    print("Generating events")

    
    sevents=200
    bevents=1000
    seed=1
    print(argv)
    if(len(argv)>1):sevents=argv[1]
    if(len(argv)>2):bevents= argv[2]
    if(len(argv)>3):seed= argv[3]

    seed = int(seed)

    s_true=int(sevents)
    b_true=int(bevents)
    mean=250
    sigma=50
    l=100

    sb_func=sum_function(a=0,b=3000,seed=seed)
    sb_func.set_pars(mean = mean, sigma=sigma,l=l,sig=s_true,bkg=b_true)
    
    sgen=poisson.rvs(s_true) 
    bgen=poisson.rvs(b_true) 
    genevents=sb_func.rvs(size=sgen+bgen)
    
    fig, ax = plt.subplots(1, 1)
    nbins = 20
    ax.hist(genevents,nbins)
    postfix=""
    if(len(argv)>0):
        postfix="_s"+str(sevents)+"_b"+str(bevents)+"_seed"+str(seed)
    plt.savefig("generated_events"+postfix+".png")
    f = open("generated_events"+postfix+".txt","w")
    for g in genevents:
        f.write(str(g)+"\n")

if __name__ == "__main__":
    main(sys.argv)
    
