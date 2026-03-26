from datetime import datetime
import math

CURRENT_DATE = datetime(2026, 2, 28)

# different memory types decay at diferent rates
# information is raw data -- invoce number, email text -- it expires fast
# knowledge is a derived insight -- supplier delays every monsoon -- it lasts longer
# evergreen is things like contract terms that basically never expire
HALF_LIVES = {
    "information": 30,    # 30 day half life -- raw facts
    "knowledge":   365,   # 1 year half life -- patterns and insights
    "evergreen":   9999   # never really expires -- contract rules etc
}

def days_since(date_string):
    event_date = datetime.strptime(date_string, "%Y-%m-%d")
    return (CURRENT_DATE - event_date).days

def recency_weight(date_string, memory_type="knowledge"):
    # formula: e^(-0.693 * days / half_life)
    # at exactly half_life days the weight drops to 0.5
    # this lets different memory types age at their own pace
    days = days_since(date_string)
    half_life = HALF_LIVES.get(memory_type, 90)
    weight = math.exp(-0.693 * days / half_life)
    return weight

# backwards compat -- old code that calls recency_weight with just a date still works
def legacy_recency_weight(date_string):
    return recency_weight(date_string, memory_type="knowledge")

if __name__ == "__main__":
    date = input("enter date (YYYY-MM-DD): ")
    print("days since:", days_since(date))
    for mtype in HALF_LIVES:
        w = recency_weight(date, mtype)
        print(f"  {mtype} weight: {round(w, 4)}")