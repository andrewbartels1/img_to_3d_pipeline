#!/bin/bash
conda env create -f im23D_pipeline.yml;
eval "$(conda shell.bash hook)";
conda activate im23D_pipeline;
echo $CONDA_PREFIX;

# install the package
pip install -e .[dev,testing];
python -m ipykernel install --user --name im23D_pipeline --display-name "Python (im23D_pipeline)";

# install pytorch3d separately from the git repo into the env
git clone https://github.com/facebookresearch/pytorch3d.git;                 
cd pytorch3d/;
eval "$(conda shell.bash hook)";
conda activate im23D_pipeline;
echo $CONDA_PREFIX;
echo "PIP:" which pip;
${CONDA_PREFIX}/bin/pip install -e .;
echo "pytorch 3d installed from git!";
cd ../; rm -rf pytorch3d/;