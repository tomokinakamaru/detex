from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    author='Tomoki Nakamaru',
    author_email='nakamaru@csg.ci.i.u-tokyo.ac.jp',
    install_requires=('TexSoup==0.2.0',),
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='detex',
    py_modules=('detex',),
    version='0.0.0'
)
