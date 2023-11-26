import json

with open('mock/mock_users.json', 'r') as f:
    """
    Expected something like this,
    {
        "bot": {
            "name": "XX",
            "avatar": "url or emoji"
        },
        "user": {
            "name": "YY",
            "avatar": "url or emoji"
        }
    }
    """
    data = json.load(f)

# export this
mock_session: dict = data