# speck_weg
# Stefan Hochuli, 24.09.2021,
# Folder: server/speck_weg_backend File: triggers.py
#

from sqlalchemy import DDL

# Before inserting /updating a training_exercise
# set the attribute baseline_weight
update_baseline_weight_func = DDL("""
CREATE OR REPLACE FUNCTION update_baseline_weight()
RETURNS TRIGGER AS $$
DECLARE
    usr_weight float := NULL;
BEGIN
    IF NEW.tex_usr_id IS NOT NULL THEN
       SELECT usr.weight INTO usr_weight FROM "user" usr WHERE usr.usr_id = NEW.tex_usr_id;
    END IF;
    NEW.baseline_weight := COALESCE(NEW.baseline_custom_weight, usr_weight);
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;
""")
update_baseline_weight_trigger = DDL("""
CREATE TRIGGER update_baseline_weight
    BEFORE INSERT OR UPDATE ON training_exercise
    FOR EACH ROW EXECUTE PROCEDURE update_baseline_weight();
""")

# Before inserting /updating a workout_set
# set the attribute score
update_set_score_func = DDL("""
CREATE OR REPLACE FUNCTION update_set_score()
RETURNS TRIGGER AS $$
DECLARE
    rec record;
    repetition_score float := 1.;
    weight_score float := 1.;
    duration_score float := 1.;
BEGIN
    -- select the corresponding training exercise to the set
    SELECT
        CAST(tex.baseline_repetitions AS FLOAT),
        tex.baseline_weight,
        tex.baseline_duration INTO rec
    FROM workout_exercise wex
    JOIN training_program_exercise tpe ON wex.wex_tpe_id = tpe.tpe_id
    JOIN training_exercise tex ON tpe.tpe_tex_id = tex_id
    WHERE wex.wex_id = NEW.wst_wex_id LIMIT 1;
    -- calculate the scores
    repetition_score := NEW.repetitions / rec.baseline_repetitions;
    IF rec.baseline_weight IS NOT NULL THEN
        weight_score := new.weight / rec.baseline_weight;
    END IF;
    IF rec.baseline_duration IS NOT NULL
        THEN duration_score := NEW.duration / rec.baseline_duration;
    END IF;
    NEW.score := repetition_score * weight_score * duration_score;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;
""")
update_set_score_trigger = DDL("""
CREATE TRIGGER update_set_score
    BEFORE INSERT OR UPDATE ON workout_set
    FOR EACH ROW EXECUTE PROCEDURE update_set_score();
""")

# Before inserting /updating a workout_exercise
# set the attribute score
update_exercise_score_func = DDL("""
CREATE OR REPLACE FUNCTION update_exercise_score()
RETURNS TRIGGER AS $$
DECLARE
    wst_row record;
    -- wst_count integer := 0;
    score float := 0.0;
begin
    -- loop through done sets
    for wst_row in
        SELECT wst.score, tex.baseline_sets
        FROM workout_exercise wex
        JOIN workout_set wst ON wex.wex_id = wst.wst_wex_id
        JOIN training_program_exercise tpe ON wex.wex_tpe_id = tpe.tpe_id
        JOIN training_exercise tex ON tpe.tpe_tex_id = tex.tex_id
        WHERE wex.wex_id = NEW.wex_id
    loop
        -- wst_count := wst_count + 1;
        -- add the scores for the mean of all sets
        score := score + wst_row.score;
        -- score := score * wex_row.score;
    end loop;
    -- total score is sum of scores / number of planned sets
    score := score::float / wst_row.baseline_sets;
    NEW.score := score;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;
""")
update_exercise_score_trigger = DDL("""
CREATE TRIGGER update_exercise_score
    BEFORE INSERT OR UPDATE ON workout_exercise
    FOR EACH ROW EXECUTE PROCEDURE update_exercise_score();
""")

# Before inserting /updating a workout_session
# set the attribute score
# todo: only one select statement (add another join)
# todo: select the count of tpe's for each session
update_session_score_func = DDL("""
CREATE OR REPLACE FUNCTION update_session_score()
RETURNS TRIGGER AS $$
DECLARE
    rec record;
    -- wex_score float;
    -- tex_count integer := 0;
    score float := 0.0;
BEGIN
    NEW."comment" := '';
    -- loop through the planned exercises
    -- calculate the score for if there is a done exercise
    FOR rec IN
        SELECT
            tpe."sequence",
            (select count(tpe.tpe_id) as tpe_count 
             from training_program tpr 
             left join training_program_exercise tpe on tpr.tpr_id = tpe.tpe_tpr_id 
             where tpr.tpr_id = NEW.wse_tpr_id) as tpe_count,
            COALESCE(wex.score, 0.0) AS wex_score
        FROM training_program tpr
        INNER JOIN training_program_exercise tpe ON tpr.tpr_id = tpe.tpe_tpr_id
        INNER JOIN training_exercise tex ON tpe.tpe_tex_id = tex.tex_id
        LEFT JOIN workout_exercise wex ON tpe.tpe_id = wex.wex_tpe_id
        WHERE tpr.tpr_id = NEW.wse_tpr_id
        ORDER BY tpe."sequence"
    LOOP
        -- tex_count := tex_count + 1;
        -- for each planned exercise: select the score (if it was done)
        -- SELECT wex.score 
        --     INTO wex_score
        --     FROM workout_exercise wex
        --     WHERE wex.wex_tpe_id = tpe_row.tpe_id AND wex.wex_wse_id = new.wse_id
        --     LIMIT 1;
        -- add the score
        -- IF wex_score IS NOT NULL THEN
        -- score := score + wex_score;
        -- END IF;
        score := score + rec.wex_score::FLOAT / rec.tpe_count;
        NEW."comment" := NEW."comment" || ' ' || rec."sequence";
        -- IF tpe_row.wex_score IS NOT NULL THEN
        --     score := score + tpe_row.wex_score::FLOAT;
        --     NEW."comment" := NEW."comment" || ' ' || tpe_row.score;
        -- ELSE
        --     NEW."comment" := NEW."comment" || ' skipped tpe ' || tpe_row.tpe_id;
        -- END IF;
    END LOOP;
    -- mean: score per planned exercises
    -- score := score::FLOAT / tex_count;
    NEW.score := score;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;
""")
update_session_score_trigger = DDL("""
CREATE TRIGGER update_session_score
    BEFORE INSERT OR UPDATE ON workout_session
    FOR EACH ROW EXECUTE PROCEDURE update_session_score();
""")

# update training_exercise trigger after changing the user_weight
user_weight_updated_func = DDL("""
CREATE OR REPLACE FUNCTION user_weight_updated()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.weight != NEW.weight THEN
        -- Initialize an irrelevant update statement to activate the other trigger
        UPDATE training_exercise SET tex_usr_id = NEW.usr_id WHERE tex_usr_id = NEW.usr_id;
    END IF;
RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;
""")
user_weight_updated_trigger = DDL("""
CREATE TRIGGER update_user_weight
    AFTER INSERT OR UPDATE ON "user"
    FOR EACH ROW EXECUTE PROCEDURE user_weight_updated();
""")
# update workout_exercise trigger after changing the baseline_weight
baseline_weight_updated_func = DDL("""
CREATE OR REPLACE FUNCTION baseline_weight_updated()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.baseline_weight != NEW.baseline_weight THEN
        -- Initialize an irrelevant update statement to activate the other trigger
        UPDATE workout_set wst SET score = 2
        FROM workout_exercise wex JOIN 
             training_program_exercise tpe ON wex.wex_tpe_id = tpe_id
        WHERE wst.wst_wex_id = wex.wex_id AND tpe.tpe_tex_id = NEW.tex_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;
""")
baseline_weight_updated_trigger = DDL("""
CREATE TRIGGER baseline_weight_updated AFTER INSERT OR UPDATE ON training_exercise
FOR EACH ROW EXECUTE PROCEDURE baseline_weight_updated();
""")
# update workout exercise trigger after changing the set score
set_score_updated_func = DDL("""
CREATE OR REPLACE FUNCTION set_score_updated()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') OR OLD.score <> NEW.score THEN
        -- Initialize an irrelevant update statement to activate the other trigger
        UPDATE workout_exercise SET score = 3 WHERE wex_id = NEW.wst_wex_id;
    END IF;
RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;
""")
set_score_updated_trigger = DDL("""
CREATE TRIGGER set_score_updated AFTER INSERT OR UPDATE ON workout_set
FOR EACH ROW EXECUTE PROCEDURE set_score_updated()
""")
# update workout_session trigger after changing the exercise score
exercise_score_updated_func = DDL("""
CREATE OR REPLACE FUNCTION exercise_score_updated()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') OR OLD.score <> NEW.score THEN
        -- Initialize an irrelevant update statement to activate the other trigger
        UPDATE workout_session SET score = 4 WHERE wse_id = NEW.wex_wse_id;
    END IF;
RETURN NEW;
END;
$$ LANGUAGE PLPGSQL
""")
exercise_score_updated_trigger = DDL("""
CREATE TRIGGER exercise_score_updated AFTER INSERT OR UPDATE ON workout_exercise
FOR EACH ROW EXECUTE PROCEDURE exercise_score_updated();
""")
