SELECT
    wf.id AS workflow_id,
    form.id,
    form.name,
    form.value,
    form.type,
    form.placeholder
FROM
    `voltaic-country-280607.Basevn.workflow_core` wf,
    UNNEST(form) AS form