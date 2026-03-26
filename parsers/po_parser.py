# po_parser.py
# purchase orders are structural documents like invoices
# no sentiment here -- relevance comes from:
#   1. who is it going to (warehouse) -- do we have risk history there?
#   2. when is it expected -- seasonal risk window?
#   3. what volume is being ordered -- is this a spike or normal?

import json
from datetime import datetime

# warehouses with known logistics issues
# in a real system this would come from the knowledge store
# for the prototype we hardcode it as a lookup table
RISKY_WAREHOUSES = {
    "Warehouse A": "severe road damage during monsoon (July 2024), caused 9+ hour delays",
    "Warehouse C": "flooding reported in 2023, access issues during heavy rain"
}

SUMMER_MONTHS = [3, 4, 5]

VOLUME_SPIKE_THRESHOLD = 0.30  # 30% above historical avg triggers flag


def parse_po(po: dict, historical_avg: dict) -> dict:
    """
    po: current purchase order as a dict
    historical_avg: e.g. {"avg_qty": 500}

    returns list of information-layer facts that are actually relevant
    irrelevant POs return empty list -- again, silence is fine
    """
    facts = []
    delivery_date = datetime.strptime(po["delivery_date"], "%Y-%m-%d")

    # --- check 1: risky warehouse ---
    warehouse = po.get("ship_to", "")
    if warehouse in RISKY_WAREHOUSES:
        facts.append({
            "source": "po",
            "supplier": po["supplier"],
            "date": po["issue_date"],
            "memory_type": "information",
            "relevance": "HIGH",
            "type": "warehouse_risk",
            "detail": f"ship-to is {warehouse}: {RISKY_WAREHOUSES[warehouse]}"
        })

    # --- check 2: seasonal delivery window ---
    # the delivery is expected in summer months
    # this combines with supplier history -- if supplier already has summer quality issues
    # and the delivery is scheduled in that window, that's a meaningful combination
    if delivery_date.month in SUMMER_MONTHS:
        facts.append({
            "source": "po",
            "supplier": po["supplier"],
            "date": po["issue_date"],
            "memory_type": "information",
            "relevance": "MEDIUM",
            "type": "seasonal_delivery_risk",
            "detail": f"delivery expected in month {delivery_date.month} -- summer risk window for heat-sensitive goods"
        })

    # --- check 3: volume spike ---
    if "quantity" in po and "avg_qty" in historical_avg:
        spike = (po["quantity"] - historical_avg["avg_qty"]) / historical_avg["avg_qty"]
        if spike > VOLUME_SPIKE_THRESHOLD:
            facts.append({
                "source": "po",
                "supplier": po["supplier"],
                "date": po["issue_date"],
                "memory_type": "information",
                "relevance": "MEDIUM",
                "type": "volume_spike",
                "detail": f"order qty {po['quantity']} is {round(spike*100)}% above usual avg of {historical_avg['avg_qty']}"
            })

    return facts


if __name__ == "__main__":
    sample_po = {
        "supplier": "XYZ Electronics",
        "issue_date": "2026-03-10",
        "delivery_date": "2026-04-05",
        "ship_to": "Warehouse A",
        "quantity": 700
    }
    historical = {"avg_qty": 500}
    results = parse_po(sample_po, historical)
    print(f"found {len(results)} relevant facts from PO:")
    for r in results:
        print(f"  [{r['relevance']}] {r['type']}: {r['detail']}")
