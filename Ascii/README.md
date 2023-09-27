# Generating Ascii Brownian Trees using DLA

This project contains scripts usefull for simulating *duffusion-limited aggregation* (DLA) to generate ascii *brownian trees*, and to convert those trees into an animated gif of the process

## Generating Brownian Trees

The `brown_tree.py` script can simulate the generation of a brownian tree.

### Usage

`python brown_tree.py heigth width number-of-particles`

Generates file `test_out.txt` with the final tree, and all generates all the intermediary steps into `test_steps/`

## Generating animated gifs from DLA steps

The `txt2image.py` script can generate an animated gif from a series of text files

### Usage

`python txt2image.py`

Assumes there is a series of text files named `test_steps/.*(\d+).txt`. Sorts those files by their number and generates an animated gif.