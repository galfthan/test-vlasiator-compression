from distutils.core import setup, Extension

# define the extension module
zfpmodule = Extension('zfpmodule', sources=['zfpmodule.c'])

# run the setup
setup(ext_modules=[zfpmodule])
