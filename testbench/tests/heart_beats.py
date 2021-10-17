from importlib.resources import contents, path
import numpy as np

def heart_beats(data: np.array) -> int:
    signal=np.diff(data)
    br = 0
    i = 0
    while i<np.size(signal)-1:
        if signal[i] > 500000:
            br = br+1
            i = i + 100
        else:
            i = i + 1
    return br

def test_heart_beats(bench: 'Testbench'):
    hearth_beats_path = 'testbench.tests.datasets.heart_beats'
    for resource in contents(hearth_beats_path):
        if not resource.endswith('.dat'):
            continue
        with path(hearth_beats_path, resource) as data_path:
            file = np.fromfile(data_path, dtype = int)
            bench.assert_eq(bench.function(file), heart_beats(file))
        
