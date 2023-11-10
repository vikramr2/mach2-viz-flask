''' Packaging Script '''

import os
import setuptools
from setuptools import find_packages

# https://stackoverflow.com/a/36693250/13241395
def package_files(directory):
    ''' Find external files to be used by Python '''
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mach2-viz",
    version="0.0.3",
    author="vikramr2",
    description="Visualizer for the MACH2 Metastasis Inference Algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vikramr2/mach2-viz-flask/tree/main/mach2viz",
    project_urls={
        "Bug Tracker": "https://github.com/vikramr2/mach2-viz-flask/tree/main/mach2viz/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "."},
    package_data={'': package_files('mach2viz/static')},
    packages=find_packages(),
    install_requires=["flask>=3.0.0"],
    python_requires=">=3.7",
)