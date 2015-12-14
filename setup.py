import os
import re
import sys
from setuptools import setup, find_packages


install_requires = []

PY_VER = sys.version_info

if not PY_VER >= (3, 5):
    raise RuntimeError("aionats doesn't support Python earlier than 3.5")


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()

extras_require = {}


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'aionats', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version in aionats/__init__.py')

classifiers = [
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Operating System :: POSIX',
    'Environment :: Web Environment',
    'Development Status :: 3 - Alpha',
]


setup(name='aionats',
      version=read_version(),
      description=(''),
      long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
      classifiers=classifiers,
      platforms=['POSIX'],
      author="",
      author_email="",
      url='',
      download_url='',
      license='MIT',
      packages=find_packages(),
      install_requires=install_requires,
      extras_require=extras_require,
      include_package_data=True)
