import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="ichorlib",
    version="0.1",
    author="Konstantinos Thalassinos",
    author_email="k.thalassinos@ucl.ac.uk",
    description=("A library for processing mass spectromtery data."),
    license="BSD",
    keywords="native mass spectrometry ",
    url="http://www.homepages.ucl.ac.uk/~ucbtkth/resources.html",
    packages=[
        'ichorlib', 'ichorlib.genClasses', 'ichorlib.imClasses',
        'ichorlib.msClasses', 'ichorlib.seqClasses', 'Testing_Ichor'
    ],
    include_package_data=True,
    install_requires=['pyteomics'],
    python_requires='>=2.7',
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: EULA?",
    ],
)
