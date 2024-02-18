# Simple toolkit for getting PROGENy scores

This folder consist of a Python toolkit package which can be used to get PROGENy score for a selected collection from 
Genialis Expressions data repository.

## Installation

In root folder of this project run the bellow command, which will create a **progeny** package:

``` pip install -e . ```


## Usage
The **progeny** package can be used like any other python package.
To get help, run:

``` 
progeny -h 
```

To get PROGENy scores for a selected dataset, you have to specify a valid collection name, for example:

```
progeny windrem-et-al-cell-2017
```

A formatted table with PROGENy scores for each sample in collection will be printed out in CLI.
If needed, the table can be saved in markdown file by adding a flag `-o`:

```
progeny windrem-et-al-cell-2017 -o
```

### Details
PROGENy scores are calculated as described in Schubert et al. 2018 (Perturbation-response genes reveal signaling footprints 
in cancer gene expression).


