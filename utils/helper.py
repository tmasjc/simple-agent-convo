def replace_keywords(text: str, mapping: dict):
    """
    Replace keywords in a string based on a provided mapping.

    Parameters:
    text (str): The input text where keywords need to be replaced.
    mapping (dict): A dictionary where each key is a keyword to be replaced in the text,
                    and the associated value is the string to replace it with.

    Returns:
    str: The modified text with all instances of the keys in the mapping replaced by their corresponding values.

    Example:
    >>> replace_keywords("Hello, world!", {"world": "universe"})
    'Hello, universe!'
    """
    for key, value in mapping.items():
        text = text.replace(key, value)
    return text


def transform_dialogue(data: list) -> str:
    """
    Transforms a list of dialogue data into a formatted string where specific keywords are replaced.

    Parameters:
    data (list): A list of dictionaries, where each dictionary should have a 'role' and 'content' key.
                 Example: [{'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hi there!'}]

    Returns:
    str: A formatted string with the dialogue. Each dialogue entry is on a new line in the format "role: content".
         Specific keywords in the content are replaced based on predefined rules (e.g., 'assistant' with 'you',
         'user' with 'friend').

    Example:
    >>> transform_dialogue([{'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'How can I help?'}])
    'user: Hello\nassistant: How can I help?'

    Note:
    The function assumes the presence of another function `replace_keywords` which is used for the replacement
    of specific keywords. This function is not defined within the scope of `transform_dialogue`.
    """
    formatted = "\n".join("{role}: {content}".format(**item) for item in data)
    transformed = replace_keywords(formatted, {"assistant": "you", "user": "friend"})
    return transformed
