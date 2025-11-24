 
open_project -reset pl_vecadd_zedboard_hls
set_top pl_vecadd
add_files pl_vecadd.cpp  -cflags "-std=c++0x"

open_solution -reset "solution1"
set_part {xc7z020clg484-1}
create_clock -period 100.0MHz

# csim_design

csynth_design
export_design -format ip_catalog -version "1.0"

exit
