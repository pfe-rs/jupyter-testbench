from testbench import Testbench

import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
import numpy as np

Testbench.author('Petar Petrović')

def image_loader(path: str) -> torch.Tensor:
    image = (cv2.imread(path).astype("float32") / 255.0)[:, :, ::-1].copy()
    return torch.from_numpy(image.transpose(2, 0, 1))

class RandomGamma():
    def __init__(self, random_gamma_delta):
        np.random.seed(0)
        self.gamma_range = 1.0 - random_gamma_delta, 1.0 + random_gamma_delta

    def __call__(self, image):
        return np.power(image, np.random.uniform(*self.gamma_range))

class ClipImage():

    def __call__(self, image):
        return np.clip(image, 0.0, 1.0)
        

if __name__ == '__main__':
    Testbench(image_loader)
    Testbench(RandomGamma(0.3).__call__)
    Testbench(ClipImage().__call__)