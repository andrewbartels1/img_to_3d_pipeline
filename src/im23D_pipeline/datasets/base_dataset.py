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
    Loader is meant to only do the general generating of items
    that all datasets (Pix3D, ShapeNet, etc.) have in common as to
    not repeat yourself.
    """

    def __init__(self, shape_input_model: ShapeNetModel):

        # Empty lists to be utilized by numerous functions
        self.labels_list = []

        # get max/min bounds of mesh for rendering etc.
        # can be derived from metadata file or through a function,
        # should be a list of lists for pydantic to deal with
        self.bbox_list = []

        # unpack pydantic model into class
        self.data_folder = shape_input_model.dataset_folder
        self.dataset_list = shape_input_model.dataset_list
        self.mesh_type = shape_input_model.mesh_type
        self.decryptor_ring_file = shape_input_model.decryptor_ring_file
        self.data_catalog_file = shape_input_model.data_catalog_file
        self.data_catalog_file_type = shape_input_model.data_catalog_file_type
        self.refresh_data_catalog = shape_input_model.refresh_data_catalog

        if not (self.data_catalog_file or self.refresh_data_catalog):
            self.data_catalog_file = self._generate_data_catalog()

        # load the csv file as a (dask) dataframe
        # self.dataCatalog = pd.read_csv(self.data)

    def _load_objects_take_pictures(self):
        self.DontUseBaseLoaderMssg = (
            "The img23DBaseDataset class is not meant to be used directly, "
            + "please use classes: in {} to load datasets!".format("\n".join(SUPPORTED_DATASETS))
        )
        return NotImplementedError(self.DontUseBaseLoaderMssg)

    def _generate_data_catalog(self, root_path_folder):
        return NotImplementedError(self.DontUseBaseLoaderMssg)

    def _read_decryptor_ring_file_and_get_labels(self):
        return NotImplementedError(self.DontUseBaseLoaderMssg)

    def _get_metadata_for_meshes(self):
        return NotImplementedError(self.DontUseBaseLoaderMssg)

    def __len__(self):
        return len(self.dataCatalog)

    # get a row at an index 5375
    def __getitem__(self, idx):
        sample = []
        return sample
