import torch
import numpy as np
from importlib.resources import contents, path, is_resource
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

def test_image_loader(bench: 'Testbench'):
    if bench.function is None:
        return
    base_data_pkg: str = 'testbench.tests.datasets.image_loader'

    input_data_pkg: str = f'{base_data_pkg}.input'
    output_data_pkg: str = f'{base_data_pkg}.output'

    for resource in contents(input_data_pkg):
        if not resource.endswith('.jpg'):
            continue

        image_out = None
        with path(input_data_pkg, resource) as data_path:
            image_out = bench.function(str(data_path))
        image_test: np.ndarray = bench.function(str(data_path))
        bench.assert_expr(np.array_equal(image_out, image_test))