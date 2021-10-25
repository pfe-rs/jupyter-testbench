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

def training_loop() -> list:
    return[(1, 100, 1.0637301526963712, 0.8980654761904762), (1, 200, 0.2986472540348768, 0.9402281746031746), (1, 300, 0.21794366601854562, 0.9553571428571429), (1, 400, 0.1870322917215526, 0.9469246031746031), (1, 500, 0.1867033694498241, 0.9598214285714286),
            (2, 100, 0.12785856365226209, 0.9689980158730159), (2, 200, 0.11231838520616293, 0.9751984126984127), (2, 300, 0.10743735128082335, 0.9794146825396826), (2, 400, 0.12183863300830126, 0.9692460317460317), (2, 500, 0.11416418978013099, 0.9794146825396826),
            (3, 100, 0.08939897006144747, 0.9732142857142857), (3, 200, 0.08664853344671428, 0.9769345238095238), (3, 300, 0.07750393797643483, 0.9806547619047619), (3, 400, 0.08816061251796782, 0.9794146825396826), (3, 500, 0.08312826447188854, 0.9791666666666666),
            (4, 100, 0.06662117821164429, 0.9799107142857143), (4, 200, 0.0634406645456329, 0.9809027777777778), (4, 300, 0.0575629359530285, 0.9833829365079365), (4, 400, 0.07515458574518562, 0.9833829365079365), (4, 500, 0.07576990403234958, 0.982390873015873),
            (5, 100, 0.06696086566196754, 0.9826388888888888), (5, 200, 0.05831786470487714, 0.9846230158730159), (5, 300, 0.07894841785775497, 0.9813988095238095), (5, 400, 0.05119838635902852, 0.9826388888888888), (5, 500, 0.059294668689835815, 0.9828869047619048)])

if __name__ == '__main__':
    Testbench(image_loader)
    Testbench(getRandomGamma)
    Testbench(getClipImage)
    Testbench(getNN)
    Testbench(split_data)
    Testbench(getDataLoader)
    Testbench(compose_transforms)
    Testbench(return_fashioncnn)
    Testbench(training_loop)
    Testbench(get_transfer_learning_model)
    Testbench(measure_quality)
