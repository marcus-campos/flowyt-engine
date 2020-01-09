{
    "id": "2",
    "action": "validation",
    "data": {
        "schema": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        },
        "next_action_success": "3",
        "next_action_fail": "4"
    },
    "next_action": "${pipeline.next_action}"
}
