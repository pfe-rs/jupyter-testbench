from io import StringIO
import sys

expected = """Sequential(
  (0): Conv2d(1, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
  (1): BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (2): ReLU()
  (3): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
  (4): Conv2d(32, 64, kernel_size=(3, 3), stride=(1, 1))
  (5): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (6): ReLU()
  (7): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
  (8): Flatten(start_dim=1, end_dim=-1)
  (9): Linear(in_features=2304, out_features=600, bias=True)
  (10): Dropout2d(p=0.25, inplace=False)
  (11): Linear(in_features=600, out_features=120, bias=True)
  (12): Linear(in_features=120, out_features=10, bias=True)
)
"""

def test_return_fashioncnn(bench: 'Testbench'):

  old_stdout = sys.stdout

  result = StringIO()
  sys.stdout = result

  print(bench.function())

  result_string = result.getvalue()

  sys.stdout = old_stdout
  assert(expected == result_string)