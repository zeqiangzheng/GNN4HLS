**Prerequisites**

These 4 scripts must be placed in the directory containing the properly-prepared benchmark folders.
Each prepared benchmark folder MUST be composed of different subfolders and files taken from the relevant Vitis project folder:

- <Benchmark+Name/>
  - dot/
  - dot-post/
  - report/
  - verilog/
  - <top_function>.adb
  - <top_function>.adb.xml

These directories can be pasted manually from the relevant Vitis project folder, or copied automatically through scripts (see for instance our scripts for PolyBench in ../).

Google Drive (and soon the NAS) contains the set of such "properly prepared" benchmark directories in *HLS_reports/*

**Usage**

Simply call `python3 io_extract.py`. It needs the 3 other scripts to be present in the same folder.

This script will extract the relevant information from each benchmark, and create an GNN_IO/ output folder containing several benchmark folders.
Each benchmark folder will contain 3 files:
- adj_matrix.npy
- graph_dic.json
- node_features.csv

GNN_IO/ will also contain two summary CSV files: HLS_report.csv and RTL_report.csv.
Google Drive (and soon the NAS) contains the output of this worflow for standard benchmarks in *GNN_IO/*

