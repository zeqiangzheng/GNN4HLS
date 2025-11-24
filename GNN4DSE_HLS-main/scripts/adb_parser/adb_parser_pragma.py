#!/usr/bin/python
import numpy as np
import xmltodict
import csv
import pickle
import argparse

class Element:
    def __init__(self) -> None:
        self.id = None
        self.ty = None
        self.name = None
        self.bitwidth = None
        self.opcode = None
        self.delay = None
        self.line_no = None
    def vector(self):
        return [self.id, self.ty, self.name, self.bitwidth, self.opcode, \
                self.delay, self.line_no]

class Port(Element):
    def __init__(self, port=None, id_space=None) -> None:
        super().__init__()
        if port and id_space:
            self.ty = "port"
            original_id = int(port['Value']['Obj']['id'])
            self.id = id_space.get_id(original_id)
            self.name = port['Value']['Obj']['name']
            self.bitwidth = port['Value']['bitwidth']
            self.line_no = port['Value']['Obj']['lineNumber']

class Node(Element):
    def __init__(self, node=None, id_space=None) -> None:
        super().__init__()
        if node and id_space:
            self.ty = "node"
            original_id = int(node['Value']['Obj']['id'])
            self.id = id_space.get_id(original_id)
            self.name = node['Value']['Obj']['name']
            self.bitwidth = node['Value']['bitwidth']
            self.opcode = node['opcode']
            self.delay = node['m_delay']
            self.line_no = node['Value']['Obj']['lineNumber']

class Const(Element):
    def __init__(self, const=None, id_space=None) -> None:
        super().__init__()
        if const and id_space:
            self.ty = "const"
            original_id = int(const['Value']['Obj']['id'])
            self.id = id_space.get_id(original_id)
            self.name = const['Value']['Obj']['name']
            self.bitwidth = const['Value']['bitwidth']
            self.line_no = const['Value']['Obj']['lineNumber']

class Block(Element):
    def __init__(self, block=None, id_space=None) -> None:
        super().__init__()
        if block and id_space:
            self.ty = "block"
            original_id = int(block['Obj']['id'])
            self.id = id_space.get_id(original_id)
            self.name = block['Obj']['name']
            self.line_no = block['Obj']['lineNumber']


class IDSpace:
    def __init__(self) -> None:
        self.id_remap = {} # map original id to new consecutive id's starting from 0
        self.curr_id  = -1

    def new_id(self):
        self.curr_id = self.curr_id + 1
        return self.curr_id

    def has_id(self, id):
        return id in self.id_remap
    
    def get_length(self):
        return len(self.id_remap)

    def get_id(self, original_id):
        if original_id not in self.id_remap:
            self.id_remap[original_id] = self.new_id()

        return self.id_remap[original_id]

def parse(adb_file, args):

    id_space = IDSpace()

    with open(adb_file) as fd:
        doc = xmltodict.parse(fd.read())

    if args.json: out_json = {}

    out_csv = [['id', 'type', 'name', 'bitwidth', 'opcode', 'delay', 'line_no']]

    cdfg   = doc['boost_serialization']['syndb']['cdfg']
    top_f  = cdfg['name']
    ports  = cdfg['ports']['item']  if cdfg['ports']['count']  != '0' else []
    nodes  = cdfg['nodes']['item']  if cdfg['nodes']['count']  != '0' else []
    consts = cdfg['consts']['item'] if cdfg['consts']['count'] != '0' else []
    blocks = cdfg['blocks']['item'] if cdfg['blocks']['count'] != '0' else []
    edges  = cdfg['edges']['item']  if cdfg['edges']['count']  != '0' else []

    ## convert to list if there is only one element
    if type(ports)  is not list: ports  = [ ports  ]
    if type(nodes)  is not list: nodes  = [ nodes  ]
    if type(consts) is not list: consts = [ consts ]
    if type(blocks) is not list: blocks = [ blocks ]
    if type(edges)  is not list: edges  = [ edges  ]

    if args.dot:
        import graphviz
        dot = graphviz.Digraph(comment=f'CDFG of {top_f}')

    for port in ports:
        p = Port(port, id_space)
        out_csv.append(p.vector())
        if args.json: out_json[p.id] = []
        if args.dot:
            node_label = f'{p.id}, {p.ty}'
            node_label = node_label + (f'.{p.opcode}' if p.opcode else '')
            dot.node(str(p.id), node_label)

    for node in nodes:
        n = Node(node, id_space)
        out_csv.append(n.vector())
        if args.json: out_json[n.id] = []
        if args.dot:
            node_label = f'{n.id}, {n.ty}'
            node_label = node_label + (f'.{n.opcode}' if n.opcode else '')
            dot.node(str(n.id), node_label)

    for const in consts:
        c = Const(const, id_space)
        out_csv.append(c.vector())
        if args.json: out_json[c.id] = []
        if args.dot:
            node_label = f'{c.id}, {c.ty}'
            node_label = node_label + (f'.{c.opcode}' if c.opcode else '')
            dot.node(str(c.id), node_label)

    for block in blocks:
        b = Block(block, id_space)
        out_csv.append(b.vector())
        if args.json: out_json[b.id] = []
        if args.dot:
            node_label = f'{b.id}, {b.ty}'
            node_label = node_label + (f'.{b.opcode}' if b.opcode else '')
            dot.node(str(b.id), node_label)

    num_nodes = id_space.get_length()
    adj_mat = np.zeros((num_nodes, num_nodes), dtype=np.bool)

    for edge in edges:
        original_id = int(edge['id'])
        id = id_space.get_id(original_id)
        source = int(edge['source_obj'])
        sink = int(edge['sink_obj'])
        if id_space.has_id(source) and id_space.has_id(sink):
            source_id = id_space.get_id(source)
            sink_id   = id_space.get_id(sink)
            if args.json: out_json[source_id].append([id, sink_id])
            if args.dot:  dot.edge(str(source_id), str(sink_id))
            adj_mat[source_id, sink_id] = True
            adj_mat[sink_id, source_id] = True
        else:
            print(f"Skipping edge {source} -> {sink}")

    np.save(args.out_npy, adj_mat)

    with open(args.out_csv, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(out_csv)

    if args.json:
        import json
        with open(args.out_json, 'w') as f:
            json.dump(out_json, f, indent=4)

        if args.pickle:
            with open(args.out_pickle, 'wb') as f:
                pickle.dump([out_json, out_csv], f)
    if args.dot:
        dot.render(args.out_dot)

def load(pkl_file):
    with open(pkl_file, 'rb') as f:
        out_json, out_csv = pickle.load(f)

    print(out_json)
    print(out_csv)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--json', help="output JSON file", \
                        action="store_true")
    parser.add_argument('-p', '--pickle', help="dump JSON and csv to pickle", \
                        action="store_true")
    parser.add_argument('-d', '--dot', help="output graph file", \
                        action="store_true")

    parser.add_argument('--input', help="input *.adb file",\
                        default='../hls_cdfg/vecadd.adb')
    parser.add_argument('--input_folder', help="folder containing *.adb files")

    parser.add_argument('--out_npy', help="output *.npy filename",
                        default="out.npy")
    parser.add_argument('--out_csv', help="output *.csv filename",
                        default="out.csv")
    parser.add_argument('--out_json', help="output *.json filename",
                        default="out.json")
    parser.add_argument('--out_pickle', help="output *.pickle filename",
                        default="out.pickle")
    parser.add_argument('--out_dot', help="output *.dot filename",
                        default="out.dot")

    args = parser.parse_args()
    if args.input_folder:
        from os import listdir
        from os.path import isfile, join
        print(listdir(args.input_folder))

        adb_files = [f for f in listdir(args.input_folder) \
                if isfile(join(args.input_folder, f)) and f.endswith('.adb')]
        print(f"adb_files = {adb_files}")
        for adb_file in adb_files:
            adb_file = join(args.input_folder, adb_file)
            print(adb_file)
            parse(adb_file, args)
    else:
        if args.input:
            adb_file = args.input
        print(adb_file)
        parse(adb_file, args)

    # load('data.pkl')
