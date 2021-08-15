import os
from setuptools import setup

NAME = 'jmfdtk'

setup_dir = os.path.abspath(os.path.dirname(__file__))
ver = {}

with open(os.path.join(setup_dir, NAME, '__version__.py')) as f:
    exec(f.read(), ver)


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name=NAME,
    version=ver.get('__version__'),
    description='Jnapanses Moral Fundation Dictionary Toolkit.',
    keywords=['Psychology', 'Moral Foundation Theory', 'Moral Foundation Dictionary'],
    author='irukafe',
    url='https://github.com/irukafe/jmfdtk',
    license='MIT',
    packages=[NAME],
    package_data={NAME: ['jmfd/*.dic']},
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=_requires_from_file('requirements.txt'),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    zip_safe=False,
)
