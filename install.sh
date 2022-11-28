#!/bin/bash
conda env create -f 2d3d_pipeline.yml
source activate 2d3d_pipeline
pip install -e .[dev,testing]
python -m ipykernel install --user --name 2d3d_pipeline --display-name "Python (2d3d_pipeline)"
