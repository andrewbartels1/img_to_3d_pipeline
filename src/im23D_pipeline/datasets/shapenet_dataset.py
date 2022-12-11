import os
import json
from os import path
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
import torch
from im23D_pipeline.pydantic_models import ShapeNetModel
from .base_dataset import img23DBaseDataset
# import dask.dataframe as dd
import pandas as pnd
import pathlib
from operator import itemgetter
from tqdm import tqdm
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
        self.meta_list = []
        # ensure catalog path exists
        catalog_path_exists = Path(self.catalog_path).parent.mkdir(parents=True, exist_ok=True)
        
        # read the json file that has all the metadata; specific to the ShapeNet dataset
        _ = self._read_decryptor_ring_file_and_get_labels()

        # first generate a dictionary of items that need to be stored in the `dask` dataframe
        self.dataCatalog = pnd.DataFrame.from_dict({"mesh_file_path": self.dataset_list})

        # run sets of functions to add columns, it's kind of slow, but it should only need to do this once!
        self.dataCatalog["metadata_file"] = self.dataCatalog.apply(self._get_per_obj_meta_json_path, axis=1)
        
        
        self.column_names_to_add_from_meta = self._get_column_names_to_add_from_meta()
        
        print("adding columns:", self.column_names_to_add_from_meta)
        
        # add label column while we're at it
        # column_names_to_add_from_meta.append("simple_label")
        
        # add the empty columns to fill up in the slow apply function
        tqdm.pandas(desc="reading metadata per .obj file")
        
        self.dataCatalog.progress_apply(self._assign_metadata_and_labels_for_meshes, axis=1, result_type="expand")
        
        # self.dataCatalog[list(temp.columns)] = temp
        self.dataCatalog = pnd.DataFrame(self.meta_list)
        
        self.dataCatalog.to_csv(self.catalog_path)
        
        # merge the meta data descriptor file to get all the labels
        self.dataCatalog = pnd.merge(self.dataCatalog, self.meta_data_label_df, left_on="sysnetId", right_on="synsetId").drop(["children", "name"],axis=1)
        
        self.dataCatalog.to_csv(self.catalog_path)
        
        print(self.dataCatalog.head(10))
        
        return self.catalog_path

    def _read_decryptor_ring_file_and_get_labels(self):
        
        # load the meta data file (json in this case)
        meta_data_label_file = json.load(self.local_fs.open(self.decryptor_ring_file))
        
        meta_data_label_file_df = pnd.DataFrame(meta_data_label_file)

        # get a simple label from the label options (ShapeNet Specific)
        meta_data_label_file_df["simple_label"] = meta_data_label_file_df["name"].apply(lambda x: x.split(",")[0])

        # if self.verbose:
        #     print(
        #         "-----------------meta data file-----------------\n\n",
        #         meta_data_label_file_df.head,
        #     )

        self.meta_data_label_df = meta_data_label_file_df
        
        # write out meta file to csv for historical reference.
        self.meta_data_label_df.to_csv(Path(self.catalog_path).parent / "meta_catalog.csv")
        
        return self.meta_data_label_df

    def _assign_metadata_and_labels_for_meshes(self, row):
        """Open a json metadata file (shapenet specific) and get a centroid, bounding box, and simple label, etc."""
        
        # get the sysnetId and modelId for a linker to the meta data.       
        sysNetId, modelId = self._get_ids_from_path(Path(row.mesh_file_path))
        
        # open the metadata file specific to that .obj file
        meta_file_temp = json.load(row["metadata_file"].open())
        
        # update with the Ids to link to meta data label
        meta_file_temp.update({"sysnetId": sysNetId, "modelId": modelId})
        
        meta_file_df = pnd.json_normalize(meta_file_temp, sep="_")
        
        object_to_return = self.decompress_obj_meta_file_to_row(meta_file_df)
        
        # do some joining of keys and append to dictionary
        temp = object_to_return.to_dict(orient="records")
        row_dict = row.to_dict()
        returns_from = {**row_dict, **temp[0]}
        
        # remove keys
        [returns_from.pop(key) for key in ["id"]]
        
        self.meta_list.append(returns_from)
        
        return None

    def _get_column_names_to_add_from_meta(self) -> list:
        """Gets all the columns the meta data rows will add to the dataframe"""
        
        # send dask to df 
        temp = self.dataCatalog
        
        # get a row
        sysNetId, modelId = self._get_ids_from_path(temp.loc[0, :]["mesh_file_path"])
        
        # open the object specific metadata file.
        meta_file_temp = json.load(Path(temp.loc[0, :]["metadata_file"]).open())
        meta_file_temp.update({"sysnetId": sysNetId, "modelId": modelId})
        
        # send to df, "flatten" anything that's nested
        meta_file_df = pnd.json_normalize(meta_file_temp, sep="_")
                
        meta_file_df = self.decompress_obj_meta_file_to_row(meta_file_df)
        
        return meta_file_df.columns.tolist()
    
    def decompress_obj_meta_file_to_row(self, meta_file_row_df: pnd.DataFrame, columns_to_expand=["min", "max", "centroid"]):
        """Unwraps meta dict from lists to one float/item per column 
        (e.g. min = [0.11, 0.1, 0.2] -> 'min_0', 'min_1', 'min_2' with 
        the corresponding number in each column)"""        
        
        for col in columns_to_expand:
            new_df = meta_file_row_df[col].transform({f'{col}_{i}': itemgetter(i) for i in [0,1,2]})
            meta_file_row_df[ list(new_df.columns) ] = new_df
        
        # drop all the list type columns
        meta_file_row_df.drop(columns_to_expand, inplace=True, axis=1)
    
        return meta_file_row_df
    
    def _get_per_obj_meta_json_path(self, row: str):
        """Gets the specific file path (verified exists) that"""
        if self.local_fs.exists(str(Path(row["mesh_file_path"]).parent.joinpath("model_normalized.json"))):
            return Path(row["mesh_file_path"]).parent / "model_normalized.json"
        else:
            return self.local_fs.ls(str(Path(row["mesh_file_path"]).parent.joinpath("*.json")))[0]

    def _get_ids_from_path(self, mesh_file_path: Path):
        """Gets the Sysnet and model Ids from the mesh file path"""

        # split on the ShapeNet folder name to establish where to start splitting!
        mesh_parts = Path(str(mesh_file_path).split("ShapeNet")[-1]).parents[0]
        
        _, sysNetId, modelId, _ = str(mesh_parts).split(pathlib.os.sep)
        
        return sysNetId, modelId
        
    def __len__(self):
        return len(self.dataCatalog)

    # get a row at an index 5375 ONE row of data
    def __getitem__(self, idx):

        sample = []
        return sample
