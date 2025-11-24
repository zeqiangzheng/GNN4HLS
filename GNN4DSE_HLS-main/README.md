# GNN4HLS: Graph Neural Network for High-Level Synthesis Modeling and Design Space Exploration

## Software Versions

Xilinx Vitis 2021.1, can be downloaded from this [link](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vitis.html). 

Note: before version 2021.1, the high-level synthesis (HLS) tool from Xilinx is called Vivado HLS. Starting version 2021.1, HLS tool is renamed to Vitis HLS. 


## Running Vitis HLS and Vivado in Command Line
You can use `run_hls.tcl` and `run_vivado.tcl` to invoke Vivado HLS and Vivado in command line. 
- Script: `scripts/run_hls.tcl` and `scripts/run_vivado.tcl`
- Usage: Before running these script, update the configurations in the scripts accordingly.  

Run Vitis HLS: 
```bash
vitis_hls -f run_hls.tcl
```

Run Vivado: 
```bash
vivado -mode batch -source run_vivado.tcl
```

## Extract Information from Vitis HLS report
After running Vitis HLS, use this script `report_extract.py` to extract resource utilization and latency information from Vitis HLS report. 

- Script: `scripts/report_extract.py`
- Usage: Inside `report_extract.py`, set `top_func` to your top function name and `prj_path` to the absolute path of your Vitis HLS project. 

```bash
python3 report_extract.py
```

## Target FPGAs
| FPGA Board  | FPGA Device          |
| ----------- | -------------------- |
| ZedBoard    | xc7z020clg484-1      |
| Ultra96     | xczu3eg-sbva484-1-e  |
| Alveo U250  | xcu250-figd2104-2L-e |


Tutorial video on how to work with HLS report automation scripts:
https://drive.google.com/file/d/16w2hpgL72RUQGO8Dc9oNW9YjdAOcbCE6/view?usp=sharing
