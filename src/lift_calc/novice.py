"""novice.py
This module contains everything needed to create novice level linear
progression workouts like those found in Starting Strength.
"""
import itertools
from dataclasses import dataclass
from datetime import date as Date
from datetime import timedelta
from typing import Dict, Generator, List

# Work set weight where first warmup sets go from 25 -> 45
TWENTY_FIVE_TO_FORTY_FIVE = 95


def round_weight(weight: int | float, base: int = 5) -> int:
    """
    Round a weight to a certain plate increment.
    """
    return int(base * round(float(weight) / base))


@dataclass(slots=True, frozen=True)
class LiftSet:
    sets: int
    reps: int
    weight: int

    def __str__(self) -> str:
        return f"{self.sets}x{self.reps}x{self.weight:<3}"


@dataclass(slots=True)
class Exercise:
    name: str
    warmup_sets: int
    work_weight: int
    work_sets: int = 3
    work_reps: int = 5
    increment_size: int = 5
    start_weight: int = 45

    def set_start_weight(self):
        if self.start_weight > 45:
            return
        if self.work_weight >= TWENTY_FIVE_TO_FORTY_FIVE:
            self.start_weight = 45
        else:
            self.start_weight = 25

    def get_sets(self) -> List[LiftSet]:
        """Returns a list of LiftSet"""

        self.set_start_weight()
        initial_sets = LiftSet(sets=2, reps=5, weight=self.start_weight)
        forty_percent = round_weight(self.work_weight * 0.4)

        if self.warmup_sets == 3:
            sets = [
                initial_sets,
                LiftSet(
                    sets=1, reps=5, weight=max(forty_percent, self.start_weight + 10)
                ),
                LiftSet(sets=1, reps=3, weight=round_weight(self.work_weight * 0.7)),
                LiftSet(sets=1, reps=2, weight=round_weight(self.work_weight * 0.9)),
            ]
        elif self.warmup_sets == 4:
            sets = [
                initial_sets,
                LiftSet(
                    sets=1, reps=5, weight=max(forty_percent, self.start_weight + 10)
                ),
                LiftSet(sets=1, reps=4, weight=round_weight(self.work_weight * 0.6)),
                LiftSet(sets=1, reps=3, weight=round_weight(self.work_weight * 0.8)),
                LiftSet(sets=1, reps=2, weight=round_weight(self.work_weight * 0.9)),
            ]
        else:
            raise ValueError("warmup_sets must be in {3,4}")

        work_sets = LiftSet(
            sets=self.work_sets, reps=self.work_reps, weight=self.work_weight
        )
        sets.append(work_sets)
        return sets

    def increment(self):
        self.work_weight += self.increment_size

    def __str__(self) -> str:
        lifts = " ".join(str(s) for s in self.get_sets())
        return f"{self.name:>10}: {lifts}"


@dataclass(slots=True)
class Workout:
    week: int
    name: str
    date: Date
    exercises: List[Exercise]

    def increment(self):
        for e in self.exercises:
            e.increment()

    def __str__(self) -> str:
        ex = "\n".join(str(e) for e in self.exercises)
        return f"Week {self.week} {self.date} Workout {self.name}\n{ex}"


def workout_iter(
    date: Date, weeks: int, exercises: Dict[str, List[Exercise]]
) -> Generator[Workout, None, None]:
    w_keys = itertools.cycle(["A", "B"])
    for week_num in range(1, weeks + 1):
        for n in [0, 2, 4]:
            w_key = next(w_keys)
            _date = date + timedelta(days=n)
            _exercises = exercises[w_key]
            yield Workout(week_num, w_key, _date, exercises[w_key])
            for e in _exercises:
                e.increment()
        date = date + timedelta(weeks=1)
