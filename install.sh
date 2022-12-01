#!/bin/bash
conda env create -f im23D_pipeline.yml
source activate im23D_pipeline
echo $CONDA_PREFIX
pip install -e .[dev,testing]
python -m ipykernel install --user --name im23D_pipeline --display-name "Python (im23D_pipeline)"
