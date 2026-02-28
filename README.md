#  Business Memory Decision Agent

A prototype AI decision-support system that mimics how experienced managers use past supplier incidents to guide current operational decisions.

---

## Overview

Most enterprise systems rely only on present transaction data.

This agent introduces **experience-based reasoning**.  
When given a supplier name, it:

- Retrieves past incidents
- Applies time-based memory decay
- Evaluates severity
- Computes a risk score
- Recommends an action with explanation

The focus is on context and memory management — not machine learning.

---

## How It Works

The agent follows a simple reasoning pipeline:

```
User Input
   ↓
Memory Retrieval
   ↓
Time-Based Weighting
   ↓
Risk Calculation
   ↓
Decision + Explanation
```

### Risk Formula

```
Risk Score = Σ (severity × recency_weight)
```

Where:

```
recency_weight = e^(-λ × days_since_incident)
```

Recent incidents influence decisions more than older ones.

---

## Project Structure

```
ai-memory-agent/
│
├── agent.py
├── memory_manager.py
├── memory_decay.py
├── reasoning_engine.py
├── data.json
└── README.md
```

---

## Run the Project

```bash
python3 agent.py
```

Example input:

```
XYZ Electronics
```

---

## Example Output

```
Relevant memories retrieved: 2

- 30% of delivered circuit boards were damaged (2025-12-15)
  Weighted Impact: 0.65

- Packaging failure caused moisture damage (2025-10-02)
  Weighted Impact: 0.29

Risk Score: 0.74
Decision: INSPECT
```

---

## Key Concepts

- Context-aware decision making  
- Experience-based reasoning  
- Time-dependent memory relevance  
- Explainable business AI  

---

## Purpose

Developed as part of an internship assignment on  
**Context and Memory Management for AI Agents in Business Environments**.

This prototype demonstrates how an AI agent can accumulate experience, evaluate relevance, and justify operational decisions. 