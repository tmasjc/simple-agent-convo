def replace_keywords(text: str, mapping: dict):
    for key, value in mapping.items():
        text = text.replace(key, value)
    return text

def transform_dialogue(data: list):
    formatted = "\n".join("{role}: {content}".format(**item) for item in data)
    transformed = replace_keywords(formatted, {"assistant": "you", "user": "friend"})
    return transformed
