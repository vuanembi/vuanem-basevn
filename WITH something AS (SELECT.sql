WITH something AS (SELECT
  wf.id,
  form,
  REPLACE(JSON_EXTRACT(form,
    "$.id"), '"', '') AS form_id,
  REPLACE(JSON_EXTRACT(form,
    "$.name"), '"', '') AS form_name,
  REPLACE(JSON_EXTRACT(form,
    "$.value"), '"', '') AS form_value
FROM
  `voltaic-country-280607.Basevn.basevn_workflow` wf,
  UNNEST(JSON_EXTRACT_ARRAY(form)) AS form)
SELECT * FROm something