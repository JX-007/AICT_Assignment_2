from typing import List, Tuple, Set, Optional
from itertools import combinations
from data_structures import Literal, Clause, PropositionalRule, ResolutionStep


class PropositionalResolutionEngine:
    """
    Implements resolution-based inference for PROPOSITIONAL LOGIC.
    
    Resolution is a refutation-based proof technique:
    1. Convert knowledge base to CNF clauses
    2. Negate the query and add to clause set
    3. Repeatedly apply resolution rule: if C1 contains p and C2 contains ¬p, resolve them
    4. If empty clause (□) is derived, query is proven
    """
    
    def __init__(self, rules: List[PropositionalRule]):
        self.rules = rules
        self.clauses: Set[Clause] = set()
        self.facts: Set[Clause] = set()
        self.resolution_steps: List[ResolutionStep] = []
        self.violated_rules: List[str] = []
        
    def add_facts(self, fact_strings: List[str]):
        """Convert fact strings to unit clauses and add to knowledge base"""
        for fact_str in fact_strings:
            lit = self._parse_literal(fact_str)
            clause = Clause([lit], source_rule="FACT")
            self.facts.add(clause)
            self.clauses.add(clause)
    
    def reset(self):
        """Reset the engine for a new inference"""
        self.clauses = set()
        self.facts = set()
        self.resolution_steps = []
        self.violated_rules = []
    
    def _parse_literal(self, text: str) -> Literal:
        """
        Parse a propositional literal string.
        Examples: 'StationClosed_Expo', '¬RouteInvalid'
        """
        negated = text.startswith('¬')
        if negated:
            text = text[1:]
        
        return Literal(text, negated)
    
    def prove(self, query_str: str, max_iterations: int = 100) -> Tuple[bool, str]:
        """
        Prove a query using resolution refutation.
        
        Returns: (proven: bool, explanation: str)
        """
        # Initialize clause set with rules converted to CNF
        self.clauses = self.facts.copy()
        for rule in self.rules:
            cnf_clause = rule.to_cnf_clause()
            self.clauses.add(cnf_clause)
        
        # Parse and negate the query
        query_lit = self._parse_literal(query_str)
        negated_query = Clause([query_lit.negate()], source_rule="NEGATED_QUERY")
        self.clauses.add(negated_query)
        
        # Apply resolution repeatedly
        new_clauses = set()
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            clause_pairs = list(combinations(self.clauses, 2))
            
            for c1, c2 in clause_pairs:
                resolvents = self._resolve(c1, c2)
                
                for resolvent in resolvents:
                    # Check if we derived the empty clause
                    if resolvent.is_empty():
                        return True, f"Proven by resolution (found contradiction in {len(self.resolution_steps)} steps)"
                    
                    # Skip tautologies
                    if not resolvent.is_tautology():
                        # Check if this is a new clause
                        if resolvent not in self.clauses and resolvent not in new_clauses:
                            new_clauses.add(resolvent)
                            
                            # Track violated rules
                            if self._is_violation_clause(resolvent):
                                for clause in [c1, c2]:
                                    if clause.source_rule and clause.source_rule not in ["FACT", "NEGATED_QUERY"]:
                                        if clause.source_rule not in self.violated_rules:
                                            self.violated_rules.append(clause.source_rule)
            
            # If no new clauses, we cannot prove the query
            if not new_clauses:
                return False, "Cannot prove (resolution saturated without finding contradiction)"
            
            # Add new clauses to the set
            self.clauses.update(new_clauses)
            new_clauses.clear()
        
        return False, f"Cannot prove (reached max iterations: {max_iterations})"
    
    def _resolve(self, c1: Clause, c2: Clause) -> List[Clause]:
        """
        Apply resolution rule to two clauses.
        In propositional logic: if c1 contains p and c2 contains ¬p, resolve them.
        
        """
        resolvents = []
        
        # Try to find complementary literals (p and ¬p)
        for lit1 in c1.literals:
            for lit2 in c2.literals:
                # Check if they are complementary (one is negation of the other)
                if lit1.is_complementary(lit2):
                    # Create resolvent: (c1 - {lit1}) ∪ (c2 - {lit2})
                    remaining1 = [l for l in c1.literals if l != lit1]
                    remaining2 = [l for l in c2.literals if l != lit2]
                    
                    # Combine literals
                    resolvent_literals = remaining1 + remaining2
                    
                    # Create resolvent clause
                    derivation = f"Res({c1.source_rule},{c2.source_rule})"
                    resolvent = Clause(resolvent_literals, source_rule="", derivation=derivation)
                    
                    # Record resolution step
                    step = ResolutionStep(
                        step_num=len(self.resolution_steps) + 1,
                        clause1=c1,
                        clause2=c2,
                        resolvent=resolvent,
                        resolved_literal=lit1.proposition,
                        description=f"Resolved {lit1} with {lit2}"
                    )
                    self.resolution_steps.append(step)
                    
                    resolvents.append(resolvent)
        
        return resolvents
    
    def _is_violation_clause(self, clause: Clause) -> bool:
        """Check if a clause represents a violation"""
        for lit in clause.literals:
            if any(keyword in lit.proposition for keyword in 
                   ["RouteInvalid", "AdvisoryContradiction", "CannotBoard", 
                    "CannotTravel", "HighCrowdingRisk"]) and not lit.negated:
                return True
        return False
    
    def check_consistency(self) -> Tuple[bool, str, List[str]]:
        """Check if the knowledge base is consistent"""
        # Initialize clauses
        self.clauses = self.facts.copy()
        for rule in self.rules:
            self.clauses.add(rule.to_cnf_clause())
        
        # Look for direct contradictions (p and ¬p both as facts)
        contradictions = []
        literals_seen = set()
        
        for clause in self.clauses:
            if clause.source_rule == "FACT":
                for lit in clause.literals:
                    if lit.negate() in literals_seen:
                        contradictions.append(f"Contradiction: {lit} and {lit.negate()}")
                    literals_seen.add(lit)
        
        if contradictions:
            return False, "Knowledge base contains contradictions", contradictions
        
        return True, "Knowledge base is consistent", []