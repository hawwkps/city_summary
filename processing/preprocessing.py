COLD_THRESHOLD = 0
EXPENSIVE_THRESHOLD = 100

def is_cold(temp_c: float) -> bool:
    return temp_c < COLD_THRESHOLD

def is_expensive(rate_to_rub: float) -> bool:
    return rate_to_rub > EXPENSIVE_THRESHOLD