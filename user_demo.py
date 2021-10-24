from torch.functional import Tensor
from testbench import Testbench

import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
import torchvision
import numpy as np
from sklearn.metrics import accuracy_score


Testbench.author('Petar Petrović')

def image_loader(path: str) -> torch.Tensor:
    image = (cv2.imread(path).astype("float32") / 255.0)[:, :, ::-1].copy()
    return torch.from_numpy(image.transpose(2, 0, 1))

class RandomGamma():
    def __init__(self, random_gamma_delta):
        self.gamma_range = 1.0 - random_gamma_delta, 1.0 + random_gamma_delta

    def __call__(self, image):
        return np.power(image, np.random.uniform(*self.gamma_range))

    def __repr__(self):
        return 'RandomGamma('+str(self.gamma_range)+')'

class ClipImage():
    def __call__(self, image):
        return np.clip(image, 0.0, 1.0)

    def __repr__(self):
        return 'ClipImage()'
        
def getRandomGamma(randaom_gamma_delta : float) -> RandomGamma:
    return RandomGamma(randaom_gamma_delta)

def getClipImage() -> ClipImage:
    return ClipImage()

#dummy
def return_model1() -> torch.nn :
    return 0

def getNN() -> nn.Sequential:
    return nn.Sequential(
        nn.Conv2d(3, 16, 5),
        nn.BatchNorm2d(16),
        nn.ReLU(),
        nn.MaxPool2d(2, 2),
        nn.Conv2d(16, 32, 5),
        nn.BatchNorm2d(32),
        nn.ReLU(),
        nn.MaxPool2d(2, 2),
        nn.Flatten(),
        nn.Linear(32 * 53 * 53, 120),
        nn.BatchNorm1d(120),
        nn.ReLU(),
        nn.Linear(120, 84),
        nn.BatchNorm1d(84),
        nn.ReLU(),
        nn.Linear(84, 10))

def return_fashioncnn() -> nn.Sequential:
    return nn.Sequential(
    nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1),
    nn.BatchNorm2d(32),
    nn.ReLU(),
    nn.MaxPool2d(kernel_size=2, stride=2),
    
    nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3),
    nn.BatchNorm2d(64),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),

    nn.Linear(in_features=64*6*6, out_features=600),
    nn.Dropout2d(0.25),
    nn.Linear(in_features=600, out_features=120),
    nn.Linear(in_features=120, out_features=10),
)

def measure_quality(model : nn.Sequential, loader : torch.utils.data.DataLoader, device : any, max_batches: int=None) -> float:
    model.eval()
    iteration_cnt = 0

    all_preds = list()
    all_labels = list()

    with torch.no_grad():
        for i, data in enumerate(loader):
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

def split_data(ratios : list, dataset: torch.utils.data.DataLoader) -> list:
    DATASET_SEED = 12345
    torch_generator = torch.Generator().manual_seed(DATASET_SEED)
    dataset_size = len(dataset)
    sizes = [int(ratio * dataset_size) for ratio in ratios]
    return torch.utils.data.random_split(
        dataset, 
        sizes, 
        generator=torch.Generator().manual_seed(DATASET_SEED))

def getDataLoader(dataset : torch.utils.data.Dataset , batch_size : int) -> torch.utils.data.DataLoader:
    return torch.utils.data.DataLoader(
        dataset, 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=0, 
        drop_last=True, 
        pin_memory=True)

def get_transfer_learning_model() -> torchvision.models.ResNet:
    model = torchvision.models.resnet50(pretrained=True)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 10)
    return model

def compose_transforms() -> torchvision.transforms.Compose:
    return torchvision.transforms.Compose([
    RandomGamma(0.3),
    ClipImage(),
    torchvision.transforms.ToPILImage(),
    torchvision.transforms.Resize(224),
    torchvision.transforms.RandomHorizontalFlip(),
    torchvision.transforms.RandomVerticalFlip(),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

if __name__ == '__main__':
    Testbench(image_loader)
    Testbench(getRandomGamma)
    Testbench(getClipImage)
    Testbench(getNN)
    Testbench(split_data)
    Testbench(getDataLoader)
    Testbench(compose_transforms)
    Testbench(get_transfer_learning_model)
    Testbench(measure_quality)
    Testbench(return_fashioncnn)
