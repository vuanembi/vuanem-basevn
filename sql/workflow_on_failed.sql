SELECT
    wf.id AS workflow_id,
    on_failed.stage_id,
    on_failed.failed_reason_id,
    on_failed.failed_name,
    on_failed.note,
    on_failed.since,
FROM
    `voltaic-country-280607.Basevn.workflow` wf,
    UNNEST(on_failed) AS on_failed