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
import pandas as pnd
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
        back to the original source (mesh, metadata like camera position...), and simply 
        rely on some mapping json that might or might not work for what study a user
        might want to do.

        :return: _description_
        :rtype: _type_
        """
        _ = self._read_decryptor_ring_file_and_get_labels()

        
        # first generate a dictionary of items that need to be stored in the `dask` dataframe
        data_catalog_dict = {
            "mesh_file_path": self.dataset_list,
            # "label": self.labels_list,
            # "bounding_box": self.bbox_list,
        }
        
        catalog_frame = pd.from_dict(data_catalog_dict, npartitions=10)
        catalog_path = Path(self.data_folder.as_posix()).joinpath("".join(("datacatalog_parts/datacatalog-*.csv")) )
        
        print(catalog_path)
        if self.verbose: print("data catalog parts saved to:", self.meta_data_label_df["simple_label"].unique())
        
        
        catalog_frame['metadata_file'] = catalog_frame.apply(self._get_meta_json_path, axis=1, meta=("x", str))
        
        
        
        
        # catalog_frame["label"] = 
        print(self.data_folder)
        print(self.data_catalog_file)
        self.data_catalog_path = catalog_frame.to_csv(self.data_folder.joinpath(self.data_catalog_file))

        return self.data_catalog_path

    def _read_decryptor_ring_file_and_get_labels(self):
        
        meta_data_label_file = json.load(self.local_fs.open(self.decryptor_ring_file))
        meta_data_label_file_df = pnd.DataFrame(meta_data_label_file)

        # get a simple label from the label options (ShapeNet Specific)
        meta_data_label_file_df['simple_label'] = meta_data_label_file_df["name"].apply(lambda x: x.split(",")[0])
        
        if self.verbose: print("-----------------meta data file-----------------\n\n", meta_data_label_file_df[["synsetId", "name", "simple_label"]].head)
        
        self.meta_data_label_df = meta_data_label_file_df
        
        return self.meta_data_label_df

    def _get_metadata_for_meshes(self):
        """Open a json metadata file (shapenet specific) and get a centroid, bounding box, and simple label"""
        
        
        return None

    def _get_meta_json_path(self, row: str):
            if self.local_fs.exists(str(Path(row["mesh_file_path"]).parent.joinpath("model_normalized.json"))):
                return Path(row["mesh_file_path"]).parent / "model_normalized.json"
            else:
                return self.local_fs.ls(str(Path(row["mesh_file_path"]).parent.joinpath("*.json")))[0]
        
        
    def __len__(self):
        return len(self.dataCatalog)

    # get a row at an index 5375
    def __getitem__(self, idx):
        sample = []
        return sample
