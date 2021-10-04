# speck_weg
# Stefan Hochuli, 24.09.2021,
# Folder: server/speck_weg_backend File: triggers.py
#

from sqlalchemy import DDL

# Random id user
random_id_user_trigger = DDL("""
CREATE TRIGGER random_id_user
   BEFORE INSERT OR UPDATE ON "user"
   FOR EACH ROW EXECUTE PROCEDURE random_id_func();
""")
# Random id training_theme
random_id_training_theme_trigger = DDL("""
CREATE TRIGGER random_id_training_theme
   BEFORE INSERT OR UPDATE ON training_theme
   FOR EACH ROW EXECUTE PROCEDURE random_id_func();
""")
# Random id training_program
random_id_training_program_trigger = DDL("""
CREATE TRIGGER random_id_training_program
   BEFORE INSERT OR UPDATE ON training_program
   FOR EACH ROW EXECUTE PROCEDURE random_id_func();
""")
# Random id training_program_exercise
random_id_training_program_exercise_trigger = DDL("""
CREATE TRIGGER random_id_training_program_exercise
   BEFORE INSERT OR UPDATE ON training_program_exercise
   FOR EACH ROW EXECUTE PROCEDURE random_id_func();
""")
# Random id training_exercise
random_id_training_exercise_trigger = DDL("""
CREATE TRIGGER random_id_training_exercise
   BEFORE INSERT OR UPDATE ON training_exercise
   FOR EACH ROW EXECUTE PROCEDURE random_id_func();
""")
# Random id workout_session
random_id_workout_session_trigger = DDL("""
CREATE TRIGGER random_id_workout_session
   BEFORE INSERT OR UPDATE ON workout_session
   FOR EACH ROW EXECUTE PROCEDURE random_id_func();
""")
# Random id workout_exercise
random_id_workout_exercise_trigger = DDL("""
CREATE TRIGGER random_id_workout_exercise
   BEFORE INSERT OR UPDATE ON workout_exercise
   FOR EACH ROW EXECUTE PROCEDURE random_id_func();
""")
# Random id workout_set
random_id_workout_set_trigger = DDL("""
CREATE TRIGGER random_id_workout_set
   BEFORE INSERT OR UPDATE ON workout_set
   FOR EACH ROW EXECUTE PROCEDURE random_id_func();
""")


# Before inserting /updating a training_exercise
# set the attribute baseline_weight
update_baseline_weight_trigger = DDL("""
CREATE TRIGGER update_baseline_weight
    BEFORE INSERT OR UPDATE ON training_exercise
    FOR EACH ROW EXECUTE PROCEDURE update_baseline_weight();
""")

# Before inserting /updating a workout_set
# set the attribute score
update_set_score_trigger = DDL("""
CREATE TRIGGER update_set_score
    BEFORE INSERT OR UPDATE ON workout_set
    FOR EACH ROW EXECUTE PROCEDURE update_set_score();
""")

# Before inserting /updating a workout_exercise
# set the attribute score
update_exercise_score_trigger = DDL("""
CREATE TRIGGER update_exercise_score
    BEFORE INSERT OR UPDATE ON workout_exercise
    FOR EACH ROW EXECUTE PROCEDURE update_exercise_score();
""")

# Before inserting /updating a workout_session
# set the attribute score
update_session_score_trigger = DDL("""
CREATE TRIGGER update_session_score
    BEFORE INSERT OR UPDATE ON workout_session
    FOR EACH ROW EXECUTE PROCEDURE update_session_score();
""")

# update training_exercise trigger after changing the user_weight
user_weight_updated_trigger = DDL("""
CREATE TRIGGER update_user_weight
    AFTER INSERT OR UPDATE ON "user"
    FOR EACH ROW EXECUTE PROCEDURE user_weight_updated();
""")
# update workout_exercise trigger after changing the baseline_weight
baseline_weight_updated_trigger = DDL("""
CREATE TRIGGER baseline_weight_updated
    AFTER INSERT OR UPDATE ON training_exercise
    FOR EACH ROW EXECUTE PROCEDURE baseline_weight_updated();
""")
# update workout exercise trigger after changing the set score
set_score_updated_trigger = DDL("""
CREATE TRIGGER set_score_updated
    AFTER INSERT OR UPDATE ON workout_set
    FOR EACH ROW EXECUTE PROCEDURE set_score_updated()
""")
# update workout_session trigger after changing the exercise score
exercise_score_updated_trigger = DDL("""
CREATE TRIGGER exercise_score_updated
    AFTER INSERT OR UPDATE ON workout_exercise
    FOR EACH ROW EXECUTE PROCEDURE exercise_score_updated();
""")
