from memory_manager import Memory
from reasoning_engine import Think

def main():

    print("Business Decision Agent")
    print("-----------------------")

    name = input("Supplier name: ") 

    mem = Memory() 
    brain = Think() 

    data = mem.get_memories(name) 

    print("\nmemories found:", len(data)) 

    r, reasons = brain.risk(data) 
    act = brain.action(r) 

    print("\nwhy?") 
    for i in reasons: 
        print("-", i) 

    print("\nrisk:", round(r,2)) 
    print("decision:", act) 


if __name__ == "__main__": 
    main() 