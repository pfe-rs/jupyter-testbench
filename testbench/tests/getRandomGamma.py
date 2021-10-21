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

def test_getRandomGamma(bench: 'Testbench'):
    if bench.function is None:
        return
    input_data_pkg: str = 'testbench.tests.datasets.tensor_images'
    test_values = [0.3, 0.6]
    for value in test_values:
        transformer_output = bench.function(value)
        transformer_base = RandomGamma(value)
        for resource in contents(input_data_pkg):
            if not resource.endswith('.pt'):
                continue
                
            with path(input_data_pkg, resource) as input_data_path:
                tensor_image = torch.load(str(input_data_path))
                np.random.seed(0)
                transformed_output = transformer_output(tensor_image)
                np.random.seed(0)
                transformed_base = transformer_base(tensor_image)
                bench.assert_expr(torch.equal(transformed_base, transformed_output))