from setuptools import setup

setup(
    name='cem',
    version='0.1',
    description='chrome extension manager',
    url='https://github.com/nitrocode/cem',
    author='nitrocode',
    license='MIT',
    packages=['cem'],
    scripts=['bin/cem'],
    zip_safe=False
)
