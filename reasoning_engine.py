class Think:

    def risk(self, mems):

        if len(mems) == 0:
            return 0, ["No history for this supplier"]

        total = 0
        reasons = []

        for m in mems:
            s = m["severity"] * m["weight"]
            total += s

            txt = m["description"] + " (" + m["date"] + ") -> impact " + str(round(s,2))
            reasons.append(txt)

        if total > 1:
            total = 1

        return total, reasons

    def action(self, r):

        if r > 0.6:
            return "INSPECT" 
        if r > 0.3:
            return "REVIEW" 

        return "APPROVE" 
    
if __name__ == "__main__": 
    test = [
        {"description":"major defect","date":"2025-12-15","severity":0.9,"weight":0.7}, 
        {"description":"packaging issue","date":"2025-10-02","severity":0.7,"weight":0.4} 
    ]

    t = Think()
    r, why = t.risk(test)
    d = t.action(r)

    print("risk:", round(r,2))
    print("decision:", d)
    for w in why:
        print("-", w)