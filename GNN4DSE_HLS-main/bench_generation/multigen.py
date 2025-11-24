import os
import sys
import time
from datetime import datetime

now = datetime.now()
now_str = now.strftime("%Y-%m-%d_%Hh%Mm%S")

# Usage for 10 processes: python3 multigen3.py 10000 10099 10
from_index = int(sys.argv[1])
to_index = int(sys.argv[2])
num_processes = int(sys.argv[3])

try:
  os.mkdir("temp")
except:
  pass
  
try:
  os.mkdir("temp/processes")
except:
  pass

pidlogfile = "temp/processes/" + now_str + ".txt"
with open(pidlogfile, "w") as f:
  f.write(" ".join(sys.argv) + "\n")

for i in range(num_processes):
  from_index2 = from_index + i
  if from_index2 > to_index:
    break
  print("\n\n======= Process " + str(i) + " =======\n")
  s = "nohup python3 autogen3.py " + str(from_index2) + " " + str(to_index) + " >/dev/null &"
  print(s + "\n")
  os.system(s + " echo $! >> " + pidlogfile )
  print("Process IDs logged in " + pidlogfile + "\n")
  time.sleep(1)
  