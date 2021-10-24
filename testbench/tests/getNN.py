import torch
import torch.nn as nn
import torch.nn.functional as F
from importlib.resources import contents, path
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

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
def test_getNN(bench: 'Testbench'):
    if bench.function is None:
        return
    bench.assert_expr(repr(getNN()) == repr(bench.function()))