import ROOT
import sys

def rooPart1():
    print("Doing part 1: definition and basics")
    #Part 1.1: definitions
    
    #Fit variable: you define the random variable
    mass = ROOT.RooRealVar("mass","mass plot",0,1000,"GeV")  
    nev = ROOT.RooRealVar("n","n events",0,2000)  
    
    nsignal=250
    nbackground=1000

    nev = ROOT.RooRealVar("n","n events",nsignal+nbackground,0,2000)  

    #Variables - or rather parameters 
    signal = ROOT.RooRealVar("signal","signal events",nsignal,0,2000) 
    background = ROOT.RooRealVar("background","signal events",nbackground,0,2000) 
    
    mean = ROOT.RooRealVar("mean","signal mean",200,0,1000)
    sigma = ROOT.RooRealVar("sigma","signal sigma",50,0,1000) 
    lam = ROOT.RooRealVar("lam","lam",-0.01,-5,0)

    total_events = ROOT.RooFormulaVar("total_events", "signal+background", ROOT.RooArgList(signal,background)) 

    #We define two pdfs which are already included in the ROOT libraries   
    #e^(x * lam)
    BkgShape = ROOT.RooExponential("expo","Roofit Exponential function",mass,lam)#Background exponential pdf, 
    SigShape = ROOT.RooGaussian("gauss","Roofit Gaussian function",mass, mean,sigma)#Signal gaussian pdf, already normalized
    #already normalized type RooAbsPdf, documentation here https://root.cern/doc/master/classRooAbsPdf.html

    totevents = ROOT.RooFormulaVar("totevents","@0+@1",ROOT.RooArgSet(signal,background))
    ExpEvents = ROOT.RooPoisson("pois","Total number of events",nev,totevents) 

    

    #Part 1.2: generation let's for example generate from the MC we have:
    AllEvents = SigShape.generate(ROOT.RooArgSet(mass),nsignal)#[2.0,"name",[1,"a"]]
    AllEventsBis = SigShape.generate(ROOT.RooArgSet(mass),20)#[2.0,"name",[1,"a"]]
    BackgroundEvents = BkgShape.generate(ROOT.RooArgSet(mass),nbackground)

    AllEvents.SetName("NominalSignal")
    AllEventsBis.SetName("AltSignal")
    AllEvents.append(BackgroundEvents)#this one is a "dataset" type object , RooAbsData: https://root.cern/doc/master/classRooAbsData.html
    AllEventsBis.append(BackgroundEvents)#this one is a "dataset" type object , RooAbsData: https://root.cern/doc/master/classRooAbsData.html
    BackgroundOnlyEvents = BackgroundEvents.Clone("BackgroundOnly")

    BinnedEvents=AllEvents.binnedClone()#the equivalent but divided in bins
    
    #Plotting routines
    frame = mass.frame(ROOT.RooFit.Title("mass distribution"))
    c1=ROOT.TCanvas()
#    BackgroundOnlyEvents.plotOn(frame)
    BinnedEvents.plotOn(frame)
    frame.Draw()
    c1.SaveAs("exampleEvents.png")
    
    #return
    #Part 1.3: define the extended maximum likelihood
    
    sum_pdf = ROOT.RooAddPdf("sumPDF","Total s+b PDF",ROOT.RooArgList(SigShape,BkgShape),ROOT.RooArgList(signal,background))
    prod_sum_pdf = ROOT.RooProdPdf("extPDF","Total s+b PDF with nevents",ROOT.RooArgList(sum_pdf,ExpEvents))

    #this is another RooAbsPdf
    prod_sum_pdf.fitTo(AllEvents, ROOT.RooFit.Extended(1))#pdf . fit to (dataset, options) 
    
    prod_sum_pdf.plotOn(frame)
    bkg_arg = ROOT.RooArgSet(BkgShape)
    sig_arg = ROOT.RooArgSet(SigShape)

    prod_sum_pdf.plotOn(frame,ROOT.RooFit.Components(bkg_arg), ROOT.RooFit.LineStyle(ROOT.kDotted) ) 
    prod_sum_pdf.plotOn(frame,ROOT.RooFit.Components(sig_arg), ROOT.RooFit.LineStyle(ROOT.kDashed) ) 
     
    frame.Draw()
    c1.SaveAs("exampleFit.png")
    
    #Ez pz lemon squeezy!

    #Now let's use some tools for 1) fit robustness checks and 2) limit setting!

    #Part 1.4: building a workspace
    #A convenient way to "Dock" your data and models is via the workspaces:
    
    w = ROOT.RooWorkspace("ws")
    getattr(w,'import')(AllEvents)
    getattr(w,'import')(BackgroundOnlyEvents)
    getattr(w,'import')(AllEventsBis)
    getattr(w,'import')(prod_sum_pdf)
    
    w.Print()
                      #filename            #option: options are OPEN=not modify existing file,NEW=create it,RECREATE=  if it exists overwrite it  
    fout = ROOT.TFile("WorkspaceFile.root","RECREATE")
    w.Write()
    fout.Close()

def rooPart2():
    print("Doing part 2: fit sanity checks")
    #Part 2.1: let's extract the workspace!
    fin = ROOT.TFile("WorkspaceFile.root")
    ws = fin.Get("ws")#NOTE: Root saves files with the "Name" field!!!
    ws.Print()
    #  return
    print(ws.pdf("sumPDF"))
    print(ws.pdf("gauss"))
    print(ws.pdf("expo"))
    print(ws.var("signal"))
    print(ws.data("NominalSignal"))

    #Now let's make the pseudoexperiments:
    mc_study = ROOT.RooMCStudy(ws.pdf("sumPDF"), ROOT.RooArgSet(ws.var("mass")), ROOT.RooFit.Extended(1), ROOT.RooFit.FitOptions(ROOT.RooFit.Save(1) ))
    mc_study.generateAndFit(1000)#performs both generation and fit 
          
    frame_nll = mc_study.plotNLL(ROOT.RooFit.Bins(40))
    frame_sig = mc_study.plotParam(ws.var("signal"),ROOT.RooFit.Bins(40))
    frame_err = mc_study.plotError(ws.var("signal"),ROOT.RooFit.Bins(40))
    frame_pulls = mc_study.plotPull(ws.var("signal"),ROOT.RooFit.Bins(40),ROOT.RooFit.FitGauss(1))

    c1=ROOT.TCanvas()
    frame_nll.Draw()
    c1.SaveAs("NLLfits.png")

    frame_sig.Draw()
    c1.SaveAs("signal.png")

    frame_err.Draw()
    c1.SaveAs("err_signal.png")

    frame_pulls.Draw()
    c1.SaveAs("pulls_signal.png")

    fin.Close()

def rooPart3(doAsymp=True):
    print("Profile likelihood")
    c1 = ROOT.TCanvas("PL")
   
    #Part 3.1: let's extract the workspace as before
    fin = ROOT.TFile("WorkspaceFile.root")
    ws = fin.Get("ws")
    ws.Print()
 
    SBModel=ROOT.RooStats.ModelConfig()
    SBModel.SetWorkspace(ws)
    
    SBModel.SetPdf("extPDF")
    SBModel.SetName("SBModel")
    poi = ROOT.RooArgSet(ws.var("signal"))#setting the parameter of interest
    SBModel.SetParametersOfInterest(poi)
    SBModel.SetSnapshot(poi)
    SBModel.Print()
    #Lets'evaluate the likelihood test statistics
#    plc = ROOT.RooStats.ProfileLikelihoodCalculator(ws.data("NominalSignal"), SBModel)
    plc = ROOT.RooStats.ProfileLikelihoodCalculator(ws.data("AltSignal"), SBModel)
    plc.SetParameters(poi)
    CI=0.95
    plc.SetConfidenceLevel(CI)
    pl_Interval = plc.GetInterval()
    print(pl_Interval)
    #Plotting 
    plot_Interval = ROOT.RooStats.LikelihoodIntervalPlot(pl_Interval)
    plot_Interval.SetTitle("Profile Likelihood Ratio")
    plot_Interval.SetMaximum(100.)
    plot_Interval.SetRange(0,500)
    plot_Interval.Draw()
    c1.SaveAs("ProfileLikelihood.png")
    
    BModel=SBModel.Clone("BOnlyModel")
    poi.find("signal").setVal(0.001)
    BModel.SetSnapshot(poi)
    BModel.Print()
    print("Profile likelihood")
    c1 = ROOT.TCanvas("PL")



    
    
def rooPart4(doHypothesisTest=False,doAsymp=False,doFreq=False):

    fin = ROOT.TFile("WorkspaceFile.root")
    ws = fin.Get("ws")
    ws.Print()

    SBModel=ROOT.RooStats.ModelConfig()
    SBModel.SetWorkspace(ws)
    SBModel.SetPdf("sumPDF")
    SBModel.SetPdf("extPDF")
    SBModel.SetName("SBModel")

        
    poi = ROOT.RooArgSet(ws.var("signal"))#setting the parameter of interest

    SBModel.SetParametersOfInterest(poi)
    
    #for CLs (bounded intervals) use one-sided profile likelihood
    profll = ROOT.RooStats.ProfileLikelihoodTestStat(SBModel.GetPdf())
    profll.SetOneSided(1)
    observables=ROOT.RooArgSet((ws.var("mass")))#we need to define the observable for the fit
    SBModel.SetObservables(observables)
    SBModel.Print()
    
    BModel=SBModel.Clone("BOnlyModel")
    BModel.SetParametersOfInterest(poi)
    poi.find("signal").setVal(0.01)
    BModel.SetSnapshot(poi) 
    BModel.SetObservables(observables)
    BModel.Print()
   
    #define the two datasets to test:
    AllData=(ws.data("NominalSignal")) #Full dataset
    AltData=(ws.data("AltSignal"))  #With reduced signal

    print(BModel,SBModel,AllData)
    ws.Print()
    AllData.Print()
    ROOT.RooStats.AsymptoticCalculator.SetPrintLevel(2)
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
                #        inv_plot.Draw("")
                #c1.GetYAxis().SetRangeUser(0.01,10)
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
                #        inv_plot.Draw("")
                #c1.GetYAxis().SetRangeUser(0.01,10)
                c1.SaveAs("limitex"+postfix+".png")

    paramsscan_alt ={"npoints":20,"poimin":0,"poimax":500,"minplot":0.001,"maxplot":10}
    paramsscan_all ={"npoints":20,"poimin":100,"poimax":600,"minplot":0.001,"maxplot":10}
    if doFreq:
        paramsscan_alt ={"npoints":8,"poimin":0,"poimax":500,"minplot":0.001,"maxplot":10}
        paramsscan_all ={"npoints":8,"poimin":100,"poimax":600,"minplot":0.001,"maxplot":10}
    
    if(doHypothesisTest):
        #hypothesis testing: need to set both hypotheses H0 and H1:
        poi.find("signal").setVal(50)
        SBModel.SetSnapshot(poi)

    printLimits(DATA=AltData,BM=BModel,SM=SBModel,poiname="signal",signif=doHypothesisTest,asymp=doAsymp,paramsscan=paramsscan_alt,postfix="alt")

    if(doHypothesisTest):
        poi.find("signal").setVal(250)
        SBModel.SetSnapshot(poi)
    printLimits(DATA=AllData,BM=BModel,SM=SBModel,poiname="signal",signif=doHypothesisTest,asymp=doAsymp,paramsscan=paramsscan_all,postfix="all")

    npoints = 20
    poimin = 0
    poimax=500

    if doFreq==True:
        
        fc = ROOT.RooStats.FrequentistCalculator(ws.data("NominalSignal"), SBModel, BModel)
        fc.SetToys(500,250)


        calc = ROOT.RooStats.HypoTestInverter(fc)
        calc.SetConfidenceLevel(0.95)
        #use CLs
        calc.UseCLs(1)
        calc.SetVerbose(3)
        #Configure ToyMC Sampler
        
        toymcs = calc.GetHypoTestCalculator().GetTestStatSampler()
        #Use profile likelihood as test statistics 

        #set the test statistic to use for toys
        toymcs.SetTestStatistic(profll)

        print ("Doing a fixed scan  in interval : ", poimin, " , ", poimax)
        calc.SetFixedScan(npoints,poimin,poimax);

        result = calc.GetInterval() #This is a HypoTestInveter class object
        upperLimit = result.UpperLimit()
    
if __name__ == "__main__":
    if(len(sys.argv)==1):
        print("Running all parts!")
        rooPart1()
        rooPart2()
#       rooPart3()
    if(len(sys.argv)>1):
        part = int(sys.argv[1])
        if part <=1: rooPart1()
        if part ==2: rooPart2()
        if part ==3: rooPart3()
        if part ==4: rooPart4(doHypothesisTest=True)
        if part ==5: rooPart4(doAsymp=True)
        if part ==6: rooPart4(doFreq=True)
