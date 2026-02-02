from mrt_inference_system import MRTInferenceSystem


def main():
    """Main execution function"""
    system = MRTInferenceSystem()
    
    # Print all rules with CNF conversion
    print("\n" + "="*80)
    print("STEP 1: Display Propositional Logic Rules and CNF Conversion")
    print("="*80)
    system.print_rules()
    
    # Run all scenarios
    print("\n" + "="*80)
    print("STEP 2: Run Test Scenarios with Propositional Resolution-Based Inference")
    print("="*80)
    results = system.run_all_scenarios(verbose=True)
    


if __name__ == "__main__":
    main()