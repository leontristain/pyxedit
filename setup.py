from setuptools import setup, find_packages


setup(name='pyxedit',
      packages=find_packages(exclude=['test']),
      version='0.1',
      description='python wrapper around xedit-lib',
      author='leontristain',
      install_requires=['cached-property>=1.5.1'],
      include_package_data=True)
