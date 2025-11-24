import os
import sys
import csv
import string
import random
from datetime import datetime
from shutil import copyfile, rmtree
from hls_timing_parser import extract_hls_timing
from rtl_timing_parser import extract_rtl_timing
from adb_parser_modified import parse
import time

# Usage: nohup python3 autogen3.py 10000 10099 >/dev/null &
from_index = int(sys.argv[1])
to_index = int(sys.argv[2])

# --- Modify below based on configuration ---
delete_project = True  # deletes the heavy Vitis project folder
delete_adb = True
delete_timing_xml = True
c_folder = "c_files2"
c_namelen = 5  # C filenames are 5 character-long e.g. 00733.c
hls_cmd = "vitis_hls"
min_c_lines = 11  # we will exclude C files that have <= 11 lines
target_board = "xc7z020clg484-1"
# -------------------------------------------

hls_timing_fields = "benchmark,dsp,ff,lut,bram,dsp_avail,ff_avail,lut_avail,bram_avail,dsp_perc,ff_perc,lut_perc,bram_perc,period,avg_latency".split(',')
rtl_timing_fields = "benchmark,dsp,ff,lut,bram,dsp_avail,ff_avail,lut_avail,bram_avail,dsp_perc,ff_perc,lut_perc,bram_perc,period".split(',')

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

folder = "output"
tmp = "temp"
error_path = tmp + "/errors"
  
for p in [folder, tmp, error_path]:
  try:
    os.mkdir(p)
  except:
    pass

for i in range(from_index, to_index+1): 
  project = str(i).zfill( c_namelen )
    
  # Checking C file
  c_file = c_folder + "/" + project + ".c"
  if os.path.exists(c_file):
    print("Fetching C file: " + c_file + " (OK)")
    f = open(c_file, "r+")
    lines = f.readlines()
    num_lines = len(lines)
    stop_outer = False
    rewrite_file = False
    if num_lines <= min_c_lines:
      print("Skipping " + project + ".c because <= 11 lines")      
      continue
    for i in range(num_lines):
      line = lines[i]
      if line[:7] == "extern ":  # for 'extern' synthesis error
        lines[i] = "       " + line[7:]  # to avoid altering filesize
        print("Removing 'extern' prefix from line " + str(i) + " in " + project + ".c" )
        rewrite_file = True          
      if line[-11:] == " fn1(void)":
        stop_outer = True
        break
    if rewrite_file:
      f.seek(0,0)
      f.writelines(lines)
    f.close()
    if stop_outer:
      print("Skipping " + project + ".c because fn1(void) (no argument)")
      continue
        
  else:
    print("C file not found: " + c_file + " (STOPPING)")
    break
  
  path = folder + "/" + project
  tmp_prj = tmp + "/" + project
  
  if os.path.isdir(path) or os.path.isdir(tmp_prj):
    print("Skipping " + project + " (folder exists already)")
    continue  # try next index
  
  if os.path.isfile(error_path + "/" + project + ".log"):
    print("Skipping " + project + " (error file exists already)")
    continue  # try next index  
  
  os.mkdir(tmp_prj)
  
  # Writes the TCL file
  tcl_path = tmp_prj + "/run.tcl"
  print("Creating TCL file: " + tcl_path)
  tcl = open(tcl_path, "w")
  tcl.write("open_project " + project + "\n")
  tcl_pos = tcl.tell()  
  tcl.write("set_top fn1\n")
  tcl.write('add_files "../' + c_file + '"\n')  
  tcl.write('open_solution "solution"\n')
  tcl.write('set_part {' + target_board + '}\n')
  tcl.write('create_clock -period 10 -name default\n')
  tcl.write('csynth_design -dump_cfg -dump_post_cfg\n')  # we only do HLS synthesis at first
  #export_design -flow impl
  # Ensures the TCL file is updated (but not closed yet)
  tcl.flush()
  os.fsync(tcl.fileno())
  
  # Run the HLS synthesis first
  print("Running TCL file (HLS syn.): " + hls_cmd + " " + tcl_path)
  start = time.time()
  log_path = tmp_prj + "/vitis_hls.log"
  
  os.chdir(tmp)  # calls vitis from the "temp" folder
  if os.system(hls_cmd + " ../" + tcl_path + " -l ../" + log_path) != 0:
    print("Error during HLS syn of " + project)  
    tcl.close()  # an error occurred
    os.chdir("..")
    # keep only the last 250 lines of the log file and store them in 'errors' folder
    os.system("tail -n 250 " + log_path + " > " + error_path + "/" + project + ".log")
    rmtree(tmp_prj)
    continue
  
  #input("PRESS TO CONTINUE -- change the XML timing report in the meantime!!!")
  
  # check the HLS timing estimates, no "temp" needed because we are inside the folder
  hls_timing_tmp_path = project + "/solution/syn/report/fn1_csynth.xml"
  hls_timing = (project,) + extract_hls_timing(hls_timing_tmp_path)
  
  # if any utilization is higher than the available resources we will NOT do RTL impl
  x1 = hls_timing[9]
  x2 = hls_timing[10]
  x3 = hls_timing[11]
  x4 = hls_timing[12]
  if x1 > 1 or x2 > 1 or x3 > 1 or x4 > 1 or (x1 == 0 and x2 == 0 and x3 == 0 and x4 == 0):
    print("Error: zero or over-utilization, will NOT do RTL impl of " + project)
    tcl.close()
    os.chdir("..")
    # keep only the last 250 lines of the (HLS) log file and store them in 'errors' folder
    os.system("tail -n 250 " + log_path + " > " + error_path + "/" + project + ".log")
    rmtree(tmp_prj)
    continue
  
  middle = time.time()
  
  # update the TCL file to replace HLS synthesis by RTL impl
  tcl.truncate(tcl_pos)
  tcl.seek(tcl_pos)
  tcl.write('\nopen_solution "solution"\n')
  tcl.write('set_part {' + target_board + '}\n')
  tcl.write('create_clock -period 10 -name default\n')  
  tcl.write('export_design -flow impl\n')
  # Ensures the TCL file is updated (but not closed yet)
  tcl.flush()
  os.fsync(tcl.fileno())
  
  # Now we can run RTL implementation
  print("Running TCL file (RTL impl.): " + hls_cmd + " " + tcl_path)
  if os.system(hls_cmd + " ../" + tcl_path + " -l ../" + log_path) != 0:
    print("Error during RTL implementation of " + project)  
    tcl.close()  # an error occurred
    os.chdir("..")
    # keep only the last 250 lines of the log file and store them in 'errors' folder
    os.system("tail -n 250 " + log_path + " > " + error_path + "/" + project + ".log")
    rmtree(tmp_prj)
    continue
  
  os.chdir("..")
  end = time.time()
  elapsed1 = int(middle-start)
  elapsed2 = int(end-middle)
  elapsed = int(end-start)
  
  tcl.write("\n")
  tcl.write("# Start: " + time.asctime(time.localtime(start)) + "\n")  
  tcl.write("# Target board: " + target_board + "\n")
  tcl.write("# HLS synthesis duration: " + str(int(elapsed1/60)) + " minutes " + str(elapsed1 % 60) + " seconds\n")    
  tcl.write("# RTL implementation duration: " + str(int(elapsed2/60)) + " minutes " + str(elapsed2 % 60) + " seconds\n")
  tcl.write("# Total duration: " + str(int(elapsed/60)) + " minutes " + str(elapsed % 60) + " seconds\n")
  tcl.write("# End: " + time.asctime(time.localtime(end)))    
  tcl.write("\n")
  tcl.write("# " + target_board + " " + str(elapsed1) + " " + str(elapsed2) + " " + str(elapsed))
    
  tcl.close()
  
  # Create the output project folder (should not exist yet)
  os.mkdir(path)
  
  # Extract the relevant project files
  print("Copying relevant project files to: " + path)
  
  # TCL file (contains device and elapsed time information)
  src = tmp_prj + "/run.tcl"
  dst = path + "/run.tcl"           
  copyfile(src, dst)
  
  # ABD file (contains graph information)
  src = tmp_prj + "/solution/.autopilot/db/fn1.adb"
  dst = path + "/fn1.adb"           
  copyfile(src, dst)
  
  # HLS timing estimates
  src = tmp_prj + "/solution/syn/report/fn1_csynth.xml"
  hls_timing_path = path + "/hls_timing.xml"           
  copyfile(src, hls_timing_path)  
  
  # RTL timing
  src = tmp_prj + "/solution/impl/report/verilog/export_impl.xml"
  rtl_timing_path = path + "/rtl_timing.xml"           
  copyfile(src, rtl_timing_path)
  
  # Extract timing reports, both in the 'output' folder and in the project subfolder 
  print("Extracting HLS and RTL timing files...")
  #already extracted before... hls_timing = (project,) + extract_hls_timing(hls_timing_path)
  rtl_timing = (project,) + extract_rtl_timing(rtl_timing_path)
    

    
  # Timing CSV files (at the root of all benchmarks) ==========================
  # NEW: relocate inside the loop to avoid conflicts when multithreading (multigen.py)
  hls_report_exists = os.path.exists(folder + '/HLS_report.csv')
  rtl_report_exists = os.path.exists(folder + '/RTL_report.csv')
  
  hls_file = open(folder + '/HLS_report.csv', mode='a' if hls_report_exists else 'w')
  rtl_file = open(folder + '/RTL_report.csv', mode='a' if rtl_report_exists else 'w')

  hls_csv = csv.writer(hls_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  rtl_csv = csv.writer(rtl_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

  if not hls_report_exists:
    hls_csv.writerow(hls_timing_fields)
  if not rtl_report_exists:
    rtl_csv.writerow(rtl_timing_fields)
    
  hls_csv.writerow(hls_timing)
  rtl_csv.writerow(rtl_timing)    
    
  hls_file.close()
  rtl_file.close()    
  # ==============================================================================  
  
  hls_file2 = open(path + '/HLS_report.csv', mode='w')
  hls_csv2 = csv.writer(hls_file2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  hls_csv2.writerow(hls_timing_fields)
  hls_csv2.writerow(hls_timing)
  hls_file2.close()
  
  rtl_file2 = open(path + '/RTL_report.csv', mode='w')
  rtl_csv2 = csv.writer(rtl_file2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  rtl_csv2.writerow(rtl_timing_fields)  
  rtl_csv2.writerow(rtl_timing)  
  rtl_file2.close()
  

  # Extract ADB graph information
  args = dotdict({'json': True, 'pickle': False,
    'out_npy': path + '/adj_matrix.npy',
    'out_csv': path + '/node_features.csv'})
  print('Parsing ' + path + '/fn1.adb')
  parse(path + '/fn1.adb', args, path + '/')
  

  # cleans up heavy project files
  if delete_project:
    print("Deleting project folder: " + tmp_prj)
    rmtree(tmp_prj)
  if delete_adb:
    os.remove(path + '/fn1.adb')
  if delete_timing_xml:
    os.remove(path + "/hls_timing.xml")
    os.remove(path + "/rtl_timing.xml")
  

  # Ensures the timing files at the root are updated (but not closed yet)
  # NEW: lines below are now useless since we open/close the files inside the loop
  #hls_file.flush()
  #os.fsync(hls_file.fileno())
  #rtl_file.flush()
  #os.fsync(rtl_file.fileno())


