import csv
import os
import distutils.dir_util
from report_extract import extract_report
from verilog_extract import extract_verilog
from adb_parser import parse
import traceback
import logging

idir = "."
odir = "GNN_IO"

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

try:
    os.mkdir(odir)
except FileExistsError:
    pass

hls_file = open(odir + '/HLS_report.csv', mode='w')
hls_csv = csv.writer(hls_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
hls_csv.writerow("benchmark,dsp,ff,lut,bram,dsp_avail,ff_avail,lut_avail,bram_avail,dsp_perc,ff_perc,lut_perc,bram_perc,period,avg_latency".split(','))

rtl_file = open(odir + '/RTL_report.csv', mode='w')
rtl_csv = csv.writer(rtl_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
rtl_csv.writerow("benchmark,dsp,ff,lut,bram,dsp_avail,ff_avail,lut_avail,bram_avail,dsp_perc,ff_perc,lut_perc,bram_perc,period".split(','))

error_file = open(odir + '/ADB_errors.txt', mode='w')

names = os.listdir(idir)
#names = ["PolyBench+2mm", "PolyBench+fft"]
for name in names:
	path = idir + "/" + name
	if name == odir or not os.path.isdir(path):
		continue

	filenames = os.listdir(path)
	for filename in filenames:
		if filename[-4:].lower() != ".adb":
			continue
		top_func = filename[:-4]
		hls_csv.writerow( (name,) + extract_report(top_func, path) )
		rtl_csv.writerow( (name,) + extract_verilog(path) )
		
		odir2 = odir + '/' + name 
		try:
		    os.mkdir(odir2)
		except FileExistsError:
		    pass		

		args = dotdict({'json': True, 'pickle': False,
			'out_npy': odir2 + '/adj_matrix.npy',
			'out_csv': odir2 + '/node_features.csv'})

		print('Parsing ' + path + '/' + filename)
		try:
			parse(path + '/' + filename, args, odir2 + '/')
		except Exception as e:
			error_file.write(path + '/' + filename + '\n' + traceback.format_exc() +'\n')
			logging.error(traceback.format_exc())
      