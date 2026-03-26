# email_parser.py
# emails are actualy the most information-rich source we have
# unlike invoices which are just numbers, emails have intent, tone, commitments
# so we extract two things:
#   1. sentiment signal (positive / negative / neutral)
#   2. factual claims -- discounts offered, delays apologised, disputes raised
# none of this needs an LLM -- keyword matching gets us 80% of the way there

import json
from datetime import datetime

NEGATIVE_SIGNALS = [
    "apologize", "apologies", "sorry", "delay", "damaged", "broken",
    "defective", "issue", "problem", "dispute", "claim", "non-receipt",
    "complaint", "unfortunately"
]

POSITIVE_SIGNALS = [
    "thank you", "pleased", "on time", "successfully", "delivered",
    "resolved", "happy to", "discount", "early payment", "offer"
]

COMMITMENT_SIGNALS = [
    "will deliver", "will send", "we offer", "we guarantee", "we commit",
    "payment within", "discount for", "by end of"
]

DISPUTE_SIGNALS = [
    "dispute", "claim", "non-receipt", "didnt receive", "not received",
    "incorrect amount", "overcharged"
]


def parse_email(email_text: str, supplier: str, date: str) -> dict:
    """
    takes raw email text and returns structured information layer facts
    the sentiment score is just a number between -1 and 1
    the facts list is what actually gets stored in teh information layer
    """
    text_lower = email_text.lower()

    # count positive and negative keyword hits
    neg_hits = sum(1 for w in NEGATIVE_SIGNALS if w in text_lower)
    pos_hits = sum(1 for w in POSITIVE_SIGNALS if w in text_lower)

    total = neg_hits + pos_hits
    if total == 0:
        sentiment_score = 0.0
    else:
        # ranges from -1 (all negative) to +1 (all positive)
        sentiment_score = (pos_hits - neg_hits) / total

    # extract any commitments
    commitments = [sig for sig in COMMITMENT_SIGNALS if sig in text_lower]

    # extract any disputes
    disputes = [sig for sig in DISPUTE_SIGNALS if sig in text_lower]

    # build the information layer entry
    # this is RAW information -- short shelf life, 30 day half life
    facts = {
        "source": "email",
        "supplier": supplier,
        "date": date,
        "memory_type": "information",   # short life -- raw data
        "sentiment_score": round(sentiment_score, 2),
        "sentiment_label": (
            "negative" if sentiment_score < -0.2 else
            "positive" if sentiment_score > 0.2 else
            "neutral"
        ),
        "commitments_found": commitments,
        "disputes_found": disputes,
        "raw_text_preview": email_text[:200]  # first 200 chars only, not whole email
    }

    # if there are disputes or strong negative signal, also flag for knowledge extraction
    # the knowledge extractor will decide if this is a pattern or a one-off
    facts["flag_for_knowledge_extraction"] = (
        len(disputes) > 0 or sentiment_score < -0.4
    )

    return facts


if __name__ == "__main__":
    sample = """
    Dear team, we apologize for the delay in our last shipment. 
    The transport strike caused unexpected issues. We will deliver 
    the remaining units by end of next week. We also offer a 2% 
    discount for early payment on invoice #1042.
    """
    result = parse_email(sample, supplier="XYZ Electronics", date="2026-01-15")
    print(json.dumps(result, indent=2))
