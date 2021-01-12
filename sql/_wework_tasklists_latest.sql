WITH cte AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY id
            ORDER BY
                _batched_at DESC
        ) AS row_number
    FROM
        `voltaic-country-280607.Basevn.wework_tasklists`
)
SELECT
    *
EXCEPT
(row_number)
FROM
    cte
WHERE
    cte.row_number = 1