from distutils.core import setup

setup(name='bpl',
      version='1.0',
      description='BPL Compiler',
      author='Oren Shoham',
      author_email='oshoham@oberlin.edu',
      url='https://github.com/oshoham/bpl-compyler',
      license='GPL',
      packages=['bpl', 'bpl.scanner', 'bpl.parser', 'bpl.type_checker', 'bpl.code_generator', 'bpl.test'],
      package_data={'bpl.test': ['test3.bpl']},
      scripts=['bplc']
)
