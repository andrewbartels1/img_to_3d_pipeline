import os
import json
from os import path
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
import torch
from im23D_pipeline.pydantic_models import ShapeNetModel
from .base_dataset import img23DBaseDataset
import dask.dataframe as pd

# https://trimsh.org/trimesh.proximity.html#trimesh.proximity.signed_distance
# https://trimsh.org/examples.nearest.html
SUPPORTED_DATASETS = ["img23DBaseDataset", "Pix3dDataset", "ShapeNetCoreDataset", "ABODataset"]


class ShapeNetCoreDataset(img23DBaseDataset):
    """The Base Implementation of the img23D Dataset, this
    Loader is meant to only do the file

    :param Dataset: _description_
    :type Dataset: _type_
    """

    def _load_objects_take_pictures(self):
        return None

    def _generate_data_catalog(self, root_path_folder):
        return None

    def __len__(self):
        return len(self.dataCatalog)

    # get a row at an index 5375
    def __getitem__(self, idx):
        sample = []
        return sample
