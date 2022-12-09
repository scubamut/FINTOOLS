from distutils.core import setup

setup(
    name='fintools',
    version='0.7.0',
    author='Dave Gilbert',
    author_email='scubamut @gmail.com',
    packages=['fintools'],
    scripts=[],
    url='http://pypi.python.org/pypi/fintools/',
    license='LICENSE.txt',
    description='Toolset for developing and backtesting asset allocation strategies',
    long_description=open('README.md').read(),
)
