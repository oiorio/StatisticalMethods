import ROOT
import sys

def rooPart1():
    print("Doing part 1: definition and basics")
    #Part 1.1: definitions

    #Fit variable: you define the random variable
    mass = ROOT.RooRealVar("mass","mass plot",0,1000,"GeV")  

    nsignal=250
    nbackground=1000

    #Variables
    signal = ROOT.RooRealVar("signal","signal events",nsignal,0,2000) 
    background = ROOT.RooRealVar("background","signal events",nbackground,0,2000) 

    mean = ROOT.RooRealVar("mean","signal mean",200,0,1000)
    sigma = ROOT.RooRealVar("sigma","signal sigma",50,0,1000) 
    lam = ROOT.RooRealVar("lam","lam",-0.01,-5,0)

    #We define two pdfs which are already included in the ROOT libraries   

    BkgShape = ROOT.RooExponential("expo","Roofit Exponential function",mass,lam)#Background exponential pdf, already normalized  
    SigShape = ROOT.RooGaussian("gauss","Roofit Gaussian function",mass, mean,sigma)#Signal gaussian pdf, already normalized

    #Part 1.2: generation let's for example generate from the MC we have:

    AllEvents = SigShape.generate(ROOT.RooArgSet(mass),nsignal)
    BackgroundEvents = BkgShape.generate(ROOT.RooArgSet(mass),nbackground)
    AllEvents.append(BackgroundEvents)

    BinnedEvents=AllEvents.binnedClone()

    #Plotting routines
    frame = mass.frame(ROOT.RooFit.Title("mass distribution"))
    c1=ROOT.TCanvas()
    AllEvents.plotOn(frame)
    BinnedEvents.plotOn(frame)
    frame.Draw()
    c1.SaveAs("exampleEvents.png")

    #Part 1.3: define the extended maximum likelihood

    sum_pdf = ROOT.RooAddPdf("sumPDF","Total s+b PDF",ROOT.RooArgList(SigShape,BkgShape),ROOT.RooArgList(signal,background))

    sum_pdf.fitTo(AllEvents, ROOT.RooFit.Extended(1))

    sum_pdf.plotOn(frame)
    frame.Draw()
    c1.SaveAs("exampleFit.png")

    #Ez pz lemon squeezy!

    #Now let's use some tools for 1) fit robustness checks and 2) limit setting!

    #Part 1.4: building a workspace
    #A convenient way to "Dock" your data and models is via the workspaces:

    
    w = ROOT.RooWorkspace("ws")
    getattr(w,'import')(AllEvents)
    getattr(w,'import')(sum_pdf)
    
    w.Print()

    fout = ROOT.TFile("WorkspaceFile.root","RECREATE")
    w.Write()
    fout.Close()

def rooPart2():
    print("Doing part 2: fit sanity checks")
    #Part 2.1: let's extract the workspace!
    fin = ROOT.TFile("WorkspaceFile.root")
    ws = fin.Get("ws")#NOTE: Root saves files with the "Name" field!!!
    ws.Print()
    
    #Now let's make the pseudoexperiments:
    mc_study = ROOT.RooMCStudy(ws.pdf("sumPDF"), ROOT.RooArgSet(ws.var("mass")), ROOT.RooFit.Extended(1), ROOT.RooFit.FitOptions(ROOT.RooFit.Save(1) ))
    mc_study.generateAndFit(1000)

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


if __name__ == "__main__":
    if(len(sys.argv)==1):
        print("Running all parts!")
        rooPart1()
        rooPart2()
    if(len(sys.argv)>1):
        part = int(sys.argv[1])
        if part <=1: rooPart1()
        if part ==2: rooPart2()
