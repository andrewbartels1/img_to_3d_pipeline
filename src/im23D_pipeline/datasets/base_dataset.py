from os import path
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
import torch
from torch.utils.data import Dataset  # , DataLoader, random_split
from im23D_pipeline.pydantic_models import ShapeNetModel
import dask.dataframe as pd

# https://trimsh.org/trimesh.proximity.html#trimesh.proximity.signed_distance
# https://trimsh.org/examples.nearest.html
SUPPORTED_DATASETS = ["img23DBaseDataset", "Pix3dDataset", "ShapeNetCoreDataset", "ABODataset"]


class img23DBaseDataset(Dataset):
    """The Base Implementation of the img23D Dataset, this
    Loader is meant to only do the file

    :param Dataset: _description_
    :type Dataset: _type_
    """

    def __init__(self, pydantic_model: ShapeNetModel):
        # load the csv file as a dataframe
        self._generate_data_catalog
        self.dataCatalog = pd.read_csv(path)

        # self.file_list = []
        self.data_folder = pydantic_model.dataset_folder
        self.mesh_type = pydantic_model.mesh_type
        # self.

    def _load_objects_take_pictures(self):
        self.DontUseBaseLoaderMssg = (
            "The img23DBaseDataset class is not meant to be used directly, "
            + "please use classes: in {} to load datasets!".format('\n'.join(SUPPORTED_DATASETS))
        )
        return NotImplementedError(self.DontUseBaseLoaderMssg)

    def _generate_data_catalog(self, root_path_folder):
        return NotImplementedError(self.DontUseBaseLoaderMssg)

    def __len__(self):
        return len(self.dataCatalog)

    # get a row at an index 5375
    def __getitem__(self, idx):
        sample = []
        return sample