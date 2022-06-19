import logging

round = 6

def log_warning(text: str) -> None:
    """
    example code
    if influence_delta:
        log_warning(f"Player {player.get_id()} attempted to spend {influence_amount} on Leadership.")
    """
    logging.warning(f"Round {round}: " + text)

def log(text: str) -> None:
    logging.info(f"Round {round}: " + text)

