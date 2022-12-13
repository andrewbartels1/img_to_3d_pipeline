from torch.utils.data import Dataset
from .base_dataset import img23DBaseDataset
from pathlib import Path
import pandas as pnd
import json

class Pix3dDataset(img23DBaseDataset):
    """The *Pix3d* Implementation of the img23D Dataset, this
    Loader is meant to only do the ShapeNet dataset, make a catalog,
    and generate specific types of output point cloud data etc. 
    per whatever model is needed.
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
        print("data catalog path", self.catalog_path)
        self.catalog_path_temp = self.catalog_path
        self.meta_list = []
        # ensure catalog path exists
        catalog_path_exists = Path(self.catalog_path).parent.mkdir(parents=True, exist_ok=True)

        # read the json file that has all the metadata; specific to the ShapeNet dataset
        _ = self._read_decryptor_ring_file_and_get_labels()
        
        # first generate a dictionary of items that need to be stored in the `dask` dataframe
        self.dataCatalog = pnd.DataFrame.from_dict({"mesh_file_path": self.dataset_list})
            
        # TODO: Tasks pending completion -@bartelsaa at 12/12/2022, 10:00:21 PM
        # CREATE the meta file for each obj from the super wiley and unreadable decryptor ring file (above)
        # self.dataCatalog["metadata_file"] = self.dataCatalog.apply(self._get_per_obj_meta_json_path, axis=1)
        
        self.dataCatalog = self._get_labels_from_meta_file()
        
        print("data catalog so far", self.dataCatalog)
        self.dataCatalog.to_csv(self.catalog_path)
        return self.catalog_path
        
    def _read_decryptor_ring_file_and_get_labels(self):

            # load the meta data file (json in this case)
            meta_data_label_file = json.load(self.local_fs.open(self.decryptor_ring_file))

            meta_data_label_file_df = pnd.json_normalize(meta_data_label_file)

            # get a simple label from the label options (ShapeNet Specific)
            meta_data_label_file_df["simple_label"] = meta_data_label_file_df["category"]

            # if self.verbose:
            #     print(
            #         "-----------------meta data file-----------------\n\n",
            #         meta_data_label_file_df.head,
            #     )

            self.meta_data_label_df = meta_data_label_file_df

            # write out meta file to csv for historical reference.
            print("saving meta data to ",Path(self.catalog_path).parent)
            self.meta_data_label_df.to_csv(Path(self.catalog_path).parent / "meta_catalog.csv")

            return self.meta_data_label_df
        
        
        
    def _get_labels_from_meta_file(self):
        """Do a simple merge to get all the models"""
        
        temp = self.dataCatalog["mesh_file_path"].str.split("model", n = 1, expand = True)
        
        self.dataCatalog["model"] = "model" + temp[1]
        print(self.dataCatalog["model"])
        self.dataCatalog = pnd.merge(
            self.dataCatalog, self.meta_data_label_df, left_on="model", right_on="model"
        )
        
        self.dataCatalog = self.dataCatalog.rename({'category': 'simple_label'}, axis="columns")

        
        return self.dataCatalog[["mesh_file_path", "simple_label"]]
        
    # def _get_per_obj_meta_json_path(self, row: str):
    #     """Gets the specific file path (verified exists) that"""
    #     if self.local_fs.exists(str(Path(row["mesh_file_path"]).parent.joinpath("model_normalized.json"))):
    #         return Path(row["mesh_file_path"]).parent / "model_normalized.json"
    #     else:
    #         return None
        
        