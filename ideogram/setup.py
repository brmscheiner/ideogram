from setuptools import setup,find_packages

setup(name='Ideogram',
         version='0.1',
         description="Python developers: Create a visual fingerprint for your project's source code!",
         author='Ben Scheiner',
         author_email='brmscheiner@gmail.com',
         url='https://github.com/brmscheiner/ideogram',
         packages=find_packages(),
         install_requires='pystache'
         )