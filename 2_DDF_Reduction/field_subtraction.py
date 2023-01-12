import subprocess
import time
from casacore.tables import table


start = time.time()

LastSelfCal_Pass = "p3"
region_file = "oj287_1800arcsec.reg"
TargetName = "OJ287"

ms_list =["L723586_121MHz_uv_pre-cal.ms","L723586_123MHz_uv_pre-cal.ms",
"L723586_125MHz_uv_pre-cal.ms","L723586_127MHz_uv_pre-cal.ms",
"L723586_129MHz_uv_pre-cal.ms","L723586_130MHz_uv_pre-cal.ms",
"L723586_132MHz_uv_pre-cal.ms","L723586_134MHz_uv_pre-cal.ms",
"L723586_136MHz_uv_pre-cal.ms","L723586_138MHz_uv_pre-cal.ms",
"L723586_140MHz_uv_pre-cal.ms","L723586_142MHz_uv_pre-cal.ms",
"L723586_144MHz_uv_pre-cal.ms","L723586_146MHz_uv_pre-cal.ms",
"L723586_148MHz_uv_pre-cal.ms","L723586_150MHz_uv_pre-cal.ms",
"L723586_152MHz_uv_pre-cal.ms","L723586_154MHz_uv_pre-cal.ms",
"L723586_156MHz_uv_pre-cal.ms","L723586_158MHz_uv_pre-cal.ms",
"L723586_160MHz_uv_pre-cal.ms","L723586_162MHz_uv_pre-cal.ms",
"L723586_164MHz_uv_pre-cal.ms","L723586_166MHz_uv_pre-cal.ms"]

DDF = "python /scratch/WORK/ebonnassieux/DDFpy3.6/sources/DDFacet/MyDDF/bin/DDF.py"
KMS = "python /scratch/WORK/ebonnassieux/DDFpy3.6/sources/killMS/MykMS/bin/kMS.py"
ClipCal = "python /scratch/WORK/ebonnassieux/DDFpy3.6/sources/killMS/MykMS/lib/python3.6/site-packages/killMS/ClipCal.py"
Breizorro = "/scratch/WORK/ebonnassieux/DDFpy3.6/bin/breizorro"
MaskDicoModel = "python /scratch/WORK/ebonnassieux/DDFpy3.6/sources/DDFacet/MyDDF/bin/MaskDicoModel.py"

chunks = [ms_list[x:x+8] for x in range(0,len(ms_list), 8)]

def getDDFPredict():
        return f"{DDF} --Data-MS ms_list.txt --Parallel-NCPU 46 " \
        f"--Image-NPix=7000 --Image-Cell 5 --Weight-Mode=Natural --Output-Also all  --Selection-UVRangeKm=0.1,30 " \
        f"--Data-ColName=CORRECTED_DATA  --Predict-ColName=WIDEFIELD_DATA --RIME-DecorrMode=FT " \
        f"--Facets-NFacets=11 --HMP-MajorStallThreshold=0.2 --HMP-Scales=[0,2,4,8,16,32] " \
        f"--Weight-ColName=IMAGING_WEIGHT --Cache-Reset=1 --Output-Mode Predict --Predict-InitDicoModel No{TargetName}.DicoModel "

def getBreizorroCommand():
        return f"{Breizorro} -r ddf_fullband_{LastSelfCal_Pass}.restored.fits -o oj287_masked.fits --subtract {region_file} -t -99999"

def getMaskDicoModelCommand():
        return f"{MaskDicoModel} --InDicoModel=ddf_fullband_{LastSelfCal_Pass}.DicoModel --OutDicoModel=No{TargetName}.DicoModel --MaskName=oj287_masked.fits"

def waitingAnimation(process):
        animation = "|/-\\"
        idx = 0
        while (process.poll() is None):
                print(animation[idx % len(animation)], end="\r")
                idx += 1
                time.sleep(0.1)

def subtractVisibilities(ms_name):
        ms = table(ms_name, readonly=False)
        name = "FIELD_SUBTRACTED_DATA"
        comment = "data after subtracting modeled visibilities for sources in the field other then target source"

        desc = ms.getcoldesc("CORRECTED_DATA")
        desc["name"] = name
        desc["comment"] = comment

        ms.addcols(desc)
        ms.putcol(name, ms.getcol("CORRECTED_DATA") - ms.getcol("WIDEFIELD_DATA"))

        ms.close()

print(f"starting field subtraction for:\n {ms_list[0][0:7]}")

#first subtract oj287 from field
with open(f"Breizorro_{LastSelfCal_Pass}.log", "w+") as f:
    process1 = subprocess.Popen(getBreizorroCommand(), shell=True, stdout=f)
print("Breizorro source subtraction running")
waitingAnimation(process1)
process1.wait()
print("Breizorro source subtraction from field done")

#MaskDicoModel
with open(f"MaskDicoModel_{LastSelfCal_Pass}.log", "w+") as f:
    process2 = subprocess.Popen(getMaskDicoModelCommand(), shell=True, stdout=f)
print("MaskDicoModel running")
waitingAnimation(process2)
process2.wait()
print("MaskDicoModel done")

#DDF Predict
with open(f"DDFPredict_{LastSelfCal_Pass}.log", "w+") as f:
    process3 = subprocess.Popen(getDDFPredict(), shell=True, stdout=f)
print("DDFPredict running")
waitingAnimation(process3)
process3.wait()
print("DDFPredict done")


#Subtract modeled visibilities of field from the observation visibilities data
for ms in ms_list:
        print(f"Subtraction of modeled visibilities running for: {ms}")
        subtractVisibilities(ms)
        print(f"Subtraction of modeled visibilities done for: {ms}")

print("COMPLETED field subtraction for all data")
print('It took', time.time()-start, 'seconds.')

## > breizorro -r ddf_154MH_p3.restored.fits -o oj287_masked.fits --subtract oj287_1800arcsec.reg -t -99999
## > MaskDicoModel --InDicoModel=ddf_154MH_p3.DicoModel --OutDicoModel=NoOJ287.DicoModel --MaskName=oj287_masked.fits


# DDF --Data-MS L723586_154MHz_uv_pre-cal_averaged.ms --Parallel-NCPU 46 --Image-NPix=28000 --Image-Cell 1.25 --Weight-Mode=Natural --Output-Also all --Data-ColName=CORRECTED_DATA  --Predict-ColName=WIDEFIELD_DATA --RIME-DecorrMode=FT --Facets-NFacets=11 --HMP-MajorStallThreshold=0.2 --HMP-Scales=[0,2,4,8,16,32] --Weight-ColName=IMAGING_WEIGHT --Output-Mode Predict --Predict-InitDicoModel NoOJ287.DicoModel --Cache-Reset=1

# DDF --Data-MS L723586_154MHz_uv_pre-cal_averaged.ms --Parallel-NCPU 46 
# --Image-NPix=7000 --Image-Cell 5 --Weight-Mode=Natural --Output-Also all 
# --Data-ColName=CORRECTED_DATA  --Predict-ColName=WIDEFIELD_DATA --RIME-DecorrMode=FT 
# --Facets-NFacets=11 --HMP-MajorStallThreshold=0.2 --HMP-Scales=[0,2,4,8,16,32] 
# --Weight-ColName=IMAGING_WEIGHT --Cache-Reset=1 --Output-Mode Predict --Predict-InitDicoModel NoOJ287.DicoModel 
