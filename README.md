Some incomplete tweaks to [xdot](https://github.com/jrfonseca/xdot.py) to make navigating verilog easier thanks to [yosys](https://github.com/YosysHQ/yosys) 

Setup:
```
git clone --recursive <url>
```
Check if the following makes sense in `sample.py`:
```
DOTFILE
VERILOGROOT
XDOT
EDITOR
```
Yosys:
```
yosys load.ys
# select some stuff, for example:
cd top
select -set pc picorv32.reg_pc
select @pc %x3:-[CLK] ; show -format dot -long
```
Xdot:
```
# need to --system-... for python3-gi
python3 -m venv venv --system-site-packages
. venv/bin/activate<.shell>
pip install pgi
python sample.py
```
Now click stuff with a filename to open that file.

Updates through `show` in yosys' standard output file will be seen automagically.
