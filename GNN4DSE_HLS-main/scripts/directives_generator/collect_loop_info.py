#!/usr/bin/python
import re
from os import listdir
from os.path import isfile, join
from pycparser import c_parser
from pycparser import c_ast

class ASTVisitor:

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node)

    def generic_visit(self, node):
        if node is None:
            return ''
        else:
            for c in node:
                self.visit(c)

    def visit_Label(self, node):
        start_lineno = node.coord.line
        
        # print(node.stmt.stmt)
        curr = node.stmt.stmt
        while isinstance(curr, c_ast.Compound):
            if curr.block_items is None:
                break
            curr = curr.block_items[-1]
            if isinstance(curr, c_ast.Label):
                curr = curr.stmt.stmt
        # print(curr)
        end_lineno = curr.coord.line
        print(f"{node.name}: {start_lineno}-{end_lineno}")
        self.visit(node.stmt)

def preprocess(code):
    code = re.sub('#[^\n]+', '', code)
    code = re.sub('//[^\n]+', '', code)
    code = re.sub('[0-9]+_t', '', code)
    code = re.sub('uint', 'unsigned int', code)
    return code


def collect_loop_info(c_file):
    with open(c_file) as f:
        code = f.read()

    code = preprocess(code)
    # with open("prep.c", "w") as fout:
    #     fout.write(code)

    parser = c_parser.CParser()
    ast = parser.parse(code, filename=c_file)
    ## ast.show(showcoord=True)
    # print((ast))
    visitor = ASTVisitor()
    visitor.visit(ast)

if __name__ == '__main__':
    collect_loop_info("100000.c")
    # collect_loop_info("basic.c")
    # path = "/mnt/shared/home/shuang91/downloads/c_files2_csmith"
    # c_files = [f for f in listdir(path) if re.match('[0-9]+.c', f) and 
    #                                        isfile(join(path, f))]
    # for c_file in c_files:
    #     print(c_file)
    #     collect_loop_info(join(path, c_file))
