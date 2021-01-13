WITH cte AS (
    SELECT
        id,
        hid,
        path,
        metatype,
        privacy,
        token,
        name,
        content,
        category,
        color,
        owners,
        followers,
        stime,
        etime,
        since,
        last_update,
        status,
        status_obj,
        stage,
        is_demo,
        managed,
        data,
        bg,
        stats,
        base,
        acl,
        review_enabled,
        external,
        keywords,
        cached_tasklists,
        template,
        options,
        opt_acl,
        opt_task_acl,
        task_duration,
        percent_completion,
        deadline_has_time,
        dept_id,
        incoming_webhook,
        icon,
        _batched_at,
        ROW_NUMBER() OVER (
            PARTITION BY id
            ORDER BY
                _batched_at DESC
        ) AS row_number
    FROM
        `voltaic-country-280607.Basevn.wework_projects`
)
SELECT
    id,
    hid,
    path,
    metatype,
    privacy,
    token,
    name,
    content,
    category,
    color,
    owners,
    followers,
    status,
    status_obj,
    stage,
    is_demo,
    managed,
    data,
    bg,
    stats,
    base,
    acl,
    review_enabled,
    external,
    keywords,
    cached_tasklists,
    template,
    options,
    opt_acl,
    opt_task_acl,
    task_duration,
    percent_completion,
    deadline_has_time,
    dept_id,
    incoming_webhook,
    icon,
    IF(UNIX_SECONDS(stime) = 0, NULL, stime) AS stime,
    IF(UNIX_SECONDS(etime) = 0, NULL, etime) AS etime,
    IF(UNIX_SECONDS(since) = 0, NULL, since) AS since,
    IF(UNIX_SECONDS(last_update) = 0, NULL, last_update) AS last_update,
    IF(UNIX_SECONDS(_batched_at) = 0, NULL, _batched_at) AS _batched_at,
FROM
    cte
WHERE
    cte.row_number = 1