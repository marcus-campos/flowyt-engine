{
    "id": "2",
    "action": "request",
    "data": {
        "url": "${env.arango_db}/document?collection=workspaces",
        "method": "get",
        "headers": {},
        "data": {},
        "next_action_success": "3",
        "next_action_fail": "3"
    },
    "next_action": "${pipeline.next_action}"
}
