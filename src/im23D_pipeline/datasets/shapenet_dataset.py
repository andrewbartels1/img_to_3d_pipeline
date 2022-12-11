import os
import json
from os import path
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
import torch
from im23D_pipeline.pydantic_models import ShapeNetModel
from .base_dataset import img23DBaseDataset
import dask.dataframe as dd
import pandas as pnd
import pathlib
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
        # read the json file that has all the metadata; specific to the ShapeNet dataset
        _ = self._read_decryptor_ring_file_and_get_labels()

        # first generate a dictionary of items that need to be stored in the `dask` dataframe
        dataCatalog = dd.from_dict({"mesh_file_path": self.dataset_list}, npartitions=10)

        # run sets of functions to add columns, it's kind of slow, but it should only need to do this once!
        dataCatalog["metadata_file"] = dataCatalog.apply(self._get_per_obj_meta_json_path, axis=1, meta=("x", str))
        dataCatalog.apply(
            self._assign_metadata_and_labels_for_meshes, axis=1 #, meta=("x", str)
        )

        # send the file to csn
        self.write_catalog_to_csv(dataCatalog)

        return self.data_catalog_path

    def _read_decryptor_ring_file_and_get_labels(self):

        meta_data_label_file = json.load(self.local_fs.open(self.decryptor_ring_file))
        meta_data_label_file_df = pnd.DataFrame(meta_data_label_file)

        # get a simple label from the label options (ShapeNet Specific)
        meta_data_label_file_df["simple_label"] = meta_data_label_file_df["name"].apply(lambda x: x.split(",")[0])

        if self.verbose:
            print(
                "-----------------meta data file-----------------\n\n",
                meta_data_label_file_df.head,
            )

        self.meta_data_label_df = meta_data_label_file_df

        print(Path(self.catalog_path).parent)
        self.meta_data_label_df.to_csv(Path(self.catalog_path).parent / "meta_catalog.csv")
        return self.meta_data_label_df

    def _assign_metadata_and_labels_for_meshes(self, row: str):
        """Open a json metadata file (shapenet specific) and get a centroid, bounding box, and simple label"""
        
        mesh_parts = Path(row.mesh_file_path.split("ShapeNet")[-1]).parents[0]
        print("mesh_parts", mesh_parts)
        _, sysNetID, modelId, _ = str(mesh_parts).split(pathlib.os.sep)
        meta_file_temp = json.load(self.local_fs.open(row["metadata_file"])).update({"sysnetId": sysNetID, "modelId": modelId})
        meta_file_df = pnd.read_json(meta_file_temp, orient="split")
        print("this is row", meta_file_df.keys(), meta_file_df)
        return None

    def _get_per_obj_meta_json_path(self, row: str):
        """Gets the specific file path (verified exists) that"""
        if self.local_fs.exists(str(Path(row["mesh_file_path"]).parent.joinpath("model_normalized.json"))):
            return Path(row["mesh_file_path"]).parent / "model_normalized.json"
        else:
            return self.local_fs.ls(str(Path(row["mesh_file_path"]).parent.joinpath("*.json")))[0]

    def __len__(self):
        return len(self.dataCatalog)

    # get a row at an index 5375 ONE row of data
    def __getitem__(self, idx):

        sample = []
        return sample
