from distutils.core import setup, Extension

# define the extension module
zfpmodule = Extension('zfpmodule',
                      sources=['zfpmodule.c'],
                      include_dirs = ['extra/zfp/include'],
                      libraries = ['zfp'],
                      library_dirs = ['extra/zfp/lib']
)

# run the setup
setup(ext_modules=[zfpmodule])
