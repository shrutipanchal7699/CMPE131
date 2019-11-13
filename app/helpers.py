from datetime import datetime

def cast_date(str):
    """casts string as a date"""
    return datetime.strptime(str, '%Y-%m-%d').date()