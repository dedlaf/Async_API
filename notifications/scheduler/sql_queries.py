class SQLQueries:
    GET_EVENT = "SELECT id, template_id, content_id, users, timestamp FROM notify.event WHERE timestamp <= %s"
    GET_TEMPLATE = "SELECT template FROM notify.template WHERE template.id = %s"
    GET_CONTENT = "SELECT words::json FROM notify.content WHERE content.id = %s"
    DELETE_EVENT = "DELETE FROM notify.event WHERE id = %s"


