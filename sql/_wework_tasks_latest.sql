WITH cte AS (
    SELECT
        id,
        gid,
        hid,
        token,
        parent_id,
        name,
        display_name,
        content,
        content_short,
        link,
        user_id,
        username,
        metatype,
        avatar,
        cover,
        creator_id,
        creator_username,
        has_deadline,
        deadline,
        deadline_has_time,
        start_time,
        stime,
        etime,
        overdue,
        urgent,
        important,
        started,
        completed_time,
        starred,
        complete,
        keywords,
        data,
        score,
        tags,
        status,
        review,
        result,
        owners,
        followers,
        since,
        last_update,
        tasklist_id,
        project_id,
        milestone_id,
        stats,
        real_order,
        ns,
        __compute,
        duration,
        logged_duration,
        _batched_at,
        ROW_NUMBER() OVER (
            PARTITION BY id
            ORDER BY
                _batched_at DESC
        ) AS row_number
    FROM
        `voltaic-country-280607.Basevn.wework_tasks`
)
SELECT
    id,
    gid,
    hid,
    token,
    parent_id,
    name,
    display_name,
    content,
    content_short,
    link,
    user_id,
    username,
    metatype,
    avatar,
    cover,
    creator_id,
    creator_username,
    has_deadline,
    deadline_has_time,
    overdue,
    urgent,
    important,
    started,
    starred,
    complete,
    keywords,
    data,
    score,
    tags,
    status,
    review,
    result,
    owners,
    followers,
    since,
    last_update,
    tasklist_id,
    project_id,
    milestone_id,
    stats,
    real_order,
    ns,
    __compute,
    duration,
    logged_duration,
    IF(UNIX_SECONDS(deadline) = 0, NULL, deadline) AS deadline,
    IF(UNIX_SECONDS(start_time) = 0, NULL, start_time) AS start_time,
    IF(UNIX_SECONDS(stime) = 0, NULL, stime) AS stime,
    IF(UNIX_SECONDS(etime) = 0, NULL, etime) AS etime,
    IF(
        UNIX_SECONDS(completed_time) = 0,
        NULL,
        completed_time
    ) AS completed_time,
    IF(UNIX_SECONDS(_batched_at) = 0, NULL, _batched_at) AS _batched_at,
FROM
    cte
WHERE
    cte.row_number = 1