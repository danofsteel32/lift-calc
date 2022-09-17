import pytest

from lift_calc import novice


@pytest.fixture(scope="session")
def transition_weight() -> int:
    return novice.TWENTY_FIVE_TO_FORTY_FIVE


def test_exercise_start_weight_below_transition_weight(transition_weight: int):
    exercise = novice.Exercise("test", 3, transition_weight - 5)
    exercise.set_start_weight()
    assert exercise.start_weight == 25


def test_exercise_start_weight_above_transition_weight(transition_weight: int):
    exercise = novice.Exercise("test", 3, transition_weight + 5)
    exercise.set_start_weight()
    assert exercise.start_weight == 45


def test_exercise_start_weight_manually_set():
    exercise = novice.Exercise("test", 3, 105, start_weight=65)
    exercise.set_start_weight()
    assert exercise.start_weight == 65


def test_exercise_get_sets():
    pass
