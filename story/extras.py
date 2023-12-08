SYSTEM_CHARACTER = (
    "You are a AI wizard. You speak elegantly and gracefully. Often funny and concise. You never mention the fact that you are an AI. You are not apologetic. When in doubt, you say 'huh?'"
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "recall_event",
            "description": "Recall important event from previous conversation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event": {
                        "type": "string",
                        "description": "Event or topic to recall, e.g. politics, relationships, meetings.",
                    },
                },
                "required": ["event"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recall_someone",
            "description": "Recall content of conversation with someone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "person": {
                        "type": "string",
                        "description": "Person of interest",
                    },
                },
                "required": ["person"],
            },
        },
    },
]

wizard_greetings = [
    "Greetings from the realms beyond!",
    "Well met by moonlight and starshine!",
    "Salutations from the whispers of the ancient winds!",
    "Hail and well met, traveler of the mortal coil!",
    "By the alchemy of old, I bid you welcome!",
    "From the depths of the mystic ether, I greet thee!",
    "May the wisdom of the ages be upon our meeting!",
    "Under the watchful eye of the arcane, our paths cross!",
    "Blessings of the enchanted realms upon you!",
    "In the light of the aurora mystica, greetings!",
]
