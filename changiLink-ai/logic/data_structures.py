from typing import List, Set, FrozenSet
from dataclasses import dataclass
from enum import Enum


class NetworkMode(Enum):
    """Network operation modes"""
    TODAY = "Today"
    FUTURE = "Future"


class RuleCategory(Enum):
    """Categories of logical rules"""
    STATION_OPERATION = "Station Operation"
    SEGMENT_OPERATION = "Segment Operation"
    LINE_OPERATION = "Line Operation"
    TRANSFER_RULES = "Transfer Rules"
    MODE_SPECIFIC = "Mode-Specific Rules"
    ADVISORY_CONSISTENCY = "Advisory Consistency"


@dataclass(frozen=True)
class Literal:
    """
    Represents a propositional literal: an atomic proposition with optional negation
    Examples: StationClosed_Expo, CannotBoard_TanahMerah, RouteInvalid"""
    proposition: str  # e.g., "StationClosed_Expo", "RouteInvalid"
    negated: bool = False
    
    def __str__(self):
        return f"¬{self.proposition}" if self.negated else self.proposition
    
    def negate(self) -> 'Literal':
        """Return the negation of this literal"""
        return Literal(self.proposition, not self.negated)
    
    def is_complementary(self, other: 'Literal') -> bool:
        """Check if this literal is the complement of another (p and ¬p)"""
        return (self.proposition == other.proposition and
                self.negated != other.negated)


@dataclass
class Clause:
    """Represents a clause: a disjunction of literals (L1 ∨ L2 ∨ ... ∨ Ln)"""
    literals: FrozenSet[Literal]
    source_rule: str = ""
    derivation: str = ""  # How this clause was derived
    
    def __init__(self, literals: List[Literal], source_rule: str = "", derivation: str = ""):
        self.literals = frozenset(literals)
        self.source_rule = source_rule
        self.derivation = derivation if derivation else source_rule
    
    def __str__(self):
        if not self.literals:
            return "□"  # Empty clause (contradiction)
        if len(self.literals) == 1:
            return str(list(self.literals)[0])
        return "(" + " ∨ ".join(str(lit) for lit in sorted(self.literals, key=str)) + ")"
    
    def __eq__(self, other):
        if not isinstance(other, Clause):
            return False
        return self.literals == other.literals
    
    def __hash__(self):
        return hash(self.literals)
    
    def is_empty(self) -> bool:
        """Check if this is the empty clause (contradiction)"""
        return len(self.literals) == 0
    
    def is_tautology(self) -> bool:
        """Check if clause contains both L and ¬L (always true)"""
        for lit in self.literals:
            if lit.negate() in self.literals:
                return True
        return False


@dataclass
class PropositionalRule:
    """
    Represents a propositional logic rule in implication format: P1 ∧ P2 ∧ ... → C
    """
    rule_id: str
    premises: List[str]  # List of proposition names
    conclusion: str  # Proposition name
    description: str
    category: RuleCategory
    
    def to_cnf_clause(self) -> Clause:
        """
        Convert implication to CNF.
        P1 ∧ P2 → C  becomes  ¬P1 ∨ ¬P2 ∨ C
        """
        literals = []
        
        # Add negated premises
        for premise in self.premises:
            lit = Literal(premise, negated=False)
            literals.append(lit.negate())
        
        # Add conclusion
        lit = Literal(self.conclusion, negated=False)
        literals.append(lit)
        
        return Clause(literals, self.rule_id)
    
    def __str__(self):
        if len(self.premises) == 1:
            premises_str = self.premises[0]
        else:
            premises_str = "(" + " ∧ ".join(self.premises) + ")"
        return f"{self.rule_id}: {premises_str} → {self.conclusion}"


@dataclass
class ResolutionStep:
    """Records a single resolution step"""
    step_num: int
    clause1: Clause
    clause2: Clause
    resolvent: Clause
    resolved_literal: str  # Which literal was resolved
    description: str