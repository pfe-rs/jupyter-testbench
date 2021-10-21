import torch
import cv2
from importlib.resources import contents, path
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

def get_base(path: str) -> torch.Tensor:
    image = (cv2.imread(path).astype("float32") / 255.0)[:, :, ::-1].copy()
    return torch.from_numpy(image.transpose(2, 0, 1))

def test_image_loader(bench: 'Testbench'):
    if bench.function is None:
        return
    input_data_pkg: str = 'testbench.tests.datasets.image_loader.input'
    for resource in contents(input_data_pkg):
        if not resource.endswith('.jpg'):
            continue
        with path(input_data_pkg, resource) as input_data_path:
            tensor_out = bench.function(str(input_data_path))
            tensor_base = get_base(str(input_data_path))
            bench.assert_expr(torch.equal(tensor_base, tensor_out))