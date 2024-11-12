class ContentQueries:
    SELECT_ALL = "SELECT id, words, created, modified " "FROM notify.content"
    SELECT_BY_ID = (
        "SELECT id, words, created, modified " "FROM notify.content WHERE id = %s"
    )
    CREATE = (
        "INSERT INTO notify.content (id, words, created, modified) "
        "VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
    )
    UPDATE = (
        "UPDATE notify.content "
        "SET words = %s, modified = CURRENT_TIMESTAMP WHERE id = %s"
    )
    DELETE = "DELETE FROM notify.content WHERE id = %s"


class TemplateQueries:
    SELECT_ALL = (
        "SELECT id, template_name, template, created, modified " "FROM notify.template"
    )
    SELECT_BY_ID = (
        "SELECT id, template_name, template, created, modified "
        "FROM notify.template WHERE id = %s"
    )
    CREATE = (
        "INSERT INTO notify.template (id, template_name, template, created, modified) "
        "VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
    )
    UPDATE = (
        "UPDATE notify.template "
        "SET template_name = %s, template = %s, modified = CURRENT_TIMESTAMP "
        "WHERE id = %s"
    )
    DELETE = "DELETE FROM notify.template WHERE id = %s"


class EventQueries:
    SELECT_ALL = (
        "SELECT id, template_id, content_id, users, timestamp, created, modified "
        "FROM notify.event"
    )
    SELECT_BY_ID = (
        "SELECT id, template_id, content_id, users, timestamp, created, modified "
        "FROM notify.event WHERE id = %s"
    )
    CREATE = (
        "INSERT INTO notify.event (id, template_id, content_id, users, timestamp, created, modified) "
        "VALUES (%s, %s, %s, %s::uuid[], %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
    )
    UPDATE = (
        "UPDATE notify.event "
        "SET template_id = %s, content_id = %s, users = %s::uuid[], timestamp = %s, "
        "modified = CURRENT_TIMESTAMP WHERE id = %s"
    )
    DELETE = "DELETE FROM notify.event WHERE id = %s"
