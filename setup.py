from setuptools import setup,find_packages

setup(name='ideogram',
         version='0.1',
         description="Python developers: Create a visual fingerprint for your project's source code!",
         author='Ben Scheiner',
         author_email='brmscheiner@gmail.com',
         url='https://github.com/brmscheiner/ideogram',
         packages=['ideogram','ideogram.polarfract'],
         install_requires=['pystache','requests'],
         package_data={'ideogram':['ideogram/templates/*.js','ideogram/templates/*.mustache']}
         )