from typing import List, Dict
from collections import defaultdict
from data_structures import RuleCategory, NetworkMode
from rules import create_mrt_rules
from scenarios import create_test_scenarios, TestScenario
from resolution_engine import PropositionalResolutionEngine


class MRTInferenceSystem:
    """Main system for testing propositional resolution-based logical inference"""
    
    def __init__(self):
        self.rules = create_mrt_rules()
        self.scenarios = create_test_scenarios()
        print(f"\n{'='*80}")
        print(f"MRT LOGICAL INFERENCE SYSTEM (Propositional Resolution)")
        print(f"{'='*80}")
        print(f"Logic Type: PROPOSITIONAL LOGIC (no variables)")
        print(f"Initialized with {len(self.rules)} propositional rules and {len(self.scenarios)} scenarios")
        print(f"{'='*80}\n")
    
    def run_scenario(self, scenario: TestScenario, verbose: bool = True) -> Dict:
        """Run a single test scenario"""
        if verbose:
            print(f"\n{'='*80}")
            print(f"SCENARIO {scenario.scenario_id}: {scenario.description}")
            print(f"{'='*80}")
            print(f"Mode: {scenario.mode.value} | Type: {scenario.scenario_type}")
            print(f"{'-'*80}")
        
        # Create resolution engine
        engine = PropositionalResolutionEngine(self.rules)
        engine.add_facts(scenario.facts)
        
        # Display facts
        if verbose:
            print(f"\nGIVEN FACTS (Propositional):")
            for i, fact in enumerate(scenario.facts, 1):
                print(f"   {i}. {fact}")
        
        # Check consistency
        consistent, consistency_msg, contradictions = engine.check_consistency()
        if verbose:
            print(f"\nKNOWLEDGE BASE CONSISTENCY:")
            print(f"   Status: {'✓ Consistent' if consistent else '✗ INCONSISTENT'}")
            if contradictions:
                print(f"   Contradictions:")
                for c in contradictions:
                    print(f"   - {c}")
        
        # Query using resolution
        if verbose:
            print(f"\nQUERY: {scenario.query}")
        
        proven, explanation = engine.prove(scenario.query)
        
        if verbose:
            
            print(f"\nRESOLUTION RESULT:")
            print(f"   {explanation}")
            print(f"   Query {scenario.query}: {'PROVEN ✓' if proven else 'NOT PROVEN ✗'}")
            
            # Show resolution steps (first 10)
            if engine.resolution_steps:
                print(f"\nRESOLUTION STEPS (showing first 10 of {len(engine.resolution_steps)}):")
                for step in engine.resolution_steps[:10]:
                    print(f"   {step.step_num}. {step.description}")
                    print(f"      Resolvent: {step.resolvent}")
            
            # Show violated rules
            if engine.violated_rules:
                print(f"\nRULES VIOLATED:")
                for rule_id in engine.violated_rules:
                    rule = next(r for r in self.rules if r.rule_id == rule_id)
                    print(f"   - {rule_id}: {rule.description}")
        
        # Compare with expected
        test_passed = (proven == scenario.expected_result)
        
        result = {
            'scenario_id': scenario.scenario_id,
            'mode': scenario.mode.value,
            'type': scenario.scenario_type,
            'description': scenario.description,
            'proven': proven,
            'expected': scenario.expected_result,
            'consistent': consistent,
            'test_passed': test_passed,
            'violated_rules': engine.violated_rules,
            'num_steps': len(engine.resolution_steps)
        }
        
        if verbose:
            print(f"\n{'─'*80}")
            print(f"TEST RESULT:")
            print(f"   Expected: {scenario.expected_result} | Actual: {proven}")
            status = "✓ PASS" if test_passed else "✗ FAIL"
            print(f"   Status: {status}")
            if scenario.explanation:
                print(f"\nEXPLANATION:")
                print(f"   {scenario.explanation}")
            print(f"{'─'*80}")
        
        return result
    
    def run_all_scenarios(self, verbose: bool = True) -> List[Dict]:
        """Run all test scenarios"""
        results = []
        for scenario in self.scenarios:
            result = self.run_scenario(scenario, verbose=verbose)
            results.append(result)
        
        # Print summary
        self.print_summary(results)
        return results
    
    def print_summary(self, results: List[Dict]):
        """Print comprehensive test summary"""
        print(f"\n{'='*80}")
        print(f"TEST SUMMARY")
        print(f"{'='*80}")
        
        total = len(results)
        passed = sum(1 for r in results if r['test_passed'])
        
        print(f"\nOverall Results:")
        print(f"  Total Scenarios: {total}")
        print(f"  Passed: {passed} ✓")
        print(f"  Failed: {total - passed} ✗")
        print(f"  Success Rate: {passed/total*100:.1f}%")
        
        # Group by mode
        today_results = [r for r in results if r['mode'] == NetworkMode.TODAY.value]
        future_results = [r for r in results if r['mode'] == NetworkMode.FUTURE.value]
        
        print(f"\nResults by Network Mode:")
        print(f"  Today Mode: {sum(1 for r in today_results if r['test_passed'])}/{len(today_results)} passed")
        print(f"  Future Mode: {sum(1 for r in future_results if r['test_passed'])}/{len(future_results)} passed")
        
        # Detailed results table
        print(f"\n{'─'*80}")
        print(f"{'ID':<6} {'Mode':<10} {'Type':<15} {'Result':<12} {'Status':<8}")
        print(f"{'─'*80}")
        for r in results:
            status = '✓ PASS' if r['test_passed'] else '✗ FAIL'
            result_str = 'Proven' if r['proven'] else 'Not Proven'
            print(f"{r['scenario_id']:<6} {r['mode']:<10} {r['type']:<15} {result_str:<12} {status:<8}")
        print(f"{'='*80}\n")
    
    def print_rules(self):
        """Print all propositional rules with CNF conversion"""
        print(f"\n{'='*80}")
        print(f"PROPOSITIONAL LOGIC RULES ({len(self.rules)} total)")
        print(f"{'='*80}")
        print(f"\nIMPORTANT: Uses PROPOSITIONAL LOGIC (not first-order logic)")
        print(f"   - No variables (X, Y, L)")
        print(f"   - Only concrete propositions (StationClosed_Expo, RouteInvalid, etc.)")
        print(f"   - Each rule is specific to particular stations/segments")
        print(f"\nThese rules cover the LTA (25 Jul 2025) TELe/CRL announcement:")
        print(f"- TELe extension: Sungei Bedok → T5 → Tanah Merah")
        print(f"- EWL segment conversion: Tanah Merah-Expo-Changi Airport → TEL systems")
        print(f"- Systems integration work requirements")
        print(f"- CRL extension to T5")
        
        # Group by category
        rules_by_category = defaultdict(list)
        for rule in self.rules:
            rules_by_category[rule.category].append(rule)
        
        for category in RuleCategory:
            category_rules = rules_by_category[category]
            if category_rules:
                print(f"\n{'-'*80}")
                print(f"{category.value}:")
                print(f"{'-'*80}")
                for rule in category_rules:
                    print(f"\n  {rule}")
                    print(f" {rule.description}")
                    cnf = rule.to_cnf_clause()
                    print(f"  CNF: {cnf}")
        
        print(f"\n{'='*80}\n")
    
