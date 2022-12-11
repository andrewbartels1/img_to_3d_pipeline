from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
import torch
from torch.utils.data import Dataset, random_split
from im23D_pipeline.pydantic_models import ShapeNetModel
import pandas as pnd

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
        self.local_fs = shape_input_model.local_fs
        self.verbose = shape_input_model.verbose
        self.catalog_path = shape_input_model.datacatalog_path

        if not self.refresh_data_catalog:
            self.data_catalog_file_path = self._generate_data_catalog()

        # load the csv file as a (dask) dataframe
        print("THIS IS Catalog path", self.data_catalog_file_path)
        self.dataCatalog = pnd.read_csv(self.data_catalog_file_path)

    def write_catalog_to_csv(self, dataCatalog):
        if self.verbose:
            print("writing out metadata to:", self.data_folder.joinpath(self.data_catalog_file))
        self.data_catalog_path = dataCatalog.to_csv(self.data_folder.joinpath(self.data_catalog_file))

        if self.verbose:
            print("wrote data catalog to path:", self.data_catalog_path)

    def _load_data_catalog_file(self):
        """Reads in group of csv data catalogs files into dask dataframe"""
        return pnd.read_csv(self.data_catalog_file_path)

    def _load_objects_take_pictures(self):
        self.DontUseBaseLoaderMssg = (
            "The img23DBaseDataset class is not meant to be used directly, "
            + "please use classes: in {} to load datasets!".format("\n".join(SUPPORTED_DATASETS))
        )
        return NotImplementedError(self.DontUseBaseLoaderMssg)

    def _generate_data_catalog(self, root_path_folder):
        return NotImplementedError(self.DontUseBaseLoaderMssg)

    def _assign_metadata_and_labels_for_meshes(self):
        return NotImplementedError(self.DontUseBaseLoaderMssg)

    def _read_decryptor_ring_file_and_get_labels(self):
        return NotImplementedError(self.DontUseBaseLoaderMssg)

    def _get_metadata_for_meshes(self):
        return NotImplementedError(self.DontUseBaseLoaderMssg)

    def __len__(self):
        return len(self.dataCatalog.index)

    # get indexes for train and test rows
    def get_splits(self, n_test=0.2):
        # determine sizes
        test_size = round(n_test * len(self.dataCatalog))
        train_size = len(self.dataCatalog) - test_size
        # calculate the split
        return random_split(self, [train_size, test_size])

    # get a row at an index 5375
    def __getitem__(self, idx):
        return NotImplementedError(self.DontUseBaseLoaderMssg)
