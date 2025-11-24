**Merge multiple benchmark folders into a common directory**

You may want to merge the sets of benchmarks generated separately. For instance, to merge the benchmarks contained in two folders
**output1** and **output2**, into a new folder **output1+output2** with consolidated summary CSV files, use the script **merge_bench.py**.
Make sure you *edit the merge_bench.py file first* to specify the directories that you want to merge.

**Merge folders manually and rebuild CSV reports**

You can also paste manually multiple benchmarks into a common folder using OS commands (faster than the merge_bench.py Python script).
After doing this, use **rebuild_csv_reports.py** to rebuild the summary CSV files from the benchmark folders.
Make sure you *edit the rebuild_csv_reports.py file first* to specify the directory that contains your benchmark folders.

This script may also be useful after benchmark generation with a lot a parallel process:
in that case, the consolidated CSVs may currently be missing some lines (a few changes to autgen3 will solve this),
instead of deleting these benchmarks, run **rebuild_csv_reports.py** to regenerate the two summary CSV files.
