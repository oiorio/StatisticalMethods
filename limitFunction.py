import ROOT
def printLimits(DATA,SM,BM,poiname,paramsscan=None,valuepoi=None,signif=False,asymp=False,freq=False,postfix=""):
    BM.Print()
    SM.Print()
    if ( paramsscan is None):
        paramsscan ={"npoints":8,"poimin":0,"poimax":2000,"minplot":-1,"maxplot":-1}

    npoints=paramsscan["npoints"]
    poimin=paramsscan["poimin"]
    poimax=paramsscan["poimax"]
    minplot=paramsscan["minplot"]
    maxplot=paramsscan["maxplot"]
 
    ac= ROOT.RooStats.AsymptoticCalculator(DATA, BM, SM);
    ac.Initialize()

    fc= ROOT.RooStats.FrequentistCalculator(DATA, BM, SM);
    fc.SetToys(2500,500)


    if(signif):
        ahypo= ac.GetHypoTest()
        ahypo.Print()

    if(freq):
            
        #use frequentist approach: 
        #Warning: this will take a lot of time! 
        #In general: better use asymptotic approximation if number of events is rather large. 
        #Bias in the test statistic negative log likelihood, i.e. q0, will go as 1/sqrt(N) --> negligible for large datasets

        #Create hypotest inverter passing the calculator 
        freqCalc = ROOT.RooStats.HypoTestInverter(fc)

        #set confidence level (e.g. 90% upper limits)
        freqCalc.SetConfidenceLevel(0.90)

        #use CLs
        freqCalc.UseCLs(1)
 
        #Configure ToyMC Sampler
        toymcs = freqCalc.GetHypoTestCalculator().GetTestStatSampler()

        #choose the test statistics: profile NLL
        profll = ROOT.RooStats.ProfileLikelihoodTestStat(SM.GetPdf())

        #for CLs (bounded intervals) use one-sided profile likelihood
        profll.SetOneSided(1)

        #set the test statistic to use for toys
        toymcs.SetTestStatistic(profll)

          
        #generate pseudoexperiments to get the distribution of the test statistic
            
        freqCalc.SetFixedScan(npoints,poimin,poimax);
            
        result = freqCalc.GetInterval() #This is a HypoTestInveter class object
        result.Print()
        upperLimit = result.UpperLimit()
        exp=result.GetExpectedUpperLimit(0)
        p1=result.GetExpectedUpperLimit(1)
        m1=result.GetExpectedUpperLimit(-1)
        
        print ("====\n upper limit is ", upperLimit," exp ", exp, " p1 ",p1, " m1 ",m1, "\n\n ====")
        result.Print()
        c1=ROOT.TCanvas("limitCanvas") 
        c1.SetLogy()
        inv_plot = ROOT.RooStats.HypoTestInverterPlot("HTI_Result_Plot","result plot",result)
        if minplot!=-1 and maxplot!=-1:
            gr1 = inv_plot.MakePlot();
            gr1.Draw("ALP")
            gr1.GetYaxis().SetRangeUser(minplot,maxplot)
            gr2 = inv_plot.MakeExpectedPlot();
            gr2.Draw("LF")
            gr1.Draw("LP")

        inv_plot.Draw("2CL")
        c1.SaveAs("limitex"+postfix+".png")
            
    if(asymp):
        asympCalc = ROOT.RooStats.HypoTestInverter(ac)
        asympCalc.SetConfidenceLevel(0.90)
        #use CLs
        asympCalc.UseCLs(1)
        asympCalc.SetVerbose(3)

            
        asympCalc.SetFixedScan(npoints,poimin,poimax);
            
 
        result = asympCalc.GetInterval() #This is a HypoTestInveter class object
        result = asympCalc.GetInterval() #This is a HypoTestInveter class object
        result.Print()
        upperLimit = result.UpperLimit()
        exp=result.GetExpectedUpperLimit(0)
        p1=result.GetExpectedUpperLimit(1)
        m1=result.GetExpectedUpperLimit(-1)
        
        print ("====\n upper limit is ", upperLimit," exp ", exp, " p1 ",p1, " m1 ",m1, "\n\n ====")
        result.Print()
        c1=ROOT.TCanvas("limitCanvas") 
        c1.SetLogy()
        inv_plot = ROOT.RooStats.HypoTestInverterPlot("HTI_Result_Plot","result plot",result)
        if minplot!=-1 and maxplot!=-1:
            gr1 = inv_plot.MakePlot();
            gr1.Draw("ALP")
            gr1.GetYaxis().SetRangeUser(minplot,maxplot)
            gr2 = inv_plot.MakeExpectedPlot();
            gr2.Draw("LF")
            gr1.Draw("LP")

            inv_plot.Draw("2CL")
        else:
            inv_plot.Draw("2CL")
        c1.SaveAs("limitex"+postfix+".png")
