
import glob
import os
import time

lFiles=[f.strip() for f in open("html.txt","r").readlines()]

def OS(ss):
    print(ss)
    os.system(ss)

def Print(ss):
    print(" "*200, end="\r")
    print(ss, end="\r")
    #print(ss)
    
def test():
    logFile="allout.txt"
    for fName in lFiles:
        print("=============================================")
        fName0=fName.split("/")[-1]
        ok=False
        if os.path.isfile("%s.done"%fName0):
            print("Already downloaded %s"%fName)
            continue
        
        cmd="rm -rf wget-log* %s; wget %s > allout.txt 2>&1 &"%(logFile,fName)
        
        dtmax=60
        dtstep=1
        t0=time.time()
        LineT0=None
        OK=False
        time.sleep(dtstep)
        Start=True
        while not OK:
            if Start:
                LWait=""
                t0=time.time()
                OS(cmd)
                time.sleep(dtstep)
                Start=False
            
            with open(logFile,"r") as f:
                L=f.readlines()
                for l in L:
                    if "saved" in l:
                        print("Successfully downloaded %s"%fName)
                        OS("touch %s.done"%fName0)
                        OK=True
                if OK:
                    break
                
                if len(L)>0:
                    LineT1=L[-1].strip()
                else:
                    time.sleep(dtstep)
                    continue

                if len(L)>1:
                    LineT1=L[-2].strip()
                
                if LineT1!=LineT0:
                    LineT0=LineT1
                    t0=time.time()
                        
                    if not OK:
                        Print(LineT1)
                        time.sleep(dtstep)
                elif time.time()-t0>dtmax:
                    print()
                    print("start over again")
                    os.system("pkill -9 wget")
                    Start=True
                else:
                    LWait+="."
                    Print("[%s] unchanged, wait %s"%(logFile,LWait))
                    #print("Wait more")
                    time.sleep(dtstep)
                    
                
if __name__=="__main__":
    test()
