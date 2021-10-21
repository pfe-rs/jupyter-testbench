import typing
import torch
import numpy as np
from importlib.resources import contents, path
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

class ClipImage():
    def __call__(self, image):
        return np.clip(image, 0.0, 1.0)

def test_getClipImage(bench: 'Testbench'):
    if bench.function is None:
        return

    input_data_pkg: str = 'testbench.tests.datasets.tensor_images'

    transformer_output = bench.function()
    transformer_base = ClipImage()
    for resource in contents(input_data_pkg):
        if not resource.endswith('.pt'):
            continue
            
        with path(input_data_pkg, resource) as input_data_path:
            tensor_image = torch.load(str(input_data_path))
            transformed_output = transformer_output(tensor_image)
            transformed_base = transformer_base(tensor_image)
            bench.assert_expr(torch.equal(transformed_base, transformed_output))