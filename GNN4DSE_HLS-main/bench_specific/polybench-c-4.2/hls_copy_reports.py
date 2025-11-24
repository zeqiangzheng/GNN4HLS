import os
import distutils.dir_util

prj = "HLS_projects"
rep = "HLS_reports"

try:
    os.mkdir(rep)
except FileExistsError:
    pass

# to do after:  cp * -r --parents ../../../../Reports/

names = os.listdir(prj)
for name in names:
    path2 = prj + "/" + name
    name2 = "PolyBench+" + name
    if os.path.isdir(path2):
            path2 += "/solution1"
            from_dir = path2 + "/syn/report"
            to_dir = rep + "/" + name2 + "/report"
            distutils.dir_util.copy_tree(from_dir, to_dir)

            from_dir = path2 + "/impl/report/verilog"
            to_dir = rep + "/" + name2 + "/verilog"
            distutils.dir_util.copy_tree(from_dir, to_dir)

            from_dir = path2 + "/.autopilot/db/dot"
            to_dir = rep + "/" + name2 + "/dot"
            distutils.dir_util.copy_tree(from_dir, to_dir)

            from_dir = path2 + "/.autopilot/db/dot-post"
            to_dir = rep + "/" + name2 + "/dot-post"
            distutils.dir_util.copy_tree(from_dir, to_dir)

