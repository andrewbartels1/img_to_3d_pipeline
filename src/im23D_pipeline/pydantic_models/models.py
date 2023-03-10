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


class DataBaseModel(BaseModel):
    """Fill this in when there are multiple pydantic models with repeated variables"""
    # folder and obj location stuff
    dataset_folder: DirectoryPath = Field(
        DirectoryPath, description=dataset_folder_description, cli=("-df", "--dataset-folder")
    )
    mesh_type: str = Field(MeshTypeChoices.mesh.value, description=mesh_type_description, cli=("-m", "--mesh"))
    data_file_type: str = Field(DataFileTypeChoices.obj.value, description=data_file_type_description)
    # fsspec stuff
    storage_options_remote: Optional[Dict[str, Any]] = Field({}, description=storage_option_description)
    local_protocol: Optional[str] = Field("file", description=protocol_description)
    local_fs: Optional[Any]  # don't actually use this, it's generate based on other things
    verbose: bool = Field(False, description="prints verbose output")
    decryptor_ring_file: FilePath = Field(
        "../data/ShapeNetCore.v2/taxonomy.json",
        description=decryptor_ring_file_description,
        cli=("-drf", "--descryptor-ring-file"),
    )
    data_catalog_file: Optional[str] = Field("datacatalog_parts/datacatalog.csv", description=data_catalog_file_description)
    data_catalog_file_type: Optional[str] = Field(
        "csv", description="data catalog output type (only csv supported currently)"
    )
    refresh_data_catalog: bool = Field(False, description=refresh_data_catalog_description)
    dataset_list: List = Field([], description=dataset_list_description)
    datacatalog_path: List = Field([], description=datacatalog_path_description)

    @root_validator()
    def validate_fields(cls, values):
        """This validator can check values based on other values"""

        values["local_fs"] = fsspec.filesystem(values.get("local_protocol"), storage_options=values.get("storage_options"))

        # glob the dataset list
        if not values.get("dataset_list"):
            # ! NOTE: THIS DOESN'T WORK ON S3FS Because it doesn't have a concept of folders
            print(
                "finding all files in:",
                values.get("dataset_folder").as_posix() + "/**/*." + values.get("data_file_type"),
            )
            values["dataset_list"] = values["local_fs"].glob(
                values.get("dataset_folder").as_posix() + "**/*." + values.get("data_file_type")
            )
            print(
                "found {} number of {} files in the dataset".format(
                    len(values["dataset_list"]), values.get("data_file_type")
                )
            )

        assert (
            len(values["dataset_list"]) > 0
        ), "something went wrong with locating mesh files in {}, maybe check to ensure the file extension is correct?".format(
            values.get("dataset_folder").as_posix()
        )

        values["datacatalog_path"] = Path(values["dataset_folder"].as_posix()).joinpath(
            "".join(("datacatalog_parts/datacatalog.csv"))
        )
        
        print("datacatalot path is:", values["datacatalog_path"])

        return values

    # For fsspec stuff
    class Config:
        arbitrary_types_allowed = True
        
        
class ShapeNetModel(DataBaseModel):
    """Base model for dataset inputs of ShapeNet"""
    pass

class Pix3dModel(DataBaseModel):
    """Base model for dataset inputs of Pix3d"""
    decryptor_ring_file: FilePath = Field(
        "../data/pix3d_full/pix3d.json",
        description=decryptor_ring_file_description,
        cli=("-drf", "--descryptor-ring-file"),
    )
    
    


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
