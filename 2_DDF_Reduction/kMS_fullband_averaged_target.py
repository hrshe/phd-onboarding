import subprocess
import time
start = time.time()

ms_list =["L723586_121MHz_averaged_uv_pre-cal.ms","L723586_123MHz_averaged_uv_pre-cal.ms","L723586_125MHz_averaged_uv_pre-cal.ms",
"L723586_127MHz_averaged_uv_pre-cal.ms","L723586_129MHz_averaged_uv_pre-cal.ms","L723586_130MHz_averaged_uv_pre-cal.ms",
"L723586_132MHz_averaged_uv_pre-cal.ms","L723586_134MHz_averaged_uv_pre-cal.ms","L723586_136MHz_averaged_uv_pre-cal.ms",
"L723586_138MHz_averaged_uv_pre-cal.ms","L723586_140MHz_averaged_uv_pre-cal.ms","L723586_142MHz_averaged_uv_pre-cal.ms",
"L723586_144MHz_averaged_uv_pre-cal.ms","L723586_146MHz_averaged_uv_pre-cal.ms","L723586_148MHz_averaged_uv_pre-cal.ms",
"L723586_150MHz_averaged_uv_pre-cal.ms","L723586_152MHz_averaged_uv_pre-cal.ms","L723586_154MHz_averaged_uv_pre-cal.ms",
"L723586_156MHz_averaged_uv_pre-cal.ms","L723586_158MHz_averaged_uv_pre-cal.ms","L723586_160MHz_averaged_uv_pre-cal.ms",
"L723586_162MHz_averaged_uv_pre-cal.ms","L723586_164MHz_averaged_uv_pre-cal.ms","L723586_166MHz_averaged_uv_pre-cal.ms"]

DDF = "python /scratch/WORK/ebonnassieux/DDFpy3.6/sources/DDFacet/MyDDF/bin/DDF.py"
KMS = "python /scratch/WORK/ebonnassieux/DDFpy3.6/sources/killMS/MykMS/bin/kMS.py"
ClipCal = "python /scratch/WORK/ebonnassieux/DDFpy3.6/sources/killMS/MykMS/lib/python3.6/site-packages/killMS/ClipCal.py"

chunks = [ms_list[x:x+8] for x in range(0,len(ms_list), 8)]

def getKMSCommand(ms_name):
        return f"{KMS} --MSName {ms_name} --InCol DATA --OutCol TARGET_CORRECTED_DATA --DicoModel OJ287.DicoModel --UVMinMax=0.1,2000 --NCPU 8 --SolverType CohJones --dt 0.5 --PolMode IFull --NChanSols 4 --NIterLM 8 --ApplyToDir 0 --ApplyMode P"

def getClipCalCommand(ms_name):
        return f"{ClipCal} --MSName {ms_name} --Th 8 --ColName TARGET_CORRECTED_DATA  --WeightCol=IMAGING_WEIGHT"

for ms_iter in range(int(len(ms_list)/3)):
    print(f"starting kMS for:\n {chunks[0][ms_iter]} \n{chunks[1][ms_iter]} \n{chunks[2][ms_iter]}")

    with open(f"kMS_{chunks[0][ms_iter][8:15]}target_p0.log", "w+") as f:
        process1 = subprocess.Popen(getKMSCommand(chunks[0][ms_iter]), shell=True, stdout=f)
    with open(f"kMS_{chunks[1][ms_iter][8:15]}target_p0.log", "w+") as f:
        process2 = subprocess.Popen(getKMSCommand(chunks[1][ms_iter]), shell=True, stdout=f)
    with open(f"kMS_{chunks[2][ms_iter][8:15]}target_p0.log", "w+") as f:
        process3 = subprocess.Popen(getKMSCommand(chunks[2][ms_iter]), shell=True, stdout=f)

    process1.wait()
    process2.wait()
    process3.wait()

   # with open(f"ClipCal_{chunks[0][ms_iter][8:15]}p3.log", "w+") as f:
   #     process1 = subprocess.Popen(getClipCalCommand(chunks[0][ms_iter]), shell=True, stdout=f)
   # with open(f"ClipCal_{chunks[1][ms_iter][8:15]}p3.log", "w+") as f:
   #     process2 = subprocess.Popen(getClipCalCommand(chunks[1][ms_iter]), shell=True, stdout=f)
   # with open(f"ClipCal_{chunks[2][ms_iter][8:15]}p3.log", "w+") as f:
   #     process3 = subprocess.Popen(getClipCalCommand(chunks[2][ms_iter]), shell=True, stdout=f)

    #process1.wait()
    #process2.wait()
    #process3.wait()
    print(f"Completed kMS:\n {chunks[0][ms_iter]} \n{chunks[1][ms_iter]} \n{chunks[2][ms_iter]}")

print("COMPLETED full band calibration")
print('It took', time.time()-start, 'seconds.')
