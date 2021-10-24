import torchvision
import numpy as np
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

class ClipImage():
    def __call__(self, image):
        return np.clip(image, 0.0, 1.0)
    
    def __repr__(self):
        return 'ClipImage()'
    
class RandomGamma():
    def __init__(self, random_gamma_delta):
        self.gamma_range = 1.0 - random_gamma_delta, 1.0 + random_gamma_delta

    def __call__(self, image):
        return np.power(image, np.random.uniform(*self.gamma_range))
    
    def __repr__(self):
        return 'RandomGamma('+str(self.gamma_range)+')'

        

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

def test_compose_transforms(bench : 'Testbench'):
    tmp=compose_transforms()
    for base, output in zip(compose_transforms().transforms, bench.function().transforms):
        bench.assert_expr(repr(base)== repr(output))