import torch
import cv2
import torchvision
import os
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

def split_data(ratios : list, dataset: torch.utils.data.DataLoader) -> list:
    DATASET_SEED = 12345
    torch_generator = torch.Generator().manual_seed(DATASET_SEED)
    dataset_size = len(dataset)
    sizes = [int(ratio * dataset_size) for ratio in ratios]
    return torch.utils.data.random_split(
        dataset, 
        sizes, 
        generator=torch.Generator().manual_seed(DATASET_SEED))

def test_split_data(bench : 'Testbench'):
    pth = os.path.dirname(os.path.realpath(__file__))
    dataset = torchvision.datasets.DatasetFolder(root=str(pth)+r"\datasets\classes_root", loader=image_loader, extensions="jpg")
    data_loader = getDataLoader(dataset, 2)
    ratios = [0.5, 0.5]
    bench.assert_expr(repr(split_data(ratios, data_loader)) == repr(bench.function(ratios, data_loader)))