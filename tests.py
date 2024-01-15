import pytest
from tic_tac_toe_bot import bots_turn, won


@pytest.mark.parametrize(
    'input, expected_result',
    [
        ([['.', '.', '.'],
          ['.', '.', '.'],
          ['.', '.', '.']],
         [(i, j) for i in range(3) for j in range(3)]),
        ([['.', '.', '.'],
          ['.', 'X', '.'],
          ['.', '.', '.']],
         [(i, j) for i in range(3) for j in range(3) if (i != 1 or j != 1)]),
        ([['X', '.', '.'],
          ['.', '.', 'X'],
          ['.', 'O', '.']],
         [(0, 1), (0, 2),
          (1, 0), (1, 1),
          (2, 0), (2, 2)]),
        ([['X', 'O', 'O'],
          ['X', '.', 'X'],
          ['O', 'X', '.']],
         [(1, 1),
          (2, 2)]),
        ([['X', 'O', 'X'],
          ['X', 'O', 'O'],
          ['O', 'X', 'X']],
         [])
    ]
)
def test_bots_turn(input, expected_result):
    if len(expected_result) > 0:
        assert bots_turn(input) in expected_result
    else:
        with pytest.raises(ValueError):
            bots_turn(input)


@pytest.mark.parametrize(
    'input, sign, expected_result',
    [
        ([['.', '.', '.'],
          ['.', '.', '.'],
          ['.', '.', '.']], 'X', False),
        ([['.', '.', '.'],
          ['.', '.', '.'],
          ['.', '.', '.']], 'O', False),
        ([['.', '.', '.'],
          ['.', 'X', '.'],
          ['.', '.', '.']], 'X', False),
        ([['X', 'O', '.'],
          ['.', '.', 'X'],
          ['.', '.', '.']], 'X', False),
        ([['X', 'O', 'O'],
          ['X', '.', 'O'],
          ['X', 'X', '.']], 'X', True),
        ([['O', 'O', 'O'],
          ['X', 'X', 'O'],
          ['X', 'X', '.']], 'O', True),
        ([['O', 'O', 'X'],
          ['X', 'X', 'O'],
          ['X', 'X', '.']], 'X', True),
        ([['X', 'O', 'O'],
          ['X', 'O', '.'],
          ['O', 'X', 'X']], 'O', True),
        ([['O', 'X', 'X'],
          ['X', 'O', 'O'],
          ['O', 'X', 'X']], 'X', False)
    ]
)
def test_won(input, sign, expected_result):
    assert won(input, sign) == expected_result
