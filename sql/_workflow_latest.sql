WITH cte AS (
    SELECT
        id,
        type,
        hid,
        token,
        status,
        state,
        starred,
        name,
        title,
        content,
        color,
        followers,
        since,
        last_update,
        finish_at,
        stage_id,
        stage_export,
        stats,
        user_id,
        username,
        todos,
        creator_id,
        creator_username,
        deadline,
        stage_deadline,
        stage_start,
        workflow_id,
        workflow_export,
        moves,
        acl,
        form,
        on_failed,
        data,
        keyword,
        deadline_by_timesheet,
        first_assignee,
        _batched_at,
        ROW_NUMBER() OVER (
            PARTITION BY id
            ORDER BY
                _batched_at DESC
        ) AS row_number
    FROM
        `voltaic-country-280607.Basevn.workflow`
)
SELECT
    id,
    type,
    hid,
    token,
    status,
    state,
    starred,
    name,
    title,
    content,
    color,
    followers,
    stage_id,
    stage_export,
    stats,
    user_id,
    username,
    todos,
    creator_id,
    creator_username,
    deadline,
    workflow_id,
    workflow_export,
    moves,
    acl,
    form,
    on_failed,
    data,
    keyword,
    deadline_by_timesheet,
    first_assignee,
    IF(UNIX_SECONDS(since) = 0, NULL, since) AS since,
    IF(UNIX_SECONDS(last_update) = 0, NULL, last_update) AS last_update,
    IF(UNIX_SECONDS(finish_at) = 0, NULL, finish_at) AS finish_at,
    IF(
        UNIX_SECONDS(stage_deadline) = 0,
        NULL,
        stage_deadline
    ) AS stage_deadline,
    IF(UNIX_SECONDS(stage_start) = 0, NULL, stage_start) AS stage_start,
    IF(UNIX_SECONDS(_batched_at) = 0, NULL, _batched_at) AS _batched_at,
FROM
    cte
WHERE
    cte.row_number = 1