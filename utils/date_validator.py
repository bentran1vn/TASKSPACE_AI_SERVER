from datetime import datetime

def validate_date(date_str: str) -> bool:
    """Validate date string format (DD/MM/YYYY)."""
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False