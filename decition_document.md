# Context & Memory Management for Business AI Agent

---

## 1. System Overview
This project implements a decision-support AI agent that uses past operational experiences to guide present business decisions.

Traditional enterprise systems rely only on current transaction data.  
This agent instead behaves like an experienced employee: when a new supplier event occurs, it retrieves relevant historical incidents, evaluates their importance, and produces a justified recommendation.

The system performs **experience-based reasoning**, not prediction.

---

## 2. Memory Model
The agent models four types of memory:

**Working Memory**  
The current supplier/event under evaluation.

**Long-Term Memory**  
Stored historical supplier incidents.

**Episodic Memory**  
Individual operational experiences such as quality failures, delivery delays, or defect spikes.

**Semantic Memory**  
Organizational rules that convert risk into actions (approve, review, inspect).

Each stored memory contains:
- supplier
- event type
- severity (business impact)
- defect rate (measurable reliability)
- date (time context)
- description (human explanation)

The system stores decision-relevant experiences rather than raw transaction logs.

---

## 3. Memory Lifecycle (Context Validity)
Past information gradually loses importance.

The system applies temporal decay:

```
weight = e^(−time_since_event / decay_factor)
```

Recent incidents strongly influence decisions, while older incidents fade.  
This prevents outdated bias and allows recognition of supplier improvement.

---

## 4. Context Retrieval & Information Overload
The agent retrieves only memories belonging to the same supplier and ranks them:

```
Relevance = severity × recency_weight
```

Only the Top-K most relevant memories are used.  
This removes noise while preserving critical context.

---

## 5. Conflict Resolution
Supplier history may be contradictory (bad earlier, good recently).  
Time-decay weighting prioritizes recent behavior, so the agent follows trends rather than isolated past incidents.

---

## 6. Decision Engine
Weighted memories are aggregated:

```
Risk Score = Σ(severity × recency_weight)
```

Actions:
- Low → Approve
- Medium → Review
- High → Inspect

Thus contextual memory becomes operational action.

---

## 7. Explainability
The agent outputs:
- retrieved incidents
- their weighted impact
- final risk score
- decision

This provides transparent, human-readable reasoning and builds trust.

---

## 8. Scalability
In real deployment:
- memories would be indexed by supplier
- stored in persistent storage
- retrieved via indexed lookups

Because only Top-K summaries are used, reasoning cost remains constant even with large datasets.

---

## 9. Privacy & Multi-Agent Use
Only summarized incidents are stored, avoiding sensitive transaction data.

Multiple agents (procurement, finance, support) can share the same memory store while applying different decision rules, enabling coordinated decisions.

---

## 10. Prototype
The prototype is a terminal-based agent that:
1. loads stored experiences
2. accepts supplier input
3. retrieves relevant memories
4. computes risk
5. outputs decision with explanation

It demonstrates context validity, lifecycle management, conflict handling, and explainable reasoning without enterprise infrastructure.