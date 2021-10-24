import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
from sklearn.metrics import accuracy_score
from importlib.resources import contents, path
import torchvision
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

def measure_quality(model : nn.Sequential, dataset : torch.utils.data.Dataset, device : any, max_batches: int=None) -> float:
    model.eval()
    iteration_cnt = 0

    all_preds = list()
    all_labels = list()

    with torch.no_grad():
        for i, data in enumerate(dataset):
            if max_batches is not None and iteration_cnt == max_batches:
                break

            inputs, labels = data[0].to(device), data[1].to(device)

            outputs = model(inputs)
            _, pred = torch.max(outputs, 1)

            all_preds += list(pred.data.cpu().numpy())
            all_labels += list(labels.data.cpu().numpy())

            iteration_cnt += 1

    model.train()

    return accuracy_score(all_labels, all_preds)

def getDataLoader(dataset : torch.utils.data.Dataset , batch_size : int) -> torch.utils.data.DataLoader:
    return torch.utils.data.DataLoader(
        dataset, 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=0, 
        drop_last=True, 
        pin_memory=True)

def image_loader(path: str) -> torch.Tensor:
    image = (cv2.imread(path).astype("float32") / 255.0)[:, :, ::-1].copy()
    return torch.from_numpy(image.transpose(2, 0, 1))

def get_transfer_learning_model():
    model = torchvision.models.resnet50(pretrained=True)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 10)
    return model

def test_measure_quality(bench: 'Testbench'):
    if bench.function is None:
      return
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = get_transfer_learning_model()
    model.to_device(device)
    dataset = torchvision.datasets.DatasetFolder(
        root=r"datasets\classes_root", 
        loader=image_loader, extensions="jpg")
    dataLoader = getDataLoader(dataset, 2)
    bench.assert_expr(measure_quality(model, dataLoader, device) == bench.function(model, dataLoader, device))