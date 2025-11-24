import os
import distutils.dir_util
from shutil import copyfile

prj = "HLS_projects"
rep = "HLS_reports"

try:
    os.mkdir(rep)
except FileExistsError:
    pass

names = os.listdir(prj)
for name in names:
    path2 = prj + "/" + name
    name2 = "PolyBench+" + name
    topName = "kernel_" + name.replace("-", "_")
    if os.path.isdir(path2):
            path2 += "/solution1"
            
            src = path2 + "/.autopilot/db/" + topName + ".adb"
            dst = rep + "/" + name2 + "/" + topName + ".adb"           
            copyfile(src, dst)

            src = path2 + "/.autopilot/db/" + topName + ".adb.xml"
            dst = rep + "/" + name2 + "/" + topName + ".adb.xml"           
            copyfile(src, dst)            
            
            
            #from_dir = path2 + "/.autopilot/db/dot"
            #to_dir = rep + "/" + name2 + "/dot"
            #distutils.dir_util.copy_tree(from_dir, to_dir)
            
            #from_dir = path2 + "/syn/report"
            #to_dir = rep + "/" + name2 + "/report"
            #distutils.dir_util.copy_tree(from_dir, to_dir)

            #from_dir = path2 + "/impl/report/verilog"
            #to_dir = rep + "/" + name2 + "/verilog"
            #distutils.dir_util.copy_tree(from_dir, to_dir)
            
            
            #from_dir = path2 + "/.autopilot/db/dot"
            #to_dir = rep + "/" + name2 + "/dot"
            #distutils.dir_util.copy_tree(from_dir, to_dir)

            #from_dir = path2 + "/.autopilot/db/dot-post"
            #to_dir = rep + "/" + name2 + "/dot-post"
            #distutils.dir_util.copy_tree(from_dir, to_dir)

