"""
@Author: andrew.bartels  (andrew.bartels@gatech.edu) 
@Date: 2022-12-01 13:39:08  
@Last Modified by:   andrew.bartels  
@Last Modified time: 2022-12-01 13:39:08 
@license: see LICENSE for more details 
"""
from fsspec.registry import known_implementations

# All model descriptions for the pydantic models should go here


# ShapeNetModel variable description
field_description = "test model desscription"
dataset_folder_description = "pathlib.Path object that holds the folder where the dataset lives, for example `../data/ShapeNetCore.v2/` will be used for the `"
mesh_type_description = "Enumerator object that will only accept the mesh type that will be preprocessed by the dataset class and loaded into the dataloader"
decryptor_ring_file_description = "json type file that has all the mapping between any folder/path/file to what the label is, orientation of the images, etc."
dataset_list_description = (
    "list of .obj or .glb files (Path Objects) that point to the files to be written to the data catalog"
)
protocol_description = (
    f"""protocol that's used for remote file storage. Current supported files are: {known_implementations}"""
)
storage_option_description = "storage option dictionary for keys/secrets to authenticate with a file system. The key inputs can vary largely depending on which file system is being used! See the fsspec specific file system docs by a 'type(some-fs-object)'"
data_file_type_description = (
    "file type ending (e.g. .obj, .glb, .etc) *needs* to be a 3D file readable by `trimesh`!"
)
data_catalog_file_description = "path to the data catalog with all the locations of files and metadata mappings. If this is the first time running the dataset, this will generate automagically, if the path exists, this will save you some time to not regenerate every time."
refresh_data_catalog_description = "runs the function that regenerates the data catalog, unless new data is put in there, this should be left as `False`"
datacatalog_path_description = (
    "could be changed, but outputs a glob string where dask will write out the dataset parts."
)
