**Prerequisites**

Make sure you always use the latest scripts from the folder:
  - multigen.py (script to directly launch parallel processes of autogen3)
  - autogen3.py (creates TCL files, runs HLS, then RTL, extract benchmarks) 
  - adb_parser_modified.py (graph extraction for ADB files, based on Sitao's v1)
  - hls_timing_parser.py (HLS timing and resource extraction from an xml file)
  - rtl_timing_parser.py (RTL timing  and resource  extraction from an xml file)

These 5 scripts should reside in the same folder. Your C files should be sitting in the subfolder **c_files2/**

**Generating the benchmarks**

You can run the (single process) generation by using the following command:
`python3 autogen3.py <from> <to>`
For example: `python3 autogen3.py 10000 10099`

To make it run in the background:
`nohup python3 autogen3.py 10000 10099 >/dev/null &`

You can run many processes in parallel by using the following command:
`python3 multigen.py <from> <to> <num_of_parallel_process>`
For example: `python3 multigen.py 50000 50099 10`
  
This command would generate benchmarks from 50000 until 50099 (i.e. 100 benchmarks in total) using 10 parallel processes (nohup is used under the hood). The "clean" benchmarks are now progressively filling the output/ folder, while all temporary and error files are in temp/
The benchmark generation process has been improved to avoid launching the RTL implementation of benchmarks whose HLS synthesis already predicts an over-utilization of resources. This will skip many benchmarks, but saves *a lot* of CPU time. 

**Important**

If you use multiple processes in parallel, you may need to rebuild your two summary CSV files at the end by using the script 'rebuild_csv_reports.py' (see folder ../bench_merging). The autogen3.py script will be modified later to avoid this kind of issues in the summary file.

**Customization**

You can modify *autogen3.py* to specify some parameters such as:
- delete_project = True  # deletes the heavy Vitis project folder
- delete_adb = True
- delete_timing_xml = True
- c_folder = "c_files2"
- c_namelen = 5  # C filenames are 5 character-long e.g. 00733.c
- hls_cmd = "vitis_hls"
- min_c_lines = 11  # we will exclude C files that have <= 11 lines
- target_board = "xc7z020clg484-1"
