from setuptools import setup

__project__ = "Marvin_PC_Interface"
__version__ = "0.0.1"
__description__ = "A Basic Communication Program to Marvin"
__packages__ = ['pandas', 'PyQt5', 'matplotlib', 'numpy', 'pyserial', 'scipy']

setup(name = __project__, version = __version__, description = __description__, scripts = ['scripts/installscript.sh'], packages = __packages__)

