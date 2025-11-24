#!/usr/bin/python
import re
import xmltodict
import json

top_func = 'kernel_deriche'
prj_path = '/home/shuang91/code/GNN4DSE_HLS/scripts/adb_files'


def explore():
    adb_file = f"{prj_path}/{top_func}.adb"
    with open(adb_file) as fp:
        txt = fp.read()

    id_lst = re.findall("<id>([0-9]+)</id>", txt)
    id_lst = [int(e) for e in id_lst]
    id_lst.sort()
    print(f"<id>: {id_lst}")
    print(f"len<id>: {len(id_lst)}")

    oid_lst = re.findall("object_id=\"_([0-9]+)\"", txt)
    oid_lst = [int(e) for e in oid_lst]
    oid_lst.sort()
    print(f"<object_id>: {oid_lst}")
    print(f"len<object_id>: {len(oid_lst)}")

    source_lst = re.findall("<source_obj>([0-9]+)</source_obj>", txt)
    source_lst = [int(e) for e in source_lst]
    source_lst.sort()
    print(f"<source_obj>: {source_lst}")
    print(f"len<source_obj>: {len(source_lst)}")

    sink_lst = re.findall("<sink_obj>([0-9]+)</sink_obj>", txt)
    sink_lst = [int(e) for e in sink_lst]
    sink_lst.sort()
    print(f"<sink_obj>: {sink_lst}")
    print(f"len<sink_obj>: {len(sink_lst)}")

    id_lst_err = []
    oid_lst_err = []

    for e in source_lst:
        if e not in id_lst:
            id_lst_err.append(e)
        if e not in oid_lst:
            oid_lst_err.append(e)

    for e in sink_lst:
        if e not in id_lst:
            id_lst_err.append(e)
        if e not in oid_lst:
            oid_lst_err.append(e)

    print(f"id errors: {id_lst_err}")
    print(f"object id errors: {oid_lst_err}")

explore()
