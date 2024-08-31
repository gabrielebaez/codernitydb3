from setuptools import setup
from slitheringdb import __version__, __license__

with open('README.rst') as fhd:
    L_DESCR = fhd.read()

keywords = ' '.join(('database', 'python', 'nosql', 'key-value', 'key/value',
                     'db', 'embedded'))

setup(name='slitheringdb',
      version=__version__,
      description='Pure python, embedded, fast, schema-less, NoSQL database',
      long_description=L_DESCR,
      long_description_content_type='text/x-rst',
      keywords=keywords,
      author='Gabriel E. Báez',
      author_email='gabrielebaez@users.noreply.github.com',
      url='https://github.com/gabrielebaez/slitheringdb',
      packages=['slitheringdb'],
      license=__license__,
      classifiers=[
          'Development Status :: 1 - Pre-Alpha', 'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.12',
          'Topic :: Database',
          'Topic :: Database :: Database Engines/Servers'
      ],
      python_requires='>=3.12')
