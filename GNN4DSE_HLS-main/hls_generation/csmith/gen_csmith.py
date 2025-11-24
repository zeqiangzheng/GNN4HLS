# Generates C files in csmith_files/
import os
import sys
import subprocess
import re


folder = "c_files2"
namelen = 6
prefix = ""

try:
  os.mkdir(folder)
except:
  pass

start = int(sys.argv[1])
end = int(sys.argv[2])

funcs = dict()
f_index = 1
def replace_func(match_obj):
  global f_index
  f_type = match_obj.group(2)
  f_name = match_obj.group(3)
  if f_name in funcs:
    f_new_name = funcs[f_name]
  else:
    f_new_name = "fn" + str(f_index)
    f_index += 1
    funcs[f_name] = f_new_name
  return f_type + "  " + f_new_name
  
def replace_for(match_obj):
  global f_index
  s = " loop" + str(f_index) + ": for ("
  f_index += 1
  return s
 
void_to_args = ""
def comment_args(match_obj):
  global void_to_args
  full_str = match_obj.group(0)
  arg_type = match_obj.group(2)
  arg_name = match_obj.group(3)
  void_to_args += arg_type + " " + arg_name + ","   
  s = full_str[7:-2] + "; //"
  return s

for i in range(start, end + 1):
  filepath = folder + "/" + prefix + str(i).zfill( namelen ) + ".c"
  if i % 100 == 0 or i == end:
    print(filepath)

  file_ok = False
  while not file_ok:
    command = "csmith --probability-configuration hls_conf.txt --muls --divs --no-packed-struct --no-safe-math --no-embedded-assigns --no-argc --no-pointers --max-funcs 2 --max-block-depth 3 --max-array-dim 3 --max-expr-complexity 10 --concise --nomain"
    content = subprocess.getoutput(command)
  
    # removes static and rename the functions
    f_index = 1
    funcs.clear()
    content = re.sub(r"static( const | )([^ ]+)  (func_[0-9]+)", replace_func, content)
    if f_index == 1: # not good, should have been incremented up to two if fn1 exists
      continue
    
    # replaces function names with fn...
    content = re.sub(r"func_[0-9]+", lambda m: funcs[m.group(0)], content)
    
    # extracts static parameters names
    void_to_args = ""
    content = re.sub(r"static( volatile | )([^ ]+) ([^ ]+) =", comment_args, content)
    
    # replaces void parameters
    content = content.replace("fn1(void)", "fn1(" + void_to_args[:-1] + ")")
    
    # adds labels to for loops
    f_index = 1
    content = re.sub(r" for \(", replace_for, content)
    
    file_ok = True
  
  with open(filepath, "w") as f:
    f.write(content)
  
  #print(content[:9500])
  
  
  
  
  #os.system("csmith --probability-configuration hls_conf.txt --muls --divs --no-packed-struct --no-embedded-assigns --no-argc --no-pointers --max-funcs 4 --max-block-depth 2 --max-array-dim 3 --max-expr-complexity 3 --concise --nomain  | sed -E 's/static( const | )([^ ]+)  func_1\\(/\\2 fn1\\(/g' > " + filepath )
  
