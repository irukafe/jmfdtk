# JMFDTk: Japanese Moral Foundation Dictionary Toolkit
## Main features
- Counting documents with moral foundation words
- Clustering texts based on counts of moral foundation words
- Generating coding files and a compoud list file for [KH Coder](https://github.com/ko-ichi-h/khcoder)

## Installation
Clone the repository.
```
$ git clone git@github.com:irukafe/jmfdtk.git
```
Move to the repository directory.
```
$ cd jmfdtk
```
Install with pip.
```
$ pip install .
```

## Uninstallation
```
$ pip uninstall jmfdtk
```

## Examples of counting documents with moral foundation words and clustering
Examples are [here](https://github.com/irukafe/jmfdtk/blob/main/examples/) and notebooks are also available.

## Generation of coding files for KH Coder
```
>>> from jmfdtk.khcodegen import generate_khcode
>>> generate_khcode()
./code_jmf.txt was created.
./code_jmfw.txt was created.
./compound_jmf.txt was created.
```
