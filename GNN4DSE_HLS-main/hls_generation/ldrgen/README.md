**Prerequisites**

Installing Frama-C and ldrgen first.
The installation process is cumbersome, we had to set up a dedicated Debian machine on Google Compute Engine just for this task.
If necessary, I will send you an image of this instance.

**Generating C files**

The usual command to generate a C file is:
`frama-c -ldrgen > <folder/> <filename.c>`

The default parameters suit our needs well. The script *create_c_files.c* is merely doing this in a loop, and can be greatly improved (e.g. parallel processes etc.).
Make sure to edit it before launch, to set the start index and the number of runs manually.
