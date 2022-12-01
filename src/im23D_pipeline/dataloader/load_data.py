import torch
from torch.utils.data import DataLoader, random_split
import pandas as pd
import os
import numpy as np
# from utils import read_datafile, reshape_data
from im23D_pipeline.dataloader import ShapeNetCoreDataset

def prepare_data(path: str,
                 num_workers: int = 0,
                 test_train_split: int = 0.2,
                 train_batch_size: int = 128,
                 test_batch_size: int = 128) -> tuple[torch.utils.data.dataloader.DataLoader,
                                                      torch.utils.data.dataloader.DataLoader]:
    """
    Function to prepare the data into test, train outputting the dataloader
    
    Credit: https://machinelearningmastery.com/pytorch-tutorial-develop-deep-learning-models/
    Parameters
    ----------
    path : str
        path to the csv catalog with all the filepaths and Reynolds numbers.
    num_workers: int
        number of parallel workers to call for a  DataLoader.
    Returns
    -------
    train_dl : torch.utils.data.dataloader.DataLoader
        Dataloader used for training.
    test_dl : torch.utils.data.dataloader.DataLoader
        Dataloader used for testing.
    """
    # load the dataset
    dataset = ShapeNetCoreDataset(path)
    # calculate split
    train, test = dataset.get_splits(test_train_split)

    # prepare data loaders
    train_dl = DataLoader(train, batch_size=train_batch_size,
                          shuffle=True, num_workers=num_workers)
    test_dl = DataLoader(test, batch_size=test_batch_size,
                         shuffle=False, num_workers=num_workers)
    return train_dl, test_dl