from pydantic import BaseModel, FilePath, DirectoryPath, validator, AnyUrl, Field, root_validator
from im23D_pipeline.pydantic_models.model_descriptions import *
from pathlib import Path
from enum import Enum
from typing import List, Optional, Any, Dict
import fsspec


class MeshTypeChoices(Enum):
    mesh = "mesh"
    point_cloud = "point_cloud"
    sdf = "sdf"
    voxel = "voxel"

class DataFileTypeChoices(Enum):
    obj = "obj"
    glb = "glb"
    # voxel = "voxel"

class ShapeNetModel(BaseModel):
    """Base model for dataset inputs"""

    dataset_folder: DirectoryPath = Field(
        DirectoryPath, description=dataset_folder_description, cli=("-df", "--dataset-folder")
    )
    mesh_type: str = Field(
        MeshTypeChoices.mesh.value, description=mesh_type_description, cli=("-m", "--mesh")
    )
    data_file_type: str = Field(DataFileTypeChoices.obj.value, description=data_file_type_description)
    decryptor_ring_file: FilePath = Field(
        "../data/ShapeNetCore.v2/taxonomy.json",
        description=decryptor_ring_file_description,
        cli=("-drf", "--descryptor-ring-file"),
    )
    dataset_list: List = Field([], description=dataset_list_description)
    storage_options_remote: Optional[Dict[str, Any]] = Field({}, description=storage_option_description)
    local_protocol: Optional[str] = Field("file", description=protocol_description)
    local_fs: Optional[Any] # don't actually use this, it's generate based on other things

    @root_validator()
    def validate_fields(cls, values):
        """This validator can check values based on other values"""
        
        values["local_fs"] = fsspec.filesystem(values.get("local_protocol"), storage_options=values.get("storage_options"))
        
        # glob the dataset list
        if not values.get("dataset_list"):
            # ! NOTE: THIS DOESN'T WORK ON S3FS Because it doesn't have a concept of folders
            print(type(values.get("dataset_folder")))
            print(values.get("mesh_type"))
            print(values.get("data_file_type"))
            print("finding all files in:", values.get("dataset_folder").as_posix() + "/**/*." + values.get("data_file_type"))
            values["dataset_list"] = values["local_fs"].glob(values.get("dataset_folder").as_posix() + "**/*." + values.get("data_file_type"))

        
        return values
    
    # For fsspec stuff
    class Config:
        arbitrary_types_allowed = True


class BaseAtomicShapeNetInput(BaseModel):
    """This will be the smalles `set` of items will need, think what gets fed into the model, what comes out, and anything it needs to get compared to
    This could be anything from an object file, an image (or set of images), camera angle, (maybe even textures) for scene generation via `trimesh`.
    ['synset_id', 'model_id', 'verts', 'faces', 'label', 'images', 'R', 'T', 'K', 'voxel_coords', 'voxels', 'mesh']
    is an example from the R2N2 Custom Dataset(and there's too much here) for one thing this should have to pass through a model and get a loss!"""

    pass


class TrainerPydanticModel(BaseModel):
    """all the hyperparameter inputs should output some sort of file correlating to the run with the inputs --> output/performance + model
    i.e. this will be the cli with things like epochs, d"""

    pass
