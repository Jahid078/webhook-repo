def format_log(entry):
    """
    Format log entries based on action type.
    """
    timestamp = entry["timestamp"]
    if entry["action"] == "push":
        return f'{entry["author"]} pushed to {entry["to_branch"]} on {timestamp}'
    elif entry["action"] == "pull_request":
        return f'{entry["author"]} submitted a pull request from {entry["from_branch"]} to {entry["to_branch"]} on {timestamp}'
    elif entry["action"] == "merge":
        return f'{entry["author"]} merged branch {entry["from_branch"]} to {entry["to_branch"]} on {timestamp}'