from typing import List
from dataclasses import dataclass, field
from data_structures import NetworkMode


@dataclass
class TestScenario:
    """Represents a test scenario"""
    scenario_id: str
    mode: NetworkMode
    scenario_type: str  # "Valid", "Invalid", "Contradictory"
    description: str
    facts: List[str]  # Propositional facts (no variables)
    query: str  # Proposition to prove
    expected_result: bool
    expected_violated_rules: List[str] = field(default_factory=list)
    explanation: str = ""


def create_test_scenarios() -> List[TestScenario]:
    """
    Create test scenarios using PROPOSITIONAL LOGIC (concrete propositions only).
    
    Covers:
    - Both Today Mode and Future Mode
    - Valid, invalid, and contradictory cases
    - TELe/CRL changes (conversion, systems integration)
    """
    scenarios = [
        # ========== TODAY MODE SCENARIOS ==========
        TestScenario(
            scenario_id="S1",
            mode=NetworkMode.TODAY,
            scenario_type="Valid",
            description="Today Mode: Normal EWL operation - all stations open",
            facts=[
                "StationOpen_TanahMerah",
                "StationOpen_Expo",
                "StationOpen_ChangiAirport",
            ],
            query="RouteInvalid",
            expected_result=False,
            explanation="All stations are open. No rules are violated, so route is valid."
        ),
        
        TestScenario(
            scenario_id="S2",
            mode=NetworkMode.TODAY,
            scenario_type="Invalid",
            description="Today Mode: Expo station closed - route becomes invalid",
            facts=[
                "StationClosed_Expo",
                "RouteIncludesExpo",
            ],
            query="RouteInvalid",
            expected_result=True,
            expected_violated_rules=["R1", "R4"],
            explanation="Expo is closed (R1 → CannotBoard_Expo), route includes Expo (R4 → RouteInvalid)"
        ),
        
        TestScenario(
            scenario_id="S3",
            mode=NetworkMode.TODAY,
            scenario_type="Contradictory",
            description="Today Mode: Advisory contradiction - Tanah Merah both open and closed",
            facts=[
                "StationClosed_TanahMerah",
                "StationOpen_TanahMerah",
            ],
            query="AdvisoryContradiction",
            expected_result=True,
            expected_violated_rules=["R15"],
            explanation="Contradictory advisories: Tanah Merah cannot be both open and closed (R15)"
        ),
        
        TestScenario(
            scenario_id="S4",
            mode=NetworkMode.TODAY,
            scenario_type="Invalid",
            description="Today Mode: Tanah Merah-Expo segment closed - route invalid",
            facts=[
                "SegmentClosed_TanahMerahExpo",
                "RouteUsesSegment_TanahMerahExpo",
            ],
            query="RouteInvalid",
            expected_result=True,
            expected_violated_rules=["R5", "R6"],
            explanation="Segment closed (R5 → CannotTravel), route uses it (R6 → RouteInvalid)"
        ),
        
        TestScenario(
            scenario_id="S5",
            mode=NetworkMode.TODAY,
            scenario_type="Invalid",
            description="Today Mode: Systems integration work causes station closure",
            facts=[
                "StationUnderIntegration_Expo",
                "RouteIncludesExpo",
            ],
            query="RouteInvalid",
            expected_result=True,
            expected_violated_rules=["R3", "R1", "R4"],
            explanation="Expo under integration (R3 → StationClosed), then R1 → CannotBoard, R4 → RouteInvalid"
        ),
        
        # ========== FUTURE MODE SCENARIOS ==========
        TestScenario(
            scenario_id="S6",
            mode=NetworkMode.FUTURE,
            scenario_type="Valid",
            description="Future Mode: TELe operational, T5 accessible",
            facts=[
                "FutureMode",
                "StationOpen_T5Interchange",
                "StationOpen_TanahMerah",
            ],
            query="RouteInvalid",
            expected_result=False,
            explanation="In Future Mode, TEL extension is operational. No violations, route is valid."
        ),
        
        TestScenario(
            scenario_id="S7",
            mode=NetworkMode.FUTURE,
            scenario_type="Invalid",
            description="Future Mode: EWL segment converted to TEL - old EWL route invalid",
            facts=[
                "FutureMode",
                "EWLSegmentConverted_TanahMerahChangiAirport",
                "RouteUsesEWL_TanahMerahChangiAirport",
            ],
            query="RouteInvalid",
            expected_result=True,
            expected_violated_rules=["R13", "R14"],
            explanation="Segment converted to TEL (R13 → NotOnEWL), old EWL routes invalid (R14)"
        ),
        
        TestScenario(
            scenario_id="S8",
            mode=NetworkMode.FUTURE,
            scenario_type="Invalid",
            description="Future Mode: Systems work + peak hour = high crowding risk",
            facts=[
                "SystemsWork_ExpoChangiAirport",
                "PeakHour",
            ],
            query="HighCrowdingRisk_ExpoChangiAirport",
            expected_result=True,
            expected_violated_rules=["R7", "R8"],
            explanation="Systems work causes reduced service (R7), during peak creates crowding (R8)"
        ),
        
        TestScenario(
            scenario_id="S9",
            mode=NetworkMode.FUTURE,
            scenario_type="Invalid",
            description="Future Mode: Closed interchange prevents transfer",
            facts=[
                "StationClosed_TanahMerah",
                "TanahMerahIsInterchange",
                "TransferAtTanahMerah",
            ],
            query="RouteInvalid",
            expected_result=True,
            expected_violated_rules=["R11"],
            explanation="Transfer at closed interchange station (R11 → RouteInvalid)"
        ),
        
        TestScenario(
            scenario_id="S10",
            mode=NetworkMode.TODAY,
            scenario_type="Contradictory",
            description="Today Mode: Segment both open and closed - contradiction",
            facts=[
                "SegmentClosed_TanahMerahExpo",
                "SegmentOpen_TanahMerahExpo",
            ],
            query="AdvisoryContradiction",
            expected_result=True,
            expected_violated_rules=["R16"],
            explanation="Tanah Merah-Expo segment cannot be both open and closed (R16)"
        ),
    ]
    
    return scenarios