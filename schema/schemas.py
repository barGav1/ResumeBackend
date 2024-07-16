from typing import List, Dict, Optional

def individual_serial(todo: Dict[str, any]) -> Dict[str, any]:
    """
    Serializes a single todo document into a dictionary.
    """
    return {
        "id": str(todo.get("_id", "")),
        "name": todo.get("name", ""),
        "description": todo.get("description", ""),
        "complete": todo.get("complete", False)
    }

def list_serial(todos: List[Dict[str, any]]) -> List[Dict[str, any]]:
    """
    Serializes a list of todo documents.
    """
    return [individual_serial(todo) for todo in todos]

def user_serial(user: Dict[str, any]) -> Dict[str, any]:
    """
    Serializes a single user document into a dictionary.
    """
    return {
        "id": str(user.get("_id", "")),
        "email": user.get("email", ""),
        "password": user.get("password", "")  # Note: Avoid sending passwords in responses for security reasons
    }

def list_users(users: List[Dict[str, any]]) -> List[Dict[str, any]]:
    """
    Serializes a list of user documents.
    """
    return [user_serial(user) for user in users]
