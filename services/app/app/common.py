from typing import Dict, Any


def merge_into(initial: Any, updates: Any) -> Dict['str', Any]:
    """Recursively merges the contents of two dictionaries.

    Values of `updates` will override the values of initial. If
    a key is not in the initial dictionary it will be added with
    the the appropriate value.
    """

    if not isinstance(initial, dict):
        return updates

    acc = {}
    for key, value in initial.items():
        if isinstance(updates, dict):
            if key in updates:
                acc[key] = merge_into(value, updates[key])
            else:
                acc[key] = value
        else:
            acc[key] = updates

    for key, value in updates.items():
        if key not in acc:
            acc[key] = value

    return acc
