import typing
import torch
import numpy as np
from importlib.resources import contents, path
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

class RandomGamma():
    def __init__(self, random_gamma_delta):
        self.gamma_range = 1.0 - random_gamma_delta, 1.0 + random_gamma_delta

    def __call__(self, image):
        return np.power(image, np.random.uniform(*self.gamma_range))

class ClipImage():
    def __call__(self, image):
        return np.clip(image, 0.0, 1.0)

def get_class_name(function):
    return str(function).split()[2].split('.')[0]

def private_callable_test(bench: 'Testbench', callable_object : typing.Callable):
    function = bench.function
    input_data_pkg: str = 'testbench.tests.datasets.tensor_images'
    for resource in contents(input_data_pkg):
        if not resource.endswith('.pt'):
            continue
            
        with path(input_data_pkg, resource) as input_data_path:
            tensor_image = torch.load(str(input_data_path))
            np.random.seed(0)
            transformed_output = function(tensor_image)
            np.random.seed(0)
            transformed_base = callable_object(tensor_image)
            bench.assert_expr(torch.equal(transformed_base, transformed_output))



def private_test_clip_image(function):
    print('test ClipImage')

def test___call__(bench: 'Testbench'):
    if bench.function is None:
        return
    class_name = get_class_name(bench.function)
    if class_name == 'RandomGamma':
        private_callable_test(bench, RandomGamma(0.3))
    elif class_name == 'ClipImage':
        private_callable_test(bench, ClipImage())
    #add elif to test more callable classes
