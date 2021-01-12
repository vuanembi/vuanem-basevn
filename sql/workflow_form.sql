SELECT
    wf.id AS job_id,
    form.id,
    form.name,
    form.value,
    form.type,
    form.placeholder
FROM
    `voltaic-country-280607.Basevn._workflow_latest` wf,
    UNNEST(form) AS form