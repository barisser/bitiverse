from setuptools import setup

setup(name='bitiverse',
      version='0.1',
      description='A Decentralized Web Page',
      url='www.bitiverse.com',
      author='Andrew Barisser',
      license='MIT',
      packages=['bitiverse'],
      install_requires=[
        'bitcoin',
        'pycoin'
      ],
      zip_safe=False)
