from pydantic import BaseModel, FilePath, DirectoryPath, validator, AnyUrl, Field, root_validator
from im23D_pipeline.pydantic_models.model_descriptions import *
from pathlib import Path
from enum import Enum


class MeshTypeChoices(Enum):
    mesh = "mesh"
    point_cloud = "point_cloud"
    sdf = "sdf"
    voxel = "voxel"
    
class BaseDatasetModel(BaseModel):
    """Base model for dataset inputs"""
    dataset_folder: DirectoryPath = Field(DirectoryPath, description=dataset_folder_description, cli=("-df", "--dataset-folder"))
    mesh_type: MeshTypeChoices = Field(MeshTypeChoices.mesh, description=mesh_type_description, cli=("", ""))
    
    @root_validator()
    def validate_fields(cls, values):
        """This validator can check values based on other values"""
        return values
        

class BaseAtomicDataObjectModel(BaseModel):
    """This will be the smalles `set` of items will need, think what gets fed into the model, what comes out, and anything it needs to get compared to
    This could be anything from an object file, an image (or set of images), camera angle, (maybe even textures) for scene generation via `trimesh`.
    ['synset_id', 'model_id', 'verts', 'faces', 'label', 'images', 'R', 'T', 'K', 'voxel_coords', 'voxels', 'mesh']
    is an example from the R2N2 Custom Dataset(and there's too much here) for one thing this should have to pass through a model and get a loss!"""        
    pass

class TrainerPydanticModel(BaseModel):
    """all the hyperparameter inputs should output some sort of file correlating to the run with the inputs --> output/performance + model
    i.e. this will be the cli with things like epochs, d"""
    pass
    