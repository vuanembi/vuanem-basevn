SELECT
    wf.id AS workflow_id,
    progression.name,
    progression.start,
    progression.duration,
FROM
    `voltaic-country-280607.Basevn.workflow_core` wf,
    UNNEST(progression) AS progression