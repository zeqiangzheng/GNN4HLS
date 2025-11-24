import os

categories = [
   'linear-algebra/blas',
   'linear-algebra/kernels',
   'linear-algebra/solvers',
   'datamining',
   'stencils',
   'medley' ]

try:
    os.mkdir("HLS_projects")
except FileExistsError:
    pass

lst = []

for category in categories:
    path = "./" + category
    directories = os.listdir(path)
    for directory in directories:
        path2 = path + "/" + directory  # linear-algebra/blas/gemm
        if os.path.isdir(path2) == True:
            # reads raw source: *.c
            lst.append(directory)
            print(directory)
            f = open(path2 + "/" + directory + ".c")
            content = f.read()
            f.close()
            
            # writes modified source (without the prefix static): *-non-static.c
            content2 = content.replace("static\nvoid kernel", "//static\nvoid kernel")
            cpath = path2 + "/" + directory + "-non-static.c"
            f2 = open(cpath, "w")
            f2.write(content2)
            f2.close()
            
            # writes the TCL file
            tcl_path = "./HLS_projects/" + "run_" + directory + ".tcl"
            tcl = open(tcl_path, "w")
            tcl.write("open_project " + directory + "\n")
            tcl.write("set_top " + "kernel_" + directory.replace("-", "_") + "\n")
            tcl.write('add_files "' + '.' + cpath + '" -cflags "-I ../utilities'\
                      + ' -I .' + path2 + ' -DPOLYBENCH_STACK_ARRAYS -DMINI_DATASET"' + '\n')
            tcl.write('''open_solution "solution1"
 set_part {xc7z020clg484-1}
 create_clock -period 10 -name default
 #csim_design
 csynth_design -dump_cfg -dump_post_cfg
 export_design -flow impl
 #cosim_design''')
            tcl.close()

print()
os.chdir("HLS_projects")
for benchmark in lst:
    tcl_path = "run_" + benchmark + ".tcl"
    #answer = input("Press Enter to run " + tcl_path + " (or 'no' to exit): ")
    #if answer != "":
    #    quit()
    os.system("vitis_hls " + tcl_path)




