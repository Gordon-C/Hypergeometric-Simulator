import sys
from cx_Freeze import setup, Executable

include_files = ["imgs\\back.png", "imgs\\forward.png"]
setup(
	name = 'HypergeoSim',
	version = '1.0',
	author='Gordon Chu',
	description = 'A hypergeometric simulator',
	options = {'build_exe': {'include_files':include_files}},
	executables = [Executable('hypergeom.py', base ='Win32GUI')]
	)