SELECT
    moves.id,
    moves.user_id,
    moves.mover_id,
    moves.job_id,
    moves.stage_id,
    moves.stage_start,
    moves.stage_deadline,
    moves.from_stage_id,
    moves.duration,
    moves.past,
    moves.stage_end
FROM
    `voltaic-country-280607.Basevn._workflow_latest` wf,
    UNNEST(moves) AS moves