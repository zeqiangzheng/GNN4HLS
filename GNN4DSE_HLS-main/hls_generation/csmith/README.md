**Prerequisites**

Make sure that **csmith** is installed and working properly.
Copy the script *gen_csmith.py* and the custom probability file *hls_conf.txt* into some folder. The *parameters.csv* file is just a table that  summarizes our choice of parameters, it is not an active file used by our script.

**Generate C files**

Run `python3 gen_csmith.py <start_index> <end_index>`
For example: `python3 gen_csmith.py 50 149` will generate 100 C files from 000050.c to 000149.c in the c_files2/ subfolder. 

**Change parameters**

Several csmith parameters can be modified in the script *gen_csmith.py* and in the custom probability file *hls_conf.txt* file.
Our main choices are summarized in the file *parameters.csv*.

Currently the script is design to remove the particularities of the C-generated files that can't be properly handled by HLS (such as static top function etc.) It also identifies **for** loops and gives them a numbered label using regular expressions.

