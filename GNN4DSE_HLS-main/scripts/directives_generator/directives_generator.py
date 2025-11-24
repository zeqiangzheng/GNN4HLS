#!/usr/bin/python
import re

def generate_directives(c_file):
    with open(c_file) as f:
        code = f.read()
    res = re.findall('(loop[0-9]+):[\s]+for', code)
    if len(res) == 0:
        return ''
    else:
        first_loop = res[0]
        return f'set_directive_pipeline {first_loop}\n'

if __name__ == '__main__':
    path = "/mnt/shared/home/shuang91/downloads/c_files2_csmith/100000.c"
    generate_directives(path)

    # c_files = [f for f in listdir(path) if re.match('[0-9]+.c', f) and isfile(join(path, f))]
    # for c_file in c_files:
    #     print(c_file)
    #     collect_loop_info(join(path, c_file))
