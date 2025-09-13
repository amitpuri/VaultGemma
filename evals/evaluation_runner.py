"""Main evaluation runner for all VaultGemma evaluation tests."""

import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Import directly to avoid circular import issues
from .base_evaluator import EvaluationSummary
from .business_evaluator import BusinessEvaluator
from .intent_evaluator import IntentEvaluator
from .sentiment_evaluator import SentimentEvaluator
from .entity_evaluator import EntityEvaluator


class EvaluationRunner:
    """Main runner for executing all evaluation tests."""
    
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
    
    def run_all_evaluations(self) -> Dict[str, EvaluationSummary]:
        """Run all evaluation tests.
        
        Returns:
            Dictionary mapping evaluator names to their results
        """
        print("🚀 VaultGemma Comprehensive Evaluation Suite")
        print("=" * 60)
        print(f"Model: {self.model_name}")
        print(f"Output Directory: {self.output_dir}")
        print(f"Timestamp: {datetime.now().isoformat()}")
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
    
    def run_specific_evaluation(self, evaluator_name: str) -> EvaluationSummary:
        """Run a specific evaluation.
        
        Args:
            evaluator_name: Name of the evaluator to run
            
        Returns:
            Evaluation summary
        """
        if evaluator_name not in self.evaluators:
            raise ValueError(f"Unknown evaluator: {evaluator_name}. Available: {list(self.evaluators.keys())}")
        
        print(f"🚀 Running {evaluator_name.upper()} evaluation")
        print("=" * 40)
        
        evaluator = self.evaluators[evaluator_name]
        summary = evaluator.run_evaluation()
        
        # Save results
        self._save_evaluator_results(evaluator_name, summary)
        
        return summary
    
    def _save_evaluator_results(self, evaluator_name: str, summary: EvaluationSummary) -> None:
        """Save results for a specific evaluator.
        
        Args:
            evaluator_name: Name of the evaluator
            summary: Evaluation summary
        """
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
    
    def _generate_overall_summary(self, results: Dict[str, EvaluationSummary]) -> None:
        """Generate overall summary of all evaluations.
        
        Args:
            results: Dictionary of evaluation results
        """
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
            
            # Save overall summary
            self._save_overall_summary(results, overall_score, pass_rate)
        else:
            print("❌ No tests were executed successfully")
    
    def _save_overall_summary(self, results: Dict[str, EvaluationSummary], overall_score: float, pass_rate: float) -> None:
        """Save overall summary to file.
        
        Args:
            results: Dictionary of evaluation results
            overall_score: Overall weighted score
            pass_rate: Overall pass rate percentage
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"overall_summary_{timestamp}.json"
        
        # Calculate detailed metrics
        evaluator_summaries = {}
        for evaluator_name, summary in results.items():
            if summary is not None:
                evaluator_summaries[evaluator_name] = {
                    "total_tests": summary.total_tests,
                    "passed_tests": summary.passed_tests,
                    "failed_tests": summary.failed_tests,
                    "average_score": summary.average_score,
                    "total_execution_time": summary.total_execution_time,
                    "pass_rate": (summary.passed_tests / summary.total_tests) * 100 if summary.total_tests > 0 else 0
                }
        
        data = {
            "model_name": self.model_name,
            "timestamp": datetime.now().isoformat(),
            "overall_metrics": {
                "total_tests": sum(s.total_tests for s in results.values() if s is not None),
                "total_passed": sum(s.passed_tests for s in results.values() if s is not None),
                "total_failed": sum(s.failed_tests for s in results.values() if s is not None),
                "overall_score": overall_score,
                "overall_pass_rate": pass_rate,
                "total_execution_time": sum(s.total_execution_time for s in results.values() if s is not None)
            },
            "evaluator_summaries": evaluator_summaries,
            "recommendations": self._generate_recommendations(results, overall_score, pass_rate)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Overall summary saved to: {filename}")
    
    def _generate_recommendations(self, results: Dict[str, EvaluationSummary], overall_score: float, pass_rate: float) -> List[str]:
        """Generate recommendations based on evaluation results.
        
        Args:
            results: Dictionary of evaluation results
            overall_score: Overall weighted score
            pass_rate: Overall pass rate percentage
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Overall performance recommendations
        if overall_score < 0.6:
            recommendations.append("Overall model performance is below acceptable threshold. Consider fine-tuning or using a different model.")
        elif overall_score < 0.8:
            recommendations.append("Model performance is moderate. Consider prompt engineering improvements or additional training.")
        else:
            recommendations.append("Model performance is good. Consider optimizing for specific use cases.")
        
        if pass_rate < 70:
            recommendations.append("Low pass rate indicates significant issues. Review failed test cases for common patterns.")
        
        # Specific evaluator recommendations
        for evaluator_name, summary in results.items():
            if summary is None:
                recommendations.append(f"{evaluator_name.title()} evaluation failed to run. Check model compatibility and configuration.")
                continue
            
            if summary.average_score < 0.6:
                recommendations.append(f"{evaluator_name.title()} performance is poor. Focus on improving this capability.")
            elif summary.passed_tests < summary.total_tests * 0.7:
                recommendations.append(f"{evaluator_name.title()} has high failure rate. Review test cases and model responses.")
        
        # Performance recommendations
        total_time = sum(s.total_execution_time for s in results.values() if s is not None)
        if total_time > 300:  # 5 minutes
            recommendations.append("Evaluation execution time is high. Consider optimizing model loading or reducing test complexity.")
        
        return recommendations


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
    runner = EvaluationRunner(
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
