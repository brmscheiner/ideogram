from setuptools import setup,find_packages

setup(name='ideogram',
         version='0.1',
         description="Python developers: Create a visual fingerprint for your project's source code!",
         author='Ben Scheiner',
         author_email='brmscheiner@gmail.com',
         url='https://github.com/brmscheiner/ideogram',
         packages=['ideogram','ideogram.polarfract'],
         install_requires=['pystache>=0.5.4','requests>=2.9.0'],
         package_data={'ideogram':['templates/*.js','templates/*.mustache']}
         )