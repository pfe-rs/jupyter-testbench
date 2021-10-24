import torch
import torch.nn as nn
import torch.nn.functional as F
from importlib.resources import contents, path
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import Testbench

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
        nn.Linear(in_features=120, out_features=10),)

def test_return_fashioncnn(bench: 'Testbench'):
  if bench.function is None:
    return
  bench.assert_expr(repr(return_fashioncnn()) == repr(bench.function()))