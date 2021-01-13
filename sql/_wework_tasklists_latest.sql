WITH cte AS (
    SELECT
        id,
        hid,
        token,
        name,
        content,
        type,
        privacy,
        ns_id,
        ns_export,
        complete,
        percent,
        stats,
        link,
        `order`,
        `data`,
        since,
        has_deadline,
        deadline,
        stime,
        etime,
        review,
        cs,
        _batched_at,
        ROW_NUMBER() OVER (
            PARTITION BY id
            ORDER BY
                _batched_at DESC
        ) AS row_number
    FROM
        `voltaic-country-280607.Basevn.wework_tasklists`
)
SELECT
    id,
    hid,
    token,
    name,
    content,
    type,
    privacy,
    ns_id,
    ns_export,
    complete,
    percent,
    stats,
    link,
    `order`,
    `data`,
    has_deadline,
    deadline,
    review,
    cs,
    IF(UNIX_SECONDS(since) = 0, NULL, since) AS since,
    IF(UNIX_SECONDS(stime) = 0, NULL, stime) AS stime,
    IF(UNIX_SECONDS(etime) = 0, NULL, etime) AS etime,
    IF(UNIX_SECONDS(_batched_at) = 0, NULL, _batched_at) AS _batched_at,
FROM
    cte
WHERE
    cte.row_number = 1