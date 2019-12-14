from setuptools import setup, find_packages


setup(name='pyxedit',
      packages=find_packages(exclude=['test']),
      version='0.1',
      description='python wrapper around xedit-lib',
      author='leontristain',
      keywords=[],
      classifiers=[],
      setup_requires=[],
      install_requires=[],
      # data_files=[('Lib/site-packages/pyxedit', ['XEditLib/XEditLib.dll'])],
      tests_require=['pytest==4.3.0'],
      test_suite='test')

