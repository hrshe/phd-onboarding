import subprocess
import time

start = time.time()

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

DP3 = "/opt/lofar/DPPP/bin/DP3"

def getDP3Command(msin, msout):
    command = f"{DP3} averager.parset msin={msin} msout={msout} "
    print(f"COMMAND is: {command}")
    return 

def waitingAnimation(process):
        animation = "|/-\\"
        idx = 0
        while (process.poll() is None):
                print(animation[idx % len(animation)], end="\r")
                idx += 1
                time.sleep(0.1)

print(f"starting averaging for:\n {ms_list[0][0:7]}")

#Subtract modeled visibilities of field from the observation visibilities data
for ms in ms_list:
    msin = ms
    msout = ms[:15]+"averaged_"+ms[15:]
    with open(f"averager_{ms[8:14]}.log", "w+") as f:
        process1 = subprocess.Popen(getDP3Command(msin, msout), shell=True, stdout=f)
    print(f"averaging running for: {ms}")
    waitingAnimation(process1)
    process1.wait()
    print(f"averaging done for: {ms}")

print("COMPLETED averaging for all data")
print('It took', time.time()-start, 'seconds.')