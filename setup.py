from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='python_ocw',
    version='0.0.5',
    description="The classses that wrap Online Checkwriter's API",
    long_description=readme,
    author='Dan Herrington',
    author_email='dan@cascadiarc.com',
    url='https://github.com/cascadiarc/python_ocw',
    license=license,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    packages=[
        'ocw'
    ],
)