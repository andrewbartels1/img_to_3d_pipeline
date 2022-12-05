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
    """The *ShapeNet* Implementation of the img23D Dataset, this
    Loader is meant to only do the file

    :param Dataset: _description_
    :type Dataset: _type_
    """

    def _generate_data_catalog(self):
        """This function generates the data catalog that
        is used to call and gerenate data per batch in the
        `__getitem__` function (below). In order to make things simple
        and readable, a simple csv file, although it *might* be switched
        to a parquet file in the future if tranformations make things too large.
        But this `data catalog` is generated in order to ensure that
        there is an artifact from generating the mapping between the mesh files,
        the representation of the data being fed into some model (e.g. point cloud
        , voxel, mesh, etc.). All previous repos have been really difficult to trace
        back to the original source, and simply rely on some mapping json that might or
        might not work for what study a user might want to do.

        :return: _description_
        :rtype: _type_
        """
        self.labels_list = self._read_decryptor_ring_file_and_get_labels()

        self._get_metadata_for_meshes()
        # first generate a dictionary of items that need to be stored in the `dask` dataframe
        data_catalog_dict = {
            "mesh_file_path": self.dataset_list,
            "label": self.labels_list,
            "bounding_box": self.bbox_list,
        }
        
        catalog_frame = pd.from_dict(data_catalog_dict)
        self.data_catalog_path = catalog_frame.to_csv(Path(self.data_folder).parent.joinpath("datacatalog", self.data_catalog_file_type))

        return self.data_catalog_path

    def _read_decryptor_ring_file_and_get_labels(self):

        return None

    def _get_metadata_for_meshes(self):
        return None

    def __len__(self):
        return len(self.dataCatalog)

    # get a row at an index 5375
    def __getitem__(self, idx):
        sample = []
        return sample
