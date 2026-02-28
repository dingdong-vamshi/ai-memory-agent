import json
from memory_decay import recency_weight

class Memory:

    def __init__(self, file="data.json"):
        with open(file, "r") as f:
            self.data = json.load(f)

    def get_memories(self, name):
        found = []

        for item in self.data: 

            # check same supplier
            if item["supplier"].lower() == name.lower():
                w = recency_weight(item["date"])
                temp = item.copy()
                temp["weight"] = w 
                found.append(temp) 

        # higher impact first
        found.sort(key=lambda x: x["weight"] * x["severity"], reverse=True)

        return found[:5] 
    
if __name__ == "__main__":
    m = Memory()
    name = input("supplier: ")
    out = m.get_memories(name)

    print("\ncount:", len(out))
    for i in out:
        print(i["description"], "| weight:", round(i["weight"],2))