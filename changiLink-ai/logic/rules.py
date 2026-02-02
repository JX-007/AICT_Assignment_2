from typing import List
from data_structures import PropositionalRule, RuleCategory


def create_mrt_rules() -> List[PropositionalRule]:
    """
    Define propositional logic rules for the MRT system.
    
    These rules cover the LTA (25 Jul 2025) TELe/CRL changes:
    - TELe extension from Sungei Bedok to T5 to Tanah Merah
    - Conversion of Tanah Merah-Expo-Changi Airport to TEL systems
    - Systems integration work requirements
    - CRL extension to T5
    
    Total: 16 propositional rules
    """
    rules = [
        # ========== STATION OPERATION RULES (R1-R4) ==========
        PropositionalRule(
            rule_id="R1",
            premises=["StationClosed_Expo"],
            conclusion="CannotBoard_Expo",
            description="If Expo station is closed, passengers cannot board at Expo",
            category=RuleCategory.STATION_OPERATION
        ),
        PropositionalRule(
            rule_id="R2",
            premises=["StationClosed_TanahMerah"],
            conclusion="CannotBoard_TanahMerah",
            description="If Tanah Merah station is closed, passengers cannot board there",
            category=RuleCategory.STATION_OPERATION
        ),
        PropositionalRule(
            rule_id="R3",
            premises=["StationUnderIntegration_Expo"],
            conclusion="StationClosed_Expo",
            description="Expo under systems integration work is considered closed",
            category=RuleCategory.STATION_OPERATION
        ),
        PropositionalRule(
            rule_id="R4",
            premises=["CannotBoard_Expo", "RouteIncludesExpo"],
            conclusion="RouteInvalid",
            description="Route including Expo when boarding not allowed is invalid",
            category=RuleCategory.STATION_OPERATION
        ),
        
        # ========== SEGMENT OPERATION RULES (R5-R8) ==========
        PropositionalRule(
            rule_id="R5",
            premises=["SegmentClosed_TanahMerahExpo"],
            conclusion="CannotTravel_TanahMerahExpo",
            description="If Tanah Merah-Expo segment is closed, cannot travel directly",
            category=RuleCategory.SEGMENT_OPERATION
        ),
        PropositionalRule(
            rule_id="R6",
            premises=["CannotTravel_TanahMerahExpo", "RouteUsesSegment_TanahMerahExpo"],
            conclusion="RouteInvalid",
            description="Route using closed Tanah Merah-Expo segment is invalid",
            category=RuleCategory.SEGMENT_OPERATION
        ),
        PropositionalRule(
            rule_id="R7",
            premises=["SystemsWork_ExpoChangiAirport"],
            conclusion="SegmentReduced_ExpoChangiAirport",
            description="Systems work on Expo-Changi Airport causes reduced service",
            category=RuleCategory.SEGMENT_OPERATION
        ),
        PropositionalRule(
            rule_id="R8",
            premises=["SegmentReduced_ExpoChangiAirport", "PeakHour"],
            conclusion="HighCrowdingRisk_ExpoChangiAirport",
            description="Reduced service during peak hours creates high crowding risk",
            category=RuleCategory.SEGMENT_OPERATION
        ),
        
        # ========== LINE OPERATION RULES (R9-R10) ==========
        PropositionalRule(
            rule_id="R9",
            premises=["LineNotOperational_EWL", "ExpoOnlyOnEWL"],
            conclusion="CannotBoard_Expo",
            description="If EWL not operational and Expo only on EWL, cannot board at Expo",
            category=RuleCategory.LINE_OPERATION
        ),
        PropositionalRule(
            rule_id="R10",
            premises=["LineDisrupted_EWL", "RouteUsesEWL"],
            conclusion="RouteUnreliable",
            description="Routes using disrupted EWL are unreliable",
            category=RuleCategory.LINE_OPERATION
        ),
        
        # ========== TRANSFER RULES (R11-R12) ==========
        PropositionalRule(
            rule_id="R11",
            premises=["StationClosed_TanahMerah", "TanahMerahIsInterchange", "TransferAtTanahMerah"],
            conclusion="RouteInvalid",
            description="Routes requiring transfer at closed Tanah Merah interchange are invalid",
            category=RuleCategory.TRANSFER_RULES
        ),
        PropositionalRule(
            rule_id="R12",
            premises=["LineNotOperational_EWL", "TransferRequiresEWL"],
            conclusion="TransferNotPossible",
            description="Cannot transfer if EWL not operational and transfer requires it",
            category=RuleCategory.TRANSFER_RULES
        ),
        
        # ========== MODE-SPECIFIC RULES (R13-R14) ==========
        PropositionalRule(
            rule_id="R13",
            premises=["FutureMode", "EWLSegmentConverted_TanahMerahChangiAirport"],
            conclusion="NotOnEWL_TanahMerahChangiAirport",
            description="In Future Mode, Tanah Merah-Changi Airport converted to TEL (no longer EWL)",
            category=RuleCategory.MODE_SPECIFIC
        ),
        PropositionalRule(
            rule_id="R14",
            premises=["FutureMode", "NotOnEWL_TanahMerahChangiAirport", "RouteUsesEWL_TanahMerahChangiAirport"],
            conclusion="RouteInvalid",
            description="Future Mode routes cannot use segments no longer on EWL",
            category=RuleCategory.MODE_SPECIFIC
        ),
        
        # ========== ADVISORY CONSISTENCY RULES (R15-R16) ==========
        PropositionalRule(
            rule_id="R15",
            premises=["StationClosed_TanahMerah", "StationOpen_TanahMerah"],
            conclusion="AdvisoryContradiction",
            description="Tanah Merah cannot be both open and closed simultaneously",
            category=RuleCategory.ADVISORY_CONSISTENCY
        ),
        PropositionalRule(
            rule_id="R16",
            premises=["SegmentClosed_TanahMerahExpo", "SegmentOpen_TanahMerahExpo"],
            conclusion="AdvisoryContradiction",
            description="Tanah Merah-Expo segment cannot be both open and closed",
            category=RuleCategory.ADVISORY_CONSISTENCY
        ),
    ]
    
    return rules