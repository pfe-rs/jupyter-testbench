import cv2
import numpy as np
from importlib.resources import contents, path
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

def test_binarization(bench: 'Testbench'):
    if bench.function is None:
        return
    base_data_pkg: str = 'testbench.tests.datasets.binarization'
    input_data_pkg: str = f'{base_data_pkg}.input'
    output_data_pkg: str = f'{base_data_pkg}.output'
    for resource in contents(input_data_pkg):
        if not resource.endswith('.png'):
            continue
        image_in = None
        image_out = None
        with path(input_data_pkg, resource) as data_path:
            image_in = cv2.imread(str(data_path))
        with path(output_data_pkg, resource) as data_path:
            image_out = cv2.imread(str(data_path))
            image_out = cv2.cvtColor(image_out, cv2.COLOR_RGB2GRAY)
        image_test: np.ndarray = bench.function(np.array(image_in))
        bench.assert_expr(np.array_equal(image_out, image_test))
