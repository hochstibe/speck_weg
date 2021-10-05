# fingertraining
# Stefan Hochuli, 31.08.2021,
# Folder:  File: add_data.py
#

from server.speck_weg_backend import create_app, models
from server.speck_weg_backend.extensions import db


if __name__ == '__main__':

    # engine.echo = True
    # models.Base.metadata.drop_all(engine)
    # models.Base.metadata.create_all(bind=engine)
    # Session = get_db_session(echo=True, drop_all=True)
    app = create_app()
    with app.app_context():
        print('connecting to the db')
        db.metadata.drop_all(db.engine)
        db.metadata.create_all(db.engine)

        print('creating all models')
        usr1 = models.UserModel(
            first_name='Stefan', last_name='Hochuli',
            email='test@example.com', password='password', weight=72)
        tth1 = models.TrainingThemeModel(user=usr1, name='Beastmaker 1000', sequence=1)
        tpr1 = models.TrainingProgramModel(name='5a', sequence=2, training_theme=tth1)
        tpr2 = models.TrainingProgramModel(name='5b', sequence=3, training_theme=tth1)
        tpr3 = models.TrainingProgramModel(name='5c', sequence=4, training_theme=tth1)
        tex1 = models.TrainingExerciseModel(name='Jugs', baseline_sets=1,
                                            baseline_repetitions=7, baseline_duration=7, user=usr1)
        tex2 = models.TrainingExerciseModel(name='Open 3 tief', baseline_sets=1,
                                            baseline_repetitions=7, baseline_duration=7, user=usr1)
        tex3 = models.TrainingExerciseModel(name='Open 4 tief', baseline_sets=1,
                                            baseline_repetitions=7, baseline_duration=7, user=usr1)
        tex4 = models.TrainingExerciseModel(name='Half Crimp tief', description='Vorderstes Glied',
                                            baseline_sets=1, baseline_repetitions=7,
                                            baseline_duration=7, user=usr1)
        tex5 = models.TrainingExerciseModel(name='Sloper 20°', baseline_sets=1,
                                            baseline_repetitions=7, baseline_duration=7, user=usr1)
        tex6 = models.TrainingExerciseModel(name='Open 3 mittel', baseline_sets=1,
                                            baseline_repetitions=7, baseline_duration=7, user=usr1)
        tex7 = models.TrainingExerciseModel(
            name='Open 2 tief (Zeig-/Mittelfinger)',
            description='Zeige- / Mittelfinger oder Mittel- / Ringfinger',
            baseline_sets=1, baseline_repetitions=7, baseline_duration=7, user=usr1)
        tex8 = models.TrainingExerciseModel(name='Open 4 halb-tief ', description='Vorderstes Glied',
                                            baseline_sets=1, baseline_repetitions=7,
                                            baseline_duration=7, user=usr1)
        tex9 = models.TrainingExerciseModel(name='Open 4 mittel', baseline_sets=1,
                                            baseline_repetitions=7, baseline_duration=7, user=usr1)

        # 5a
        tpe1 = models.TrainingProgramExerciseModel(training_program=tpr1, training_exercise=tex1,
                                                   sequence=1)
        tpe2 = models.TrainingProgramExerciseModel(training_program=tpr1, training_exercise=tex1,
                                                   sequence=2)
        tpe3 = models.TrainingProgramExerciseModel(training_program=tpr1, training_exercise=tex2,
                                                   sequence=3)
        tpe4 = models.TrainingProgramExerciseModel(training_program=tpr1, training_exercise=tex2,
                                                   sequence=4)
        tpe5 = models.TrainingProgramExerciseModel(training_program=tpr1, training_exercise=tex3,
                                                   sequence=5)
        tpe6 = models.TrainingProgramExerciseModel(training_program=tpr1, training_exercise=tex3,
                                                   sequence=6)
        # 5b
        tpe7 = models.TrainingProgramExerciseModel(training_program=tpr2, training_exercise=tex4,
                                                   sequence=1)
        tpe8 = models.TrainingProgramExerciseModel(training_program=tpr2, training_exercise=tex5,
                                                   sequence=2)
        tpe9 = models.TrainingProgramExerciseModel(training_program=tpr2, training_exercise=tex4,
                                                   sequence=3)
        tpe10 = models.TrainingProgramExerciseModel(training_program=tpr2, training_exercise=tex6,
                                                    sequence=4)
        tpe11 = models.TrainingProgramExerciseModel(training_program=tpr2, training_exercise=tex7,
                                                    sequence=5)
        tpe12 = models.TrainingProgramExerciseModel(training_program=tpr2, training_exercise=tex8,
                                                    sequence=6)
        # 5c
        tpe13 = models.TrainingProgramExerciseModel(training_program=tpr3, training_exercise=tex4,
                                                    sequence=1)
        tpe14 = models.TrainingProgramExerciseModel(training_program=tpr3, training_exercise=tex6,
                                                    sequence=2)
        tpe15 = models.TrainingProgramExerciseModel(training_program=tpr3, training_exercise=tex9,
                                                    sequence=3)
        tpe16 = models.TrainingProgramExerciseModel(training_program=tpr3, training_exercise=tex7,
                                                    sequence=4)
        tpe17 = models.TrainingProgramExerciseModel(training_program=tpr3, training_exercise=tex5,
                                                    sequence=5)
        tpe18 = models.TrainingProgramExerciseModel(training_program=tpr3, training_exercise=tex9,
                                                    sequence=6)

        # Warmup
        tpr4 = models.TrainingProgramModel(name='Warmup Schultern / Arme', training_theme=tth1,
                                           sequence=1)
        tex10 = models.TrainingExerciseModel(name='Terraband diagonal',
                                             baseline_sets=3, baseline_repetitions=10)
        tex11 = models.TrainingExerciseModel(name='Terraband Schulter 1/4 Drehung',
                                             baseline_sets=3, baseline_repetitions=10)
        tex12 = models.TrainingExerciseModel(name='Terraband Ellbogen 1/4 Drehung',
                                             baseline_sets=3, baseline_repetitions=10)
        tex13 = models.TrainingExerciseModel(name='Liegestützen', baseline_sets=3,
                                             baseline_repetitions=10)
        tex14 = models.TrainingExerciseModel(name='Schulter anspannen 2 Arme', description='3s halten',
                                             baseline_sets=3, baseline_repetitions=10, user=usr1)
        tex15 = models.TrainingExerciseModel(name='Schulter anspannen 1 Arm', description='3s halten',
                                             baseline_sets=3, baseline_repetitions=5, user=usr1)
        tex16 = models.TrainingExerciseModel(name='Klimmzug',
                                             baseline_sets=3, baseline_repetitions=5, user=usr1)
        tpe19 = models.TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex10,
                                                    sequence=1)
        tpe20 = models.TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex11,
                                                    sequence=2)
        tpe21 = models.TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex12,
                                                    sequence=3)
        tpe22 = models.TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex13,
                                                    sequence=4)
        tpe23 = models.TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex14,
                                                    sequence=5)
        tpe24 = models.TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex15,
                                                    sequence=6)
        tpe25 = models.TrainingProgramExerciseModel(training_program=tpr4, training_exercise=tex16,
                                                    sequence=7)

        tth101 = models.TrainingThemeModel(user=usr1, name='Test', sequence=2)
        tpr101 = models.TrainingProgramModel(name='Test', training_theme=tth101, sequence=1)
        tex101 = models.TrainingExerciseModel(name='weight', baseline_sets=2,
                                              baseline_repetitions=3, baseline_custom_weight=3.)
        tex102 = models.TrainingExerciseModel(name='body_weight duration',
                                              baseline_sets=3, baseline_repetitions=3, user=usr1,
                                              baseline_duration=11)
        tex103 = models.TrainingExerciseModel(name='repetitions',
                                              baseline_sets=3, baseline_repetitions=2)
        tex104 = models.TrainingExerciseModel(name='skipped set',
                                              baseline_sets=3, baseline_repetitions=2)
        tex105 = models.TrainingExerciseModel(name='skipped tex',
                                              baseline_sets=1, baseline_repetitions=1)
        tpe101 = models.TrainingProgramExerciseModel(training_program=tpr101, training_exercise=tex101,
                                                     sequence=1)
        tpe102 = models.TrainingProgramExerciseModel(training_program=tpr101, training_exercise=tex102,
                                                     sequence=2)
        tpe103 = models.TrainingProgramExerciseModel(training_program=tpr101, training_exercise=tex103,
                                                     sequence=3)
        tpe104 = models.TrainingProgramExerciseModel(training_program=tpr101, training_exercise=tex104,
                                                     sequence=4)
        tpe105 = models.TrainingProgramExerciseModel(training_program=tpr101, training_exercise=tex105,
                                                     sequence=5)

        # workout
        wse1 = models.WorkoutSessionModel(training_program=tpr101)
        wex1 = models.WorkoutExerciseModel(workout_session=wse1, training_exercise=tpe101, sequence=1)
        wst1 = models.WorkoutSetModel(workout_exercise=wex1, set=1, repetitions=3, weight=1.1)
        wst2 = models.WorkoutSetModel(workout_exercise=wex1, set=2, repetitions=5, weight=3)
        wex2 = models.WorkoutExerciseModel(workout_session=wse1, training_exercise=tpe102, sequence=2)
        wst3 = models.WorkoutSetModel(workout_exercise=wex2, set=1, repetitions=3,
                                      weight=72, duration=19)
        wst4 = models.WorkoutSetModel(workout_exercise=wex2, set=2, repetitions=3,
                                      weight=32, duration=11)
        wst5 = models.WorkoutSetModel(workout_exercise=wex2, set=3, repetitions=3,
                                      weight=78, duration=22)
        wex3 = models.WorkoutExerciseModel(workout_session=wse1, training_exercise=tpe103, sequence=3)
        wst6 = models.WorkoutSetModel(workout_exercise=wex3, set=1, repetitions=2)
        wst7 = models.WorkoutSetModel(workout_exercise=wex3, set=2, repetitions=3)
        wex4 = models.WorkoutExerciseModel(workout_session=wse1, training_exercise=tpe104, sequence=4)
        wst8 = models.WorkoutSetModel(workout_exercise=wex4, set=1, repetitions=2)
        # a realistic 5b session
        wse2 = models.WorkoutSessionModel(training_program=tpr2)
        wex11 = models.WorkoutExerciseModel(workout_session=wse2, training_exercise=tpe7, sequence=1)
        wst11 = models.WorkoutSetModel(workout_exercise=wex11, set=1, repetitions=7,
                                       weight=72*0.8, duration=7)
        wex12 = models.WorkoutExerciseModel(workout_session=wse2, training_exercise=tpe8, sequence=2)
        wst12 = models.WorkoutSetModel(workout_exercise=wex12, set=1, repetitions=7,
                                       weight=72, duration=7)
        wex13 = models.WorkoutExerciseModel(workout_session=wse2, training_exercise=tpe9, sequence=3)
        wst13 = models.WorkoutSetModel(workout_exercise=wex13, set=1, repetitions=7,
                                       weight=72*0.8, duration=7)
        wex14 = models.WorkoutExerciseModel(workout_session=wse2, training_exercise=tpe10, sequence=4)
        wst14 = models.WorkoutSetModel(workout_exercise=wex14, set=1, repetitions=7,
                                       weight=72, duration=7)
        wex15 = models.WorkoutExerciseModel(workout_session=wse2, training_exercise=tpe11, sequence=5)
        wst15 = models.WorkoutSetModel(workout_exercise=wex15, set=1, repetitions=7,
                                       weight=72*0.8, duration=7)
        wex16 = models.WorkoutExerciseModel(workout_session=wse2, training_exercise=tpe12, sequence=6)
        wst16 = models.WorkoutSetModel(workout_exercise=wex16, set=1, repetitions=7,
                                       weight=72*0.8, duration=7)

        # with Session.begin() as session:
        #     print(type(session), session)
        # commits and closes the session
        # alternative: with SessionLocal() as session: ..... session.commit() end with
        print('persisting all models')
        db.session.add_all([usr1, tth1, tth101])
        db.session.commit()

        print('All models persisted in the database.')
