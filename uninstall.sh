#!/bin/bash
source activate base
conda env remove --name 2d3d_pipeline
yes | jupyter kernelspec uninstall 2d3d_pipeline
