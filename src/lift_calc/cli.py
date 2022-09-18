import sys
from datetime import date as Date
from datetime import datetime

import click

from . import __version__
from .novice import Exercise, workout_iter


@click.command()
@click.option(
    "--rep-scheme",
    type=click.Choice(("3x5", "5x5", "5x3")),
    default=("3x5"),
    help="Defaults to 3x5",
)
@click.option(
    "--weeks", default=4, type=int, help="Number of weeks to plan; Defaults to 4"
)
@click.option(
    "--start-date",
    default=str(Date.today()),
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Start date of the program. Defaults to today",
)
@click.option(
    "--warmup-sets",
    default=3,
    type=int,
    help="Number of warmup sets [3|4]; Defaults to 3",
)
@click.option("--squat", required=True, type=int, help="Initial squat work weight")
@click.option("--press", required=True, type=int, help="Initial press work weight")
@click.option("--bench", required=True, type=int, help="Initial bench work weight")
@click.option(
    "--deadlift", required=True, type=int, help="Initial deadlift work weight"
)
@click.option(
    "--powerclean",
    required=True,
    type=int,
    help="Initial powerclean work weight",
)
@click.version_option(__version__)
def run(
    rep_scheme: str,
    start_date: datetime,
    weeks: int,
    warmup_sets: int,
    squat: int,
    bench: int,
    press: int,
    deadlift: int,
    powerclean: int,
):
    if warmup_sets not in {3, 4}:
        print("Warmup sets must be 3 or 4. Don't over or under do it !")
        sys.exit(1)

    sets, reps = [int(num) for num in rep_scheme.split("x")]

    _squat = Exercise(
        "Squat", warmup_sets, work_weight=squat, work_sets=sets, work_reps=reps
    )
    _bench = Exercise(
        "Bench", warmup_sets, work_weight=bench, work_sets=sets, work_reps=reps
    )
    _press = Exercise(
        "Press", warmup_sets, work_weight=press, work_sets=sets, work_reps=reps
    )
    _dl = Exercise(
        "Deadlift",
        warmup_sets,
        work_weight=deadlift,
        work_reps=reps,
        work_sets=1,
        increment_size=10,
        start_weight=65,
    )
    _pc = Exercise(
        "Powerclean",
        warmup_sets,
        work_weight=powerclean,
        work_sets=5,
        work_reps=3,
        start_weight=65,
    )

    # TODO: if deadlift is light ask user if they want to deadlift 3x week first week
    exercises = {
        "A": [_squat, _bench, _dl],
        "B": [_squat, _press, _pc],
    }

    for workout in workout_iter(start_date.date(), weeks, exercises):
        print(workout)
        print()


if __name__ == "__main__":
    run()
