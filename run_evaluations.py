#!/usr/bin/env python3
"""
Standalone script to run VaultGemma evaluations without module import issues.
"""

import sys
import argparse
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import directly to avoid circular import warnings
from evals.base_evaluator import EvaluationSummary
from evals.business_evaluator import BusinessEvaluator
from evals.intent_evaluator import IntentEvaluator
from evals.sentiment_evaluator import SentimentEvaluator
from evals.entity_evaluator import EntityEvaluator


class StandaloneEvaluationRunner:
    """Standalone runner for executing all evaluation tests."""
    
    def __init__(self, model_name: str = "google/vaultgemma-1b", output_dir: str = "eval_results"):
        """Initialize the evaluation runner.
        
        Args:
            model_name: Name of the model to evaluate
            output_dir: Directory to save evaluation results
        """
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize evaluators
        self.evaluators = {
            'business': BusinessEvaluator(model_name=model_name),
            'intent': IntentEvaluator(model_name=model_name),
            'sentiment': SentimentEvaluator(model_name=model_name),
            'entity': EntityEvaluator(model_name=model_name)
        }
    
    def run_all_evaluations(self):
        """Run all evaluation tests."""
        print("🚀 VaultGemma Comprehensive Evaluation Suite")
        print("=" * 60)
        print(f"Model: {self.model_name}")
        print(f"Output Directory: {self.output_dir}")
        print("=" * 60)
        
        results = {}
        
        for evaluator_name, evaluator in self.evaluators.items():
            print(f"\n🔄 Running {evaluator_name.upper()} evaluation...")
            print("-" * 40)
            
            try:
                summary = evaluator.run_evaluation()
                results[evaluator_name] = summary
                
                # Save individual results
                self._save_evaluator_results(evaluator_name, summary)
                
            except Exception as e:
                print(f"❌ Error running {evaluator_name} evaluation: {e}")
                results[evaluator_name] = None
        
        # Generate overall summary
        self._generate_overall_summary(results)
        
        return results
    
    def run_specific_evaluation(self, evaluator_name: str):
        """Run a specific evaluation."""
        if evaluator_name not in self.evaluators:
            raise ValueError(f"Unknown evaluator: {evaluator_name}. Available: {list(self.evaluators.keys())}")
        
        print(f"🚀 Running {evaluator_name.upper()} evaluation")
        print("=" * 40)
        
        evaluator = self.evaluators[evaluator_name]
        summary = evaluator.run_evaluation()
        
        # Save results
        self._save_evaluator_results(evaluator_name, summary)
        
        return summary
    
    def _save_evaluator_results(self, evaluator_name: str, summary: EvaluationSummary):
        """Save results for a specific evaluator."""
        import json
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"{evaluator_name}_results_{timestamp}.json"
        
        # Convert to serializable format
        data = {
            "evaluator": evaluator_name,
            "model_name": self.model_name,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": summary.total_tests,
                "passed_tests": summary.passed_tests,
                "failed_tests": summary.failed_tests,
                "average_score": summary.average_score,
                "total_execution_time": summary.total_execution_time
            },
            "results": [
                {
                    "test_name": r.test_name,
                    "prompt": r.prompt,
                    "expected_output": r.expected_output,
                    "actual_output": r.actual_output,
                    "score": r.score,
                    "metrics": r.metrics,
                    "execution_time": r.execution_time,
                    "timestamp": r.timestamp,
                    "passed": r.passed
                }
                for r in summary.results
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 {evaluator_name.title()} results saved to: {filename}")
    
    def _generate_overall_summary(self, results):
        """Generate overall summary of all evaluations."""
        print("\n" + "=" * 60)
        print("📊 OVERALL EVALUATION SUMMARY")
        print("=" * 60)
        
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_execution_time = 0.0
        weighted_scores = []
        
        for evaluator_name, summary in results.items():
            if summary is None:
                print(f"❌ {evaluator_name.upper()}: FAILED TO RUN")
                continue
            
            total_tests += summary.total_tests
            total_passed += summary.passed_tests
            total_failed += summary.failed_tests
            total_execution_time += summary.total_execution_time
            
            # Weight scores by number of tests
            weighted_scores.append(summary.average_score * summary.total_tests)
            
            status = "✅ PASSED" if summary.passed_tests > summary.failed_tests else "❌ FAILED"
            print(f"{evaluator_name.upper():12} | {status:8} | Tests: {summary.total_tests:2d} | Score: {summary.average_score:.2f} | Time: {summary.total_execution_time:.1f}s")
        
        if total_tests > 0:
            overall_score = sum(weighted_scores) / total_tests
            pass_rate = (total_passed / total_tests) * 100
            
            print("-" * 60)
            print(f"TOTAL        | Tests: {total_tests:2d} | Passed: {total_passed:2d} ({pass_rate:.1f}%) | Score: {overall_score:.2f} | Time: {total_execution_time:.1f}s")
            print("=" * 60)


def main():
    """Main entry point for the evaluation runner."""
    parser = argparse.ArgumentParser(description="Run VaultGemma evaluation tests")
    parser.add_argument(
        "--model", 
        default="google/vaultgemma-1b",
        help="Model name to evaluate (default: google/vaultgemma-1b)"
    )
    parser.add_argument(
        "--evaluator",
        choices=['business', 'intent', 'sentiment', 'entity', 'all'],
        default='all',
        help="Specific evaluator to run (default: all)"
    )
    parser.add_argument(
        "--output-dir",
        default="eval_results",
        help="Output directory for results (default: eval_results)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=300,
        help="Maximum tokens to generate (default: 300)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature (default: 0.7)"
    )
    
    args = parser.parse_args()
    
    # Initialize runner
    runner = StandaloneEvaluationRunner(
        model_name=args.model,
        output_dir=args.output_dir
    )
    
    # Update evaluator configurations
    for evaluator in runner.evaluators.values():
        evaluator.max_tokens = args.max_tokens
        evaluator.temperature = args.temperature
    
    try:
        if args.evaluator == 'all':
            results = runner.run_all_evaluations()
        else:
            summary = runner.run_specific_evaluation(args.evaluator)
            results = {args.evaluator: summary}
        
        print("\n🎉 Evaluation completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Evaluation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Evaluation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
