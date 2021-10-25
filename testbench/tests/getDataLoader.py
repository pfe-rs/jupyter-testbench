import torch
import cv2
import os
import torchvision
from importlib.resources import contents, path
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

def image_loader(path: str) -> torch.Tensor:
    image = (cv2.imread(path).astype("float32") / 255.0)[:, :, ::-1].copy()
    return torch.from_numpy(image.transpose(2, 0, 1))

def getDataLoader(dataset : torch.utils.data.Dataset , batch_size : int) -> torch.utils.data.DataLoader:
    return torch.utils.data.DataLoader(
        dataset, 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=0, 
        drop_last=True, 
        pin_memory=True)

def test_getDataLoader(bench : 'Testbench'):
    dirr = os.path.dirname(os.path.realpath(__file__))
    pth = os.path.join(dirr, "datasets/classes_root")
    dataset = torchvision.datasets.DatasetFolder(root=str(pth), loader=image_loader, extensions="jpg")
    data_loader = getDataLoader(dataset, 2)
    bench.assert_expr(repr(getDataLoader(dataset, 2))==repr(bench.function(dataset, 2)))