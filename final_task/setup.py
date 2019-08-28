from setuptools import setup
with open('README.md') as readme:
    full_description = readme.read()

setup(
    name='pycalc',
    version='1.0',
    author='Nikita Makhnitskiy',
    author_email='makhnitskiy1@yandex.by',
    description='Pure-python command-line calculator',
    long_description=full_description,
    url='https://github.com/Creator227/PythonHomework',
    license='MIT',
    packages=['pycalc'],
    zip_safe='False',
    entry_points={'console_scripts': ['pycalc=rpn_pycalc.__main__:_main']}
)