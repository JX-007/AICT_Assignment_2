

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD

# -----------------------
# States
# -----------------------
W_states = ["clear", "rainy", "thunderstorms"]
T_states = ["morning", "afternoon", "evening"]
D_states = ["weekday", "weekend"]
M_states = ["today", "future"]
S_states = ["normal", "reduced", "disrupted"]
P_states = ["low", "medium", "high"]
C_states = ["low", "medium", "high"]

# -----------------------
# Structure (DAG)
# -----------------------
# Mode affects demand (route attractiveness / flow shift), NOT service.
model = DiscreteBayesianNetwork([
    ("W", "P"), ("T", "P"), ("D", "P"), ("M", "P"),  # demand drivers (route-specific)
    ("P", "C"), ("S", "C")                           # crowding depends on demand + service status
])

# -----------------------
# Priors
# -----------------------
cpd_W = TabularCPD("W", 3, [[0.532], [0.140], [0.328]], state_names={"W": W_states})
cpd_T = TabularCPD("T", 3, [[0.351], [0.270], [0.378]], state_names={"T": T_states})
cpd_D = TabularCPD("D", 2, [[0.72], [0.28]], state_names={"D": D_states})

# Mode prior not too important (you usually set M in evidence)
cpd_M = TabularCPD("M", 2, [[0.50], [0.50]], state_names={"M": M_states})

# Service status is INCLUDED (required), but independent of Mode in this assumption.
# (You can treat it as "current operating condition/advisory".)
cpd_S = TabularCPD(
    "S", 3,
    [[0.85], [0.10], [0.05]],  # normal, reduced, disrupted
    state_names={"S": S_states}
)

# -----------------------
# Demand Proxy: P | W,T,D,M  (3*3*2*2 = 36 columns)
# We'll generate this CPT with a simple scoring rule:
# - Weekday + peak (morning/evening) -> higher demand
# - Rain/thunder -> higher demand
# - Future mode -> demand shift for Bayshore->Expo (slightly higher) due to network changes
#   (CRL + TEL conversions change route attractiveness / transfers / access patterns)
# -----------------------
values_low, values_med, values_high = [], [], []

for w in W_states:
    for t in T_states:
        for d in D_states:
            for m in M_states:
                score = 0
                if d == "weekday":
                    score += 1
                if t in ["morning", "evening"]:
                    score += 1
                if w == "rainy":
                    score += 1
                elif w == "thunderstorms":
                    score += 2

                # MODE EFFECT (your chosen assumption):
                # Future doesn't change service, but can shift demand for this route.
                # Add a small bump in demand for future.
                if m == "future":
                    score += 1

                # Map score -> (low, medium, high) probabilities
                if score <= 1:
                    p_low, p_med, p_high = 0.60, 0.30, 0.10
                elif score == 2:
                    p_low, p_med, p_high = 0.35, 0.45, 0.20
                elif score == 3:
                    p_low, p_med, p_high = 0.20, 0.45, 0.35
                elif score == 4:
                    p_low, p_med, p_high = 0.12, 0.38, 0.50
                else:  # 5+
                    p_low, p_med, p_high = 0.08, 0.27, 0.65

                values_low.append(p_low)
                values_med.append(p_med)
                values_high.append(p_high)

cpd_P = TabularCPD(
    "P", 3,
    [values_low, values_med, values_high],
    evidence=["W", "T", "D", "M"],
    evidence_card=[3, 3, 2, 2],
    state_names={"P": P_states, "W": W_states, "T": T_states, "D": D_states, "M": M_states}
)

# -----------------------
# Crowding Risk: C | P,S (3*3=9 columns)
# -----------------------
C_table = {
    ("low",    "normal"):    (0.80, 0.18, 0.02),
    ("low",    "reduced"):   (0.60, 0.32, 0.08),
    ("low",    "disrupted"): (0.25, 0.40, 0.35),

    ("medium", "normal"):    (0.35, 0.55, 0.10),
    ("medium", "reduced"):   (0.18, 0.52, 0.30),
    ("medium", "disrupted"): (0.06, 0.30, 0.64),

    ("high",   "normal"):    (0.15, 0.50, 0.35),
    ("high",   "reduced"):   (0.06, 0.30, 0.64),
    ("high",   "disrupted"): (0.02, 0.12, 0.86),
}

vals_c_low, vals_c_med, vals_c_high = [], [], []
for p in P_states:
    for s in S_states:
        lo, me, hi = C_table[(p, s)]
        vals_c_low.append(lo)
        vals_c_med.append(me)
        vals_c_high.append(hi)

cpd_C = TabularCPD(
    "C", 3,
    [vals_c_low, vals_c_med, vals_c_high],
    evidence=["P", "S"],
    evidence_card=[3, 3],
    state_names={"C": C_states, "P": P_states, "S": S_states}
)

# -----------------------
# Finalize
# -----------------------
model.add_cpds(cpd_W, cpd_T, cpd_D, cpd_M, cpd_S, cpd_P, cpd_C)
assert model.check_model()
