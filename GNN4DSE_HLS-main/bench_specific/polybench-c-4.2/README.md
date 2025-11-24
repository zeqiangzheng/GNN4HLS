**Prerequisites**

These scripts should be placed inside your *polybench-c-4.2* folder along with the other Polybench files and benchmark folders.

**Usage**

Run the script `python3 hls_create_run.py`

**Main objectives**

The main script *hls_create_run.py* performs three important tasks:
- first, it goes into each benchmark folder and modifies the C code to remove `static` prefixes
- second, it creates a custom TCL file for each benchmark into the ./HLS_projects/ directory
- third, it runs each of these TCL files one after the other (i.e. runs HLS/RTL syntheses and implementation)

**Next steps**

The other two scripts *hls_copy_reports.py* and *hls_copy_db.py* are used to move the most important benchmark files into a consolidated folder (along with other benchmarks such as CHStone etc.), for further processing.

The reports can then be processed using our script io_extract.py, accessible in the *extract/* folder, which needs slightly modified versions of three other scripts (adb_parser.py, report_extract.py, verilog_extract.py) present in the same *extract/* folder.
