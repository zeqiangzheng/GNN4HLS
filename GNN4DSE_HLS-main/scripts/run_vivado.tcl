
create_project pl_vecadd_zedboard_vivado /home/shuang91/pylog_projects/pl_vecadd/pl_vecadd_zedboard_vivado -part xc7z020clg484-1

set_property board_part    em.avnet.com:zed:part0:1.4 [current_project]
set_property ip_repo_paths /home/shuang91/pylog_projects/pl_vecadd/pl_vecadd_zedboard_hls/solution1 [current_project]
update_ip_catalog

create_bd_design "design_1"
update_compile_order -fileset sources_1

create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7_0

apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 -config {make_external "FIXED_IO, DDR" apply_board_preset "1" Master "Disable" Slave "Disable" }  [get_bd_cells processing_system7_0]

set_property -dict [list CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {100.0}  CONFIG.PCW_USE_S_AXI_HP0 {1} CONFIG.PCW_USE_S_AXI_HP1 {1} CONFIG.PCW_USE_S_AXI_HP2 {1} ] [get_bd_cells processing_system7_0]


create_bd_cell -type ip -vlnv xilinx.com:hls:pl_vecadd:1.0 pl_vecadd_0


apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/pl_vecadd_0/m_axi_data0} Slave {/processing_system7_0/S_AXI_HP0} intc_ip {Auto} master_apm {0}}  [get_bd_intf_pins processing_system7_0/S_AXI_HP0]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/pl_vecadd_0/m_axi_data1} Slave {/processing_system7_0/S_AXI_HP1} intc_ip {Auto} master_apm {0}}  [get_bd_intf_pins processing_system7_0/S_AXI_HP1]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/pl_vecadd_0/m_axi_data2} Slave {/processing_system7_0/S_AXI_HP2} intc_ip {Auto} master_apm {0}}  [get_bd_intf_pins processing_system7_0/S_AXI_HP2]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/processing_system7_0/M_AXI_GP0} Slave {/pl_vecadd_0/s_axi_ctrl} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins pl_vecadd_0/s_axi_ctrl]

validate_bd_design
save_bd_design

make_wrapper -files [get_files /home/shuang91/pylog_projects/pl_vecadd/pl_vecadd_zedboard_vivado/pl_vecadd_zedboard_vivado.srcs/sources_1/bd/design_1/design_1.bd] -top

add_files -norecurse /home/shuang91/pylog_projects/pl_vecadd/pl_vecadd_zedboard_vivado/pl_vecadd_zedboard_vivado.srcs/sources_1/bd/design_1/hdl/design_1_wrapper.v
launch_runs impl_1 -to_step write_bitstream -jobs 4

wait_on_run impl_1
