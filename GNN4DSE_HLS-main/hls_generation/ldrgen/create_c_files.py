import os
runs = 100000
for i in range(57356, runs):
  os.system("frama-c -ldrgen > c_files2/" + str(i).zfill(len(str(runs-1))) + ".c")
  print(i, end =" ")