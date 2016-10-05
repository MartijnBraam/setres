from setuptools import setup

setup(name='setres',
      version='0.3',
      description='Set the resolution in xorg',
      url='http://github.com/MartijnBraam/setres',
      author='Martijn Braam',
      author_email='martijn@brixit.nl',
      license='MIT',
      packages=['setres'],
      entry_points={
          'console_scripts': ['setres=setres.__main__:main'],
      })
