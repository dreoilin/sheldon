from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sheldon',
    version='0.1.0',
    description='Python package for WPT characterisation equipment',
    long_description=readme,
    author="Cian O'Donnell",
    author_email='cian.odonnell@tyndall.ie',
    url='https://github.com/madrasalach/sheldon',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)