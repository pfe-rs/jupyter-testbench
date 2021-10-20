from io import StringIO
import sys

expected = """Net(
  (conv1): Conv2d(3, 16, kernel_size=(5, 5), stride=(1, 1))
  (pool): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
  (conv2): Conv2d(16, 32, kernel_size=(5, 5), stride=(1, 1))
  (fc1): Linear(in_features=5408, out_features=120, bias=True)
  (fc2): Linear(in_features=120, out_features=84, bias=True)
  (fc3): Linear(in_features=84, out_features=10, bias=True)
)
"""

def test_return_model1(bench: 'Testbench'):

  old_stdout = sys.stdout

  result = StringIO()
  sys.stdout = result

  print(bench.function())

  result_string = result.getvalue()

  sys.stdout = old_stdout
  assert(expected == result_string)