SYSTEM_CHARACTER = (
    "You are a AI wizard. You speak elegantly and gracefully. Full of wisdom and charm."
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_memory",
            "description": "Recall content of previous conversation from memory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event": {
                        "type": "string",
                        "description": "Event or topic to recall, e.g. talking about politics, asking someone's status.",
                    },
                    "target": {"type": "string", "description": "person of interest"},
                },
                "required": ["event"],
            },
        },
    }
]
