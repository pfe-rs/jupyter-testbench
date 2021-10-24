expected = [(1, 100, 1.0637301526963712, 0.8980654761904762), (1, 200, 0.2986472540348768, 0.9402281746031746), (1, 300, 0.21794366601854562, 0.9553571428571429), (1, 400, 0.1870322917215526, 0.9469246031746031), (1, 500, 0.1867033694498241, 0.9598214285714286),
            (2, 100, 0.12785856365226209, 0.9689980158730159), (2, 200, 0.11231838520616293, 0.9751984126984127), (2, 300, 0.10743735128082335, 0.9794146825396826), (2, 400, 0.12183863300830126, 0.9692460317460317), (2, 500, 0.11416418978013099, 0.9794146825396826),
            (3, 100, 0.08939897006144747, 0.9732142857142857), (3, 200, 0.08664853344671428, 0.9769345238095238), (3, 300, 0.07750393797643483, 0.9806547619047619), (3, 400, 0.08816061251796782, 0.9794146825396826), (3, 500, 0.08312826447188854, 0.9791666666666666),
            (4, 100, 0.06662117821164429, 0.9799107142857143), (4, 200, 0.0634406645456329, 0.9809027777777778), (4, 300, 0.0575629359530285, 0.9833829365079365), (4, 400, 0.07515458574518562, 0.9833829365079365), (4, 500, 0.07576990403234958, 0.982390873015873),
            (5, 100, 0.06696086566196754, 0.9826388888888888), (5, 200, 0.05831786470487714, 0.9846230158730159), (5, 300, 0.07894841785775497, 0.9813988095238095), (5, 400, 0.05119838635902852, 0.9826388888888888), (5, 500, 0.059294668689835815, 0.9828869047619048)]

def test_training_loop(bench: 'Testbench'):
  bench.assert_eq(bench.function(), expected)