SELECT
    wf.id AS workflow_id,
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
    `voltaic-country-280607.Basevn.workflow_core` wf,
    UNNEST(moves) AS moves