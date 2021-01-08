WITH cte AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY id
            ORDER BY
                last_update DESC
        ) AS row_number
    FROM
        `voltaic-country-280607.Basevn.workflow` wf
)
SELECT
    *
EXCEPT
    (row_number)
FROM
    cte
WHERE
    row_number = 1