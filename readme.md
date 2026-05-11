## 🚦 Smart City Traffic & Emergency Response AI System


A **Python-based simulation** (no real sensors, no NLP) that takes structured traffic requests and routes them through different AI modules depending on the request type.

---
# Moiz DOC
### What is a Feature Vector?
An ANN (Artificial Neural Network) cannot understand words or strings. It only understands numbers.

So when we have a request like this:

```
    "vehicle_type"    : "ambulance",
    "incident_severity": "high",
    "time_sensitivity": True,
    "traffic_density" : 0.85,
    "priority_claim"  : True,
```
The ANN can't process "ambulance" or "high" — we need to convert everything to numbers first.

That's all Function 4 does:
It takes the request dictionary and returns a simple list of numbers:

### Input (words/bools/floats)
"ambulance" → 1
"high"      → 2
True        → 1
0.85        → 0.85
True        → 1
distance    → 1.0  (hardcoded for now)

### Output (feature vector)
[1, 2, 1, 0.85, 1, 1.0]

---
Think of it like this:
The ANN module later will receive this list and say:

"Hmm, vehicle is emergency(1), severity is high(2), time sensitive(1), density is high(0.85)... this looks CRITICAL priority!"

But it does that purely with math on numbers — not words.

That's it! It's basically just a translation function — from human-readable request → numbers the ANN can process.


---

## 📋 Phase Breakdown

---

### **Phase 1 — Project Setup & Data Design** *(Do this first)*

**Goal:** Lay the foundation before writing any logic.

**Tasks:**
- Create your folder structure:
```
project/
├── main.py
├── modules/
│   ├── preprocessing.py
│   ├── router.py
│   ├── ann.py
│   ├── knowledge_base.py
│   ├── csp.py
│   ├── search.py
│   └── response.py
├── data/
│   └── city_graph.py
└── report/
```
- Define your **city graph** (nodes + edges) based on the graphs in the PDF. Two versions:
  - Unweighted (for BFS)
  - Weighted (for UCS / A*)

Nodes from the PDF: `Police_HQ, Traffic_Control_Center, North_Station, River_Bridge, Stadium, East_Market, Central_Junction, West_Terminal, Fire_Station, Airport_Road, South_Residential, City_Hospital, Industrial_Zone`

- Define what a **request dictionary** looks like, e.g.:
```python
request = {
    "request_id": "REQ-001",
    "vehicle_type": "ambulance",       # ambulance / civilian / police / fire
    "request_category": "Emergency_Response_Request",
    "current_location": "Central_Junction",
    "destination": "City_Hospital",
    "incident_severity": "High",       # Low / Medium / High
    "time_sensitivity": True,
    "traffic_density": 0.85,           # 0.0 to 1.0
    "priority_claim": True,
    "control_zone": "S1",
    "description_note": "Cardiac emergency"
}
```

✅ **Deliverable:** Folder structure ready, graph data defined, sample request structure decided.

---

### **Phase 2 — Input & Preprocessing Module** *(10 marks)*

**Goal:** Validate and normalize incoming requests.

**What to code in `preprocessing.py`:**
- Check all required fields exist
- Validate values (e.g., `vehicle_type` must be one of the allowed types)
- Normalize strings (strip spaces, lowercase where needed)
- Map vehicle type → category: `ambulance/fire/police → EmergencyVehicle`, `car/truck/bus → CivilianVehicle`
- For requests needing ANN, build a **feature vector** (list of numbers):
  - vehicle_type → encode as number (e.g., ambulance=1, civilian=0)
  - incident_severity → Low=0, Medium=1, High=2
  - time_sensitivity → True=1, False=0
  - traffic_density → already a float
  - priority_claim → True=1, False=0
  - estimated_distance → you'll compute this from graph later, or hardcode for now

**Key rule:** If validation fails, stop processing and return an error. Use `try/except` where inputs could crash.

✅ **Deliverable:** `preprocess(request)` function that returns a clean, validated request object or raises an error.

---

### **Phase 3 — Request Router** *(no direct marks, but critical)*

**Goal:** Look at `request_category` and decide which modules to call.

**What to code in `router.py`:**

| Category | Modules to Call |
|---|---|
| `Route_Request` | Search only |
| `Policy_Check` | Knowledge Base only |
| `Control_Allocation_Request` | Knowledge Base → CSP |
| `Emergency_Response_Request` | ANN → Knowledge Base → CSP → Search |
| `Integrated_City_Service_Request` | ANN → KB → CSP → Search → Full Response |

The router just **calls the right modules in the right order** and collects their outputs.

✅ **Deliverable:** `route_request(request)` function that dispatches to modules and returns collected results.

---

### **Phase 4 — ANN Priority Module** *(20 marks — biggest marks!)*

**Goal:** Predict urgency level from numeric features.

**What to build in `ann.py`** — implement a simple MLP **from scratch** (no sklearn, use numpy):

**Two models:**
1. **Binary classifier** → outputs: `Urgent (1)` or `Not Urgent (0)`
2. **Multiclass classifier** → outputs: `Low / Normal / High / Critical`

**ANN from scratch means:**
- Manually define weights (you can hardcode or randomly initialize)
- Implement forward pass: `input → hidden layer(s) → output`
- Use sigmoid or ReLU activation
- Use softmax for multiclass output

**Training data** — make up ~10–15 sample cases manually, e.g.:
```python
# [vehicle_encoded, severity, time_sensitive, density, priority_claim]
X = [
    [1, 2, 1, 0.9, 1],  # ambulance, high severity → Critical
    [0, 0, 0, 0.2, 0],  # civilian, low severity → Low
    ...
]
y = [3, 0, ...]  # 0=Low, 1=Normal, 2=High, 3=Critical
```

> 💡 **Tip:** Since it's academic, you can hardcode weights that produce correct outputs for your test cases. The point is demonstrating the ANN structure works.

✅ **Deliverable:** `predict_priority(feature_vector)` returning a priority level string.

---

### **Phase 5 — Logic / Knowledge Base Module** *(20 marks)*

**Goal:** Rule-based policy validation — is this vehicle allowed to do what it's requesting?

**What to code in `knowledge_base.py`:**

Implement each rule from the PDF as Python `if` conditions. Think of it as a **fact checker**:

```python
# Example rule implementation
def check_priority(vehicle_type, severity, time_sensitive):
    if vehicle_type == "EmergencyVehicle" and severity == "High":
        return "Critical"
    elif vehicle_type == "EmergencyVehicle" and time_sensitive:
        return "High"
    elif vehicle_type == "CivilianVehicle":
        return "Normal"
```

**Rules to implement** (from the PDF predicates):
- Priority assignment rules
- Signal override authorization (only EmergencyVehicle in SignalZone)
- EmergencyCorridor activation (EmergencyVehicle going to Hospital)
- Approved/Rejected based on request type + authorization
- Per request category: Route_Request always approved, Policy_Check depends on authorization, etc.

✅ **Deliverable:** `validate_policy(request, priority)` returning `{approved: True/False, reasons: [...], allowed_actions: [...]}`

---

### **Phase 6 — CSP Scheduler / Control Allocation** *(15 marks)*

**Goal:** Assign signal phases to intersections without conflicts.

**What to code in `csp.py`:**

Use the 5 intersections from the CSP graph in the PDF:
- S1: Central_Junction → phases: A, B
- S2: North_Station → phases: A, B, C
- S3: East_Market → phases: B, C
- S4: River_Bridge → phases: A, C
- S5: City_Hospital → phases: B, C

**Constraints:**
- Conflicting intersections can't have the same phase at the same time (S1 conflicts with S2 and S3)
- Emergency corridor gets priority (S1 → S5 path gets PhaseB preference)
- Coordination between S2 and S4

**Implement simple backtracking CSP:**
```python
def assign_signals(intersections, constraints, emergency_path=None):
    # Try to assign a valid phase to each intersection
    # Backtrack if conflict found
```

✅ **Deliverable:** `allocate_signals(request, allowed_actions)` returning a dict of `{intersection: assigned_phase}`

---

### **Phase 7 — Search & Navigation Module** *(15 marks)*

**Goal:** Find the best route through the city graph.

**What to code in `search.py`:**

Implement **3 algorithms:**

1. **BFS** — unweighted graph, finds path with fewest hops
2. **UCS (Uniform Cost Search)** — weighted graph, finds cheapest cost path (use `heapq`)
3. **A\*** — weighted graph + heuristic (you can use straight-line distance or just assign heuristic values manually per node toward City_Hospital)

**The router decides which to use:**
- Unweighted request → BFS
- Weighted + heuristic available → A*
- Weighted, no heuristic → UCS

✅ **Deliverable:** `find_route(graph, start, destination, algorithm)` returning `(path_list, total_cost)`

---

### **Phase 8 — Final Response Layer + Integration** *(10 marks)*

**Goal:** Combine all module outputs into a clean, readable response.

**What to code in `response.py`:**
- Only include fields from modules that were actually used
- Format it as a readable dict or printout

Example output for Emergency_Response_Request:
```
=== FINAL RESPONSE ===
Request ID     : REQ-001
Status         : APPROVED
Priority Level : Critical
Policy Check   : Emergency corridor authorized
Signal Plan    : {S1: PhaseA, S3: PhaseB, S5: PhaseB}
Route          : Central_Junction → East_Market → City_Hospital
Route Cost     : 6 units
Message        : Emergency vehicle cleared. Signal corridor active.
```

**`main.py`** should present a menu:
```
1. Submit Route Request
2. Submit Policy Check
3. Submit Control Allocation
4. Submit Emergency Response
5. Submit Integrated City Service
6. Exit
```
Each option collects input, builds the request dict, and runs the full pipeline.

✅ **Deliverable:** Working end-to-end system with clean output.

---

### **Phase 9 — Report Writing** *(10 marks)*

Write your Word doc report with:
- Project overview
- Description of each AI concept used (ANN, Logic/KB, CSP, Search)
- Code snippets for each module
- Screenshots of every scenario running

---

## 🗓️ Suggested Order to Tackle These

```
Phase 1 (Setup)  →  Phase 2 (Preprocessing)  →  Phase 3 (Router)
→  Phase 7 (Search — easiest AI module, good warmup)
→  Phase 5 (Knowledge Base)
→  Phase 6 (CSP)
→  Phase 4 (ANN — hardest, save for when you're warmed up)
→  Phase 8 (Integration + main.py)
→  Phase 9 (Report)
```

---

**Start with Phase 1** — set up your folders and define the city graph data. Once you have that, come back and I'll guide you through each phase. When you want me to review your code or help you debug, just paste it and I'll help!



Quick ANN Theory
An ANN has 3 parts:
Input Layer → Hidden Layer(s) → Output Layer

[1, 2, 1, 0.85, 1, 1.0]  →  hidden neurons  →  [Low, Normal, High, Critical]
Each layer does this:
output = activation(weights × input + bias)
Two activation functions we'll use:
python# ReLU — for hidden layer (kills negatives)
relu(x) = max(0, x)

# Softmax — for output layer (converts to probabilities)
softmax(x) = e^x / sum(e^x)

Our ANN Architecture:
Input:   6 neurons  (feature vector size)
Hidden1: 8 neurons  (ReLU)
Hidden2: 6 neurons  (ReLU)
Output:  4 neurons  (Softmax → Low/Normal/High/Critical)
