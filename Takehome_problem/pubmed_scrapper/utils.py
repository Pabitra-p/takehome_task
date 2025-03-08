def log_debug(message: str, debug: bool):
    """Prints debug messages if debug mode is enabled."""
    if debug:
        print(f"[DEBUG] {message}")
