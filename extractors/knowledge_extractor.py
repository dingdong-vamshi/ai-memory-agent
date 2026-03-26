# knowledge_extractor.py
# this is the bridge between raw information and long-term knowledge
# the idea is: a single incident is just information
# but when you see the same type of thing happen 3 times from the same supplier
# that becomes a pattern -- and patterns are knowledge
#
# knowledge is what the agent should actually use in its final decisions
# information is just evidence that might eventually become knowledge

import json
from datetime import datetime

CURRENT_DATE = datetime(2026, 2, 28)


def days_old(date_string):
    d = datetime.strptime(date_string, "%Y-%m-%d")
    return (CURRENT_DATE - d).days


def extract_knowledge(information_facts: list, supplier: str) -> list:
    """
    looks at the information layer for a given supplier
    and promotes repeating patterns into the knowledge layer

    the promotion threshold is 3 or more similar events in 6 months (180 days)
    below that threshold its a one-off, not a pattern worth preserving long-term
    """
    if not information_facts:
        return []

    # filter to just this supplier and recent enought to be relevant
    supplier_facts = [
        f for f in information_facts
        if f.get("supplier", "").lower() == supplier.lower()
        and days_old(f.get("date", "2020-01-01")) < 180
    ]

    knowledge = []

    # --- pattern 1: repeated price anomalies ---
    price_flags = [f for f in supplier_facts if f.get("type") == "price_deviation"]
    if len(price_flags) >= 2:
        knowledge.append({
            "supplier": supplier,
            "pattern": "recurring_price_deviations",
            "memory_type": "knowledge",   # long life -- this is a pattern
            "confidence": min(len(price_flags) * 0.3, 1.0),
            "date": CURRENT_DATE.strftime("%Y-%m-%d"),
            "description": f"supplier has {len(price_flags)} price deviations in past 6 months -- pricing is unreliable",
            "severity": 0.6
        })

    # --- pattern 2: repeated seasonal risk flags ---
    seasonal_flags = [f for f in supplier_facts if f.get("type") in ["seasonal_risk", "seasonal_delivery_risk"]]
    if len(seasonal_flags) >= 2:
        knowledge.append({
            "supplier": supplier,
            "pattern": "seasonal_quality_risk",
            "memory_type": "knowledge",
            "confidence": min(len(seasonal_flags) * 0.35, 1.0),
            "date": CURRENT_DATE.strftime("%Y-%m-%d"),
            "description": f"supplier consistently triggers seasonal risk flags -- summer deliveries are unreliable",
            "severity": 0.7
        })

    # --- pattern 3: dispute history from emails ---
    dispute_flags = [f for f in supplier_facts if len(f.get("disputes_found", [])) > 0]
    if len(dispute_flags) >= 1:
        knowledge.append({
            "supplier": supplier,
            "pattern": "dispute_history",
            "memory_type": "knowledge",
            "confidence": min(len(dispute_flags) * 0.5, 1.0),
            "date": CURRENT_DATE.strftime("%Y-%m-%d"),
            "description": f"supplier has raised {len(dispute_flags)} payment dispute(s) -- finance team should verify",
            "severity": 0.8
        })

    return knowledge


if __name__ == "__main__":
    # simulate some information-layer facts already stored
    sample_info = [
        {"supplier": "XYZ Electronics", "date": "2026-01-10", "type": "price_deviation", "detail": "..."},
        {"supplier": "XYZ Electronics", "date": "2026-02-05", "type": "price_deviation", "detail": "..."},
        {"supplier": "XYZ Electronics", "date": "2026-01-20", "type": "seasonal_risk", "detail": "..."},
        {"supplier": "XYZ Electronics", "date": "2026-02-01", "type": "seasonal_delivery_risk", "detail": "..."},
        {"supplier": "XYZ Electronics", "date": "2026-01-15", "disputes_found": ["claim"], "detail": "..."},
    ]
    results = extract_knowledge(sample_info, "XYZ Electronics")
    print(f"promoted {len(results)} patterns to knowledge layer:")
    for k in results:
        print(f"  [{k['pattern']}] confidence={k['confidence']} severity={k['severity']}")
        print(f"  -> {k['description']}")
