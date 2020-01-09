{
    "id": "2",
    "action": "flow_var",
    "data": {
        "flow_id": "${function.util.generate_uuid()}",
        "flow_slugged": "${function.util.slugify(request.data.flow_name)}"
    },
    "next_action": "3"
}
