from distutils.core import setup

setup(
    name='wikitree-api',
    version='0.1',
    packages=['wikitree'],
    url='http://github.com/jeroenl/wikitree-api',
    license='Apache v2 License',
    author='Jeroen Latour',
    author_email='jeroenl on GitHub',
    description='Provides access to WikiTree genealogical data.',
    requires=['microdata']
)
