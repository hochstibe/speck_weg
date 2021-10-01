# fingertraining
# Stefan Hochuli, 10.09.2021,
# Folder: speck_weg/app File: workout.py
#

from typing import Optional, Union, Dict, Tuple, TYPE_CHECKING

from .. import db
from .message import Message
from .workout_session import WorkoutSession

if TYPE_CHECKING:
    from .workout_exercise import WorkoutExerciseSet
    from ..models import (TrainingExerciseModel, WorkoutExerciseModel,
                          TrainingProgramModel, WorkoutSessionModel)


class Workout:
    def __init__(self, tpr: Union[int, 'TrainingProgramModel'] = None,
                 wse: Union[int, 'WorkoutSessionModel'] = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.workout_session = WorkoutSession(db, tpr, wse)

        # default messages
        self.messages: Dict[str, 'Message'] = dict()

        title = 'Session löschen'
        text = 'Die Session wird geschlossen und gelöscht. ' \
               'Alle gespeicherten Übungen werden ebenfalls gelöscht.'
        self.messages['delete_session'] = Message(title, text, 'question',
                                                  button_accept_name='Löschen')

        # Set the starting position
        # both, the position and the set equals the position in the respective list
        # in the database, the values start with 1
        # --> always add +1 for persisting the position or set in the database
        self.current_pos: int = -1  # position in WorkoutSession.exercises
        self.current_set: int = -1  # position in WorkoutExerciseSet.wex_model_list

    @property
    def current_exercise_set(self) -> Union['WorkoutExerciseSet', None]:
        if self.current_pos in range(len(self.workout_session.exercises)):
            return self.workout_session.exercises[self.current_pos]
        else:
            print('out of range', self.current_pos, len(self.workout_session.exercises))
            return None

    @property
    def current_tex_wex(self) -> Tuple['TrainingExerciseModel', Optional['WorkoutExerciseModel']]:
        if self.current_pos in range(len(self.workout_session.exercises)):
            current_exercise_set = self.workout_session.exercises[self.current_pos]
            tex = current_exercise_set.tex_model
            wex = current_exercise_set.wex_model_list[self.current_set]
            return tex, wex
        else:
            raise ValueError('No current exercise (start or end position)')

    @property
    def start_position(self) -> bool:
        # If it is the start position -> True
        if self.current_pos == -1:
            return True
        else:
            return False

    @property
    def end_position(self) -> bool:
        if self.current_pos == len(self.workout_session.exercises):
            return True
        else:
            return False

    def save(self, comment: str,  # comment is for both: session and exercise
             repetitions: int = None,
             weight: float = None, duration: float = None):
        # all attributes from the widgets are given -> not necessary for the session...
        if self.current_pos == -1 or self.current_pos == len(self.workout_session.exercises):
            # start / stop
            self.workout_session.edit_session(comment)
        else:
            if self.current_exercise_set.wex_model_list[self.current_set]:
                # edit the model
                self.current_exercise_set.edit_exercise(
                    n_set=self.current_set,   # only for accessing the exercise
                    repetitions=repetitions, weight=weight,
                    duration=duration, comment=comment
                )
            else:
                # new model
                # the position equals the sequence in the tpe
                self.current_exercise_set.add_exercise(
                    sequence=self.current_pos + 1, n_set=self.current_set,
                    repetitions=repetitions, weight=weight,
                    duration=duration, comment=comment
                )

    def delete(self):
        if self.current_pos == -1 or self.current_pos == len(self.workout_session.exercises):
            self.workout_session.remove_session()

        else:
            self.current_exercise_set.remove_exercise(self.current_set)

    def delete_message(self) -> bool:
        # Check, if there should be a delete message popped or not
        if self.current_pos == -1 or self.current_pos == len(self.workout_session.exercises):
            # Check, if there are any exercises saved
            if self.workout_session.wex_saved:
                # Session with saved workout exercises -> pop message
                return True
            else:
                # no exercises saved, just delete the session
                return False
        else:
            # Delete exercise -> no message
            return False

    def previous_set(self):
        print('previous exercise or set')
        # minimum position: -1
        self.current_set -= 1
        if self.current_set == -1:
            # previous exercise
            self.current_pos -= 1
            if not self.start_position:
                # Go to last set of the previous exercise
                self.current_set = self.current_exercise_set.tex_model.baseline_sets - 1
        # If it already was on start position -> set -1 for start position
        self.current_pos = max(self.current_pos, -1)
        # If it was on first set of first exercise -> reset to first set
        self.current_set = max(self.current_set, 0)

    def next_set(self):
        print('next set or exercise')
        # maximum position: len(self.workout_session.exercises) = end position

        self.current_set += 1
        if self.end_position:
            # current set = 0 -> previous_set -> -1 -> go to previous exercise
            self.current_set = 0
        if self.start_position or \
                self.current_set == self.current_exercise_set.tex_model.baseline_sets:
            # start -> pos=-1 -> pos=0 goto first exercise
            # any last set of an exercise -> set higher than baseline -> next exercise
            self.current_pos += 1
            self.current_set = 0

    def previous_exercise(self):
        print('previous exercise')
        self.current_pos -= 1
        self.current_set = 0
        self.current_pos = max(self.current_pos, -1)

    def next_exercise(self):
        print('next exercise')
        self.current_pos += 1
        self.current_set = 0

        self.current_pos = min(self.current_pos, len(self.workout_session.exercises))

    def calc_ratio(self, weight: float) -> float:
        return weight / self.current_exercise_set.tex_model.baseline_weight

    def calc_weight(self, ratio: float) -> float:
        return ratio * self.current_exercise_set.tex_model.baseline_weight
