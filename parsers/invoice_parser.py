# invoice_parser.py
# invoices have zero sentiment -- they are just numbers and dates
# so relevance here doesn't come from tone, it comes from deviation
# the logic is: if everything matches what we expect, it's not interesting
# if something is off, that's worth flagging
#
# three strategies to find relevance in a document with no sentiment:
#   1. deviation detection -- compare against historical average
#   2. threshold breach -- pre-set rules (>10% price change = relevant)
#   3. cross-document linking -- does this invoice date fall in a known risk season?

import json
from datetime import datetime

# summer months -- march to may in india
# heat sensitive packaging causes quality issues in this period
# this logic comes from the problem statements example where it says
# "delivery quality degrades during summer months (March-May) due to heat-sensitive packaging"
# so if an invoice or PO falls in this window we flag it as a seasonl risk
SUMMER_MONTHS = [3, 4, 5]

# how much price deviation is acceptable before we flag it
PRICE_DEVIATION_THRESHOLD = 0.10  # 10%

# how much quantity deviation is acceptable
QTY_DEVIATION_THRESHOLD = 0.05  # 5%

# how many days between PO and invoice is normal
INVOICE_LAG_NORMAL_MAX = 30  # days


def parse_invoice(invoice: dict, historical_avg: dict) -> dict:
    """
    invoice: the current invoice as a dict
    historical_avg: average values for this supplier from past invoices
                    e.g. {"avg_amount": 200000, "avg_qty": 480}

    returns a list of information-layer facts with relevance flags
    if something doesnt deviate, we dont even store it -- its just noise
    """
    facts = []
    invoice_date = datetime.strptime(invoice["date"], "%Y-%m-%d")

    # --- check 1: price deviation ---
    if "amount" in invoice and "avg_amount" in historical_avg:
        deviation = abs(invoice["amount"] - historical_avg["avg_amount"]) / historical_avg["avg_amount"]
        if deviation > PRICE_DEVIATION_THRESHOLD:
            facts.append({
                "source": "invoice",
                "supplier": invoice["supplier"],
                "date": invoice["date"],
                "memory_type": "information",
                "relevance": "HIGH" if deviation > 0.25 else "MEDIUM",
                "type": "price_deviation",
                "detail": f"invoice amount {invoice['amount']} deviates {round(deviation*100, 1)}% from historical avg {historical_avg['avg_amount']}"
            })

    # --- check 2: quantity mismatch ---
    if "quantity" in invoice and "avg_qty" in historical_avg:
        qty_dev = abs(invoice["quantity"] - historical_avg["avg_qty"]) / historical_avg["avg_qty"]
        if qty_dev > QTY_DEVIATION_THRESHOLD:
            facts.append({
                "source": "invoice",
                "supplier": invoice["supplier"],
                "date": invoice["date"],
                "memory_type": "information",
                "relevance": "MEDIUM",
                "type": "quantity_mismatch",
                "detail": f"billed qty {invoice['quantity']} vs expected ~{historical_avg['avg_qty']}"
            })

    # --- check 3: seasonal risk ---
    # this is cross-document linking -- the invoice itself doesnt say anything about summer
    # but the date, when you cross it with existing knowledge about this supplier's seasonal pattern,
    # suddenly becomes meaningful information
    if invoice_date.month in SUMMER_MONTHS:
        facts.append({
            "source": "invoice",
            "supplier": invoice["supplier"],
            "date": invoice["date"],
            "memory_type": "information",
            "relevance": "MEDIUM",
            "type": "seasonal_risk",
            "detail": f"invoice date falls in summer (month {invoice_date.month}) -- known quality risk period for heat-sensitive suppliers"
        })

    # --- check 4: late invoice (PO to invoice lag) ---
    if "po_date" in invoice:
        po_date = datetime.strptime(invoice["po_date"], "%Y-%m-%d")
        lag_days = (invoice_date - po_date).days
        if lag_days > INVOICE_LAG_NORMAL_MAX:
            facts.append({
                "source": "invoice",
                "supplier": invoice["supplier"],
                "date": invoice["date"],
                "memory_type": "information",
                "relevance": "LOW",
                "type": "late_invoice",
                "detail": f"invoice arrived {lag_days} days after PO -- expected within {INVOICE_LAG_NORMAL_MAX} days"
            })

    # if nothing deviated, we return an empty list -- that's intentional
    # not everything needs to be stored. noise is the enemy of good decisions
    return facts


if __name__ == "__main__":
    sample_invoice = {
        "supplier": "XYZ Electronics",
        "date": "2026-03-15",
        "po_date": "2026-02-01",
        "amount": 280000,
        "quantity": 520
    }
    historical = {
        "avg_amount": 210000,
        "avg_qty": 480
    }
    results = parse_invoice(sample_invoice, historical)
    print(f"found {len(results)} relevant facts:")
    for r in results:
        print(f"  [{r['relevance']}] {r['type']}: {r['detail']}")
