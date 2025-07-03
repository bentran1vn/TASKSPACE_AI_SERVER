from datetime import datetime

def validate_date(date_str: str) -> bool:
    """Validate date string format (YYYY-MM-DD HH:MM:SS)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False