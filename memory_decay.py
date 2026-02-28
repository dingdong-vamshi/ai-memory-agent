from datetime import datetime
import math

CURRENT_DATE = datetime(2026, 2, 28)

def days_since(date_string):
    event_date = datetime.strptime(date_string, "%Y-%m-%d")
    return (CURRENT_DATE - event_date).days

def recency_weight(date_string):

    # More recent memories should matter more.
    # We use exponential decay.

    days = days_since(date_string)

    # 90 day memory half-life
    decay_factor = 90 

    weight = math.exp(-days / decay_factor) 
    return weight

if __name__ == "__main__":
    date = input("date ")
    print(days_since(date))
    print(recency_weight(date)) 