import os
import json
from os import path
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np

# import torch
# from PIL import Image
# from pytorch3d.common.types import Device
# from pytorch3d.datasets.shapenet_base import ShapeNetBase
# from pytorch3d.renderer import HardPhongShader
# from tabulate import tabulate
# from pytorch3d.datasets.r2n2 import utils
# from pytorch3d.datasets.r2n2.utils import (
#     BlenderCamera,
#     align_bbox,
#     compute_extrinsic_matrix,
#     read_binvox_coords,
# )
# import utils_vox

import torch
from torch.utils.data import Dataset, DataLoader, random_split

SYNSET_DICT_DIR = Path(utils.__file__).resolve().parent
print("SYNSET_DICT_DIR", SYNSET_DICT_DIR)
MAX_CAMERA_DISTANCE = 1.75  # Constant from R2N2.
VOXEL_SIZE = 128
# Intrinsic matrix extracted from Blender. Taken from meshrcnn codebase:
# https://github.com/facebookresearch/meshrcnn/blob/main/shapenet/utils/coords.py
BLENDER_INTRINSIC = torch.tensor(
    [
        [2.1875, 0.0, 0.0, 0.0],
        [0.0, 2.1875, 0.0, 0.0],
        [0.0, 0.0, -1.002002, -0.2002002],
        [0.0, 0.0, -1.0, 0.0],
    ]
)

class img23DBaseDataset(Dataset):
    raise NotImplementedError

class R2N2Dataset(Dataset):
    raise NotImplementedError

class ShapeNetCoreDataset(Dataset):
    raise NotImplementedError

class ABODataset(Dataset):
    raise NotImplementedError

