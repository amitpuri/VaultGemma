#!/usr/bin/env python3
"""
Example script demonstrating how to use the VaultGemma evaluation framework.
"""

import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import directly to avoid circular import issues
from evals.business_evaluator import BusinessEvaluator
from evals.intent_evaluator import IntentEvaluator
from evals.sentiment_evaluator import SentimentEvaluator
from evals.entity_evaluator import EntityEvaluator
from evals.evaluation_runner import EvaluationRunner


def run_business_evaluation():
    """Example: Run business evaluation only."""
    print("🚀 Running Business Evaluation Example")
    print("=" * 50)
    
    evaluator = BusinessEvaluator(
        model_name="google/vaultgemma-1b",
        max_tokens=400,
        temperature=0.8
    )
    
    summary = evaluator.run_evaluation()
    
    print(f"\n📊 Business Evaluation Results:")
    print(f"Total Tests: {summary.total_tests}")
    print(f"Passed: {summary.passed_tests}")
    print(f"Failed: {summary.failed_tests}")
    print(f"Average Score: {summary.average_score:.2f}")
    
    return summary


def run_intent_evaluation():
    """Example: Run intent recognition evaluation only."""
    print("\n🚀 Running Intent Recognition Evaluation Example")
    print("=" * 50)
    
    evaluator = IntentEvaluator(
        model_name="google/vaultgemma-1b",
        max_tokens=300,
        temperature=0.7
    )
    
    summary = evaluator.run_evaluation()
    
    print(f"\n📊 Intent Recognition Results:")
    print(f"Total Tests: {summary.total_tests}")
    print(f"Passed: {summary.passed_tests}")
    print(f"Failed: {summary.failed_tests}")
    print(f"Average Score: {summary.average_score:.2f}")
    
    return summary


def run_sentiment_evaluation():
    """Example: Run sentiment analysis evaluation only."""
    print("\n🚀 Running Sentiment Analysis Evaluation Example")
    print("=" * 50)
    
    evaluator = SentimentEvaluator(
        model_name="google/vaultgemma-1b",
        max_tokens=250,
        temperature=0.6
    )
    
    summary = evaluator.run_evaluation()
    
    print(f"\n📊 Sentiment Analysis Results:")
    print(f"Total Tests: {summary.total_tests}")
    print(f"Passed: {summary.passed_tests}")
    print(f"Failed: {summary.failed_tests}")
    print(f"Average Score: {summary.average_score:.2f}")
    
    return summary


def run_entity_evaluation():
    """Example: Run entity extraction evaluation only."""
    print("\n🚀 Running Entity Extraction Evaluation Example")
    print("=" * 50)
    
    evaluator = EntityEvaluator(
        model_name="google/vaultgemma-1b",
        max_tokens=350,
        temperature=0.7
    )
    
    summary = evaluator.run_evaluation()
    
    print(f"\n📊 Entity Extraction Results:")
    print(f"Total Tests: {summary.total_tests}")
    print(f"Passed: {summary.passed_tests}")
    print(f"Failed: {summary.failed_tests}")
    print(f"Average Score: {summary.average_score:.2f}")
    
    return summary


def run_comprehensive_evaluation():
    """Example: Run all evaluations using the runner."""
    print("\n🚀 Running Comprehensive Evaluation Example")
    print("=" * 50)
    
    runner = EvaluationRunner(
        model_name="google/vaultgemma-1b",
        output_dir="example_results"
    )
    
    # Update evaluator configurations
    for evaluator in runner.evaluators.values():
        evaluator.max_tokens = 300
        evaluator.temperature = 0.7
    
    results = runner.run_all_evaluations()
    
    print(f"\n📊 Comprehensive Evaluation Results:")
    for evaluator_name, summary in results.items():
        if summary:
            print(f"{evaluator_name.title()}: {summary.average_score:.2f} score, {summary.passed_tests}/{summary.total_tests} passed")
        else:
            print(f"{evaluator_name.title()}: Failed to run")
    
    return results


def run_custom_business_test():
    """Example: Run a custom business test case."""
    print("\n🚀 Running Custom Business Test Example")
    print("=" * 50)
    
    class CustomBusinessEvaluator(BusinessEvaluator):
        def get_test_cases(self):
            return [
                {
                    "name": "custom_startup_scenario",
                    "prompt": "I'm starting a tech startup with $100,000 in funding. We're building a SaaS product for small businesses. What should be my top 3 priorities for the first 6 months?",
                    "expected_output": None
                },
                {
                    "name": "custom_remote_work",
                    "prompt": "Our company of 50 employees is transitioning to fully remote work. What are the key challenges and solutions I should consider?",
                    "expected_output": None
                }
            ]
    
    evaluator = CustomBusinessEvaluator(
        model_name="google/vaultgemma-1b",
        max_tokens=400,
        temperature=0.8
    )
    
    summary = evaluator.run_evaluation()
    
    print(f"\n📊 Custom Business Test Results:")
    print(f"Total Tests: {summary.total_tests}")
    print(f"Passed: {summary.passed_tests}")
    print(f"Average Score: {summary.average_score:.2f}")
    
    # Show detailed results
    for result in summary.results:
        print(f"\nTest: {result.test_name}")
        print(f"Score: {result.score:.2f}")
        print(f"Passed: {result.passed}")
        print(f"Response: {result.actual_output[:100]}...")
    
    return summary


def main():
    """Main function to run examples."""
    print("🎯 VaultGemma Evaluation Framework Examples")
    print("=" * 60)
    
    try:
        # Example 1: Individual evaluators
        print("\n1️⃣ Running Individual Evaluators")
        business_summary = run_business_evaluation()
        intent_summary = run_intent_evaluation()
        sentiment_summary = run_sentiment_evaluation()
        entity_summary = run_entity_evaluation()
        
        # Example 2: Comprehensive evaluation
        print("\n2️⃣ Running Comprehensive Evaluation")
        comprehensive_results = run_comprehensive_evaluation()
        
        # Example 3: Custom test cases
        print("\n3️⃣ Running Custom Test Cases")
        custom_summary = run_custom_business_test()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
        print(f"Business Evaluation: {business_summary.average_score:.2f}")
        print(f"Intent Recognition: {intent_summary.average_score:.2f}")
        print(f"Sentiment Analysis: {sentiment_summary.average_score:.2f}")
        print(f"Entity Extraction: {entity_summary.average_score:.2f}")
        print(f"Custom Business Test: {custom_summary.average_score:.2f}")
        
        print("\n💾 Check the 'example_results' directory for detailed JSON reports")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
