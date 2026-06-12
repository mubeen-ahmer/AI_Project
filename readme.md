# Smart City Traffic & Emergency Response AI System

A modular AI pipeline that processes city traffic requests and returns routing, signal coordination, and policy decisions based on request type.

---

## Stack

- Python 3.x
- NumPy (ANN only)

```bash
pip install numpy
python main.py
```

---

## Project Structure

```
SmartTraffic/
├── main.py
├── data/
│   └── city_graph.py
└── modules/
    ├── preprocessing.py
    ├── router.py
    ├── ann.py
    ├── knowledge_base.py
    ├── csp.py
    ├── search.py
    └── response.py
```

---

## How It Works

Request type determines which modules run. Nothing else does.

| Request Type | Pipeline |
|---|---|
| Route Request | Search (BFS) |
| Policy Check | Knowledge Base |
| Control Allocation | KB → CSP |
| Emergency Response | ANN → KB → CSP → A* |
| Integrated Service | ANN → KB → CSP → A* |

---

## Modules

**Preprocessing** — validates fields, normalizes strings, maps vehicle to class, builds ANN feature vector.

**Router** — reads `request_category`, returns pipeline list.

**ANN** — MLP built with NumPy from scratch. 6 inputs → 8 → 6 → 4 outputs (Low / Normal / High / Critical). Trained via backpropagation on 15 examples. Trains once on first call.

**Knowledge Base** — rule-based policy engine. Determines priority, checks authorization, approves or rejects request based on vehicle class, severity, destination, and request type.

**CSP** — assigns signal phases to 5 intersections using backtracking. Constraints: S1≠S2, S1≠S3. Emergency override forces S1=PhaseA, S4=PhaseC, S5=PhaseB when priority is Critical.

**Search** — BFS on unweighted graph (route requests), A* on weighted graph with manual heuristic (emergency). UCS also implemented.

**Response** — aggregates outputs from modules that actually ran. Fields from unused modules are excluded.

---

## City Graph

13 nodes, 2 versions — unweighted (BFS) and weighted (UCS/A*).

```
Police_HQ  Traffic_Control_Center  North_Station  River_Bridge
Stadium  Airport_Road  South_Residential  City_Hospital
East_Market  Central_Junction  West_Terminal  Fire_Station  Industrial_Zone
```

Signal intersections: `S1=Central_Junction  S2=North_Station  S3=East_Market  S4=River_Bridge  S5=City_Hospital`

---

## Example

```
Option  : 4 (Emergency Response)
Vehicle : ambulance
From    : Central_Junction
To      : City_Hospital
Severity: high  |  Time sensitive: true  |  Density: 0.85
```

```
ANN          → Critical
KB           → APPROVED [SignalOverride, EmergencyCorridor, EmergencyRoute]
CSP          → S1=PhaseA  S2=PhaseB  S3=PhaseB  S4=PhaseC  S5=PhaseB
A*           → Central_Junction → East_Market → City_Hospital (cost: 6)
```