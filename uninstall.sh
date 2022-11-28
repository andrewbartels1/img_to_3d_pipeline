#!/bin/bash
source activate base
conda env remove --name im23D_pipeline
yes | jupyter kernelspec uninstall im23D_pipeline
