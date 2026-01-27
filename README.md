# ChangiLink AI  

Intelligent MRT Routing and Disruption Support System for Changi Airport Terminal 5

  

## Overview

ChangiLink AI is an AI-based prototype system developed to support intelligent MRT route planning, service advisory validation, and crowding-risk prediction for Singapore’s rail network, with a focus on the Changi Airport – Terminal 5 (T5) corridor.

  

The system models both:

  

- **Today Mode** – Current MRT network with East-West Line (EWL) airport branch operations.

- **Future Mode** – Planned network based on LTA’s July 2025 announcement, including:

  - Thomson-East Coast Line Extension (TELe) from Sungei Bedok → T5 → Tanah Merah,

  - Conversion of Tanah Merah–Expo–Changi Airport stations to TEL systems,

  - Cross Island Line (CRL) extension to T5.

  

This project demonstrates the application of multiple AI techniques to real-world transportation planning and disruption management.

  

---

  

## Key Features

  

### 1. MRT Network Graph Modeling

- Stations represented as nodes and rail connections as edges.

- Weighted edges using:

  - Travel time,

  - Transfer penalties,

  - Crowding-risk penalties.

- Supports both Today Mode and Future Mode network configurations.

  

---

  

### 1. AI Route Planning with Search Algorithms

Implemented algorithms:

  

- Breadth-First Search (BFS)

- Depth-First Search (DFS)

- Greedy Best-First Search (GBFS)

- A* Search

  

Features:

- Custom cost function (travel time + transfer penalty + crowding penalty)

- Heuristic based on straight-line distance between stations

- Performance evaluation:

  - Runtime

  - Nodes expanded

  - Path cost

- Comparison between Today Mode and Future Mode results

  

---

### 2. Logical Inference for MRT Service Rules & Advisory Consistency

- MRT operational rules and service advisories are formalised using propositional logic.

- The logic model explicitly captures:

  - Thomson–East Coast Line Extension (TELe) and Cross Island Line (CRL) changes,

  - Conversion of Tanah Merah–Expo–Changi Airport stations to TEL systems,

  - Temporary service adjustments during systems integration works.

- At least 10 logical rules are defined to represent routing constraints and service conditions.

- A resolution-based inference mechanism is implemented to:

  - Validate whether a proposed route complies with current service advisories,

  - Detect internal contradictions within advisory information,

  - Identify the specific rule(s) violated when a route or advisory is invalid.

Logical inference is demonstrated across multiple scenarios in both Today Mode and Future Mode.

  

---

### 3. Crowding Risk Prediction using Bayesian Networks

Bayesian network variables include:

  

- Weather

- Time of day

- Day type

- Network mode (Today / Future)

- Service status (Normal / Reduced / Disrupted)

- Demand proxy

- Crowding risk (Low / Medium / High)

  

Capabilities:

- Scenario-based inference

- Comparison of crowding risk between Today Mode and Future Mode

- Evaluation of impact from service disruptions and network upgrades

  

---

  

### (Bonus) Passenger Re-Routing Optimization

Optional advanced component:

  

- Disruption scenarios (segment suspensions, reduced service, increased transfer penalties)

- Optimization objectives:

  - Minimize total travel time

  - Minimize average delay

  - Minimize worst-case delay

- AI techniques:

  - Local Search

  - Hill Climbing

  - Simulated Annealing

  - Constraint Satisfaction

  

---

  

## Project Structure

- (to be updated)

  
  
  

## Technologies & Tools

- Programming Language: Python (recommended)

- Libraries:

  - NetworkX (graph modeling)

  - NumPy / Pandas (data handling)

  - pgmpy or PyMC (Bayesian networks)

  - Matplotlib / Seaborn (visualization)

- Development:

  - Git & GitHub

  - Jupyter Notebook or Python scripts
