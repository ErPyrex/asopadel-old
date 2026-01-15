"""
Utility functions for the core application.
Contains role-checking functions and other helpers.
"""


def IsAdmin(User):
    """
    Check if a user has administrator privileges.
    
    Args:
        User: The user object to check
        
    Returns:
        bool: True if user is authenticated and is an administrator
    """
    return User.is_authenticated and User.es_admin_aso


def IsArbitro(User):
    """
    Check if a user is a referee (arbitro).
    
    Args:
        User: The user object to check
        
    Returns:
        bool: True if user is authenticated and is a referee
    """
    return User.is_authenticated and User.es_arbitro


def IsJugador(User):
    """
    Check if a user is a player (jugador).
    
    Args:
        User: The user object to check
        
    Returns:
        bool: True if user is authenticated and is a player
    """
    return User.is_authenticated and User.es_jugador


def IsAdminOrArbitro(User):
    """
    Check if a user is either an admin or a referee.
    
    Args:
        User: The user object to check
        
    Returns:
        bool: True if user is authenticated and is an admin OR a referee
    """
    return User.is_authenticated and (User.es_admin_aso or User.es_arbitro)

