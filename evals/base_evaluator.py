"""Base evaluator class for VaultGemma evaluations."""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json
import time
from datetime import datetime

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from vaultgemma import ModelManager, TextGenerator, ModelConfig, GenerationConfig


@dataclass
class EvaluationResult:
    """Result of a single evaluation test."""
    
    test_name: str
    prompt: str
    expected_output: Optional[str]
    actual_output: str
    score: float
    metrics: Dict[str, Any]
    execution_time: float
    timestamp: str
    passed: bool


@dataclass
class EvaluationSummary:
    """Summary of evaluation results."""
    
    total_tests: int
    passed_tests: int
    failed_tests: int
    average_score: float
    total_execution_time: float
    results: List[EvaluationResult]


class BaseEvaluator(ABC):
    """Base class for all VaultGemma evaluators."""
    
    def __init__(
        self, 
        model_name: str = "google/vaultgemma-1b",
        max_tokens: int = 300,
        temperature: float = 0.7
    ):
        """Initialize the evaluator.
        
        Args:
            model_name: Name of the model to evaluate
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
        """
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.manager = None
        self.generator = None
        
    def setup_model(self) -> None:
        """Set up the model for evaluation."""
        try:
            print(f"🔄 Loading model: {self.model_name}")
            
            # Configure model
            model_config = ModelConfig(
                model_name=self.model_name,
                use_fast_tokenizer=False,
                device_map="auto"
            )
            
            # Configure generation
            generation_config = GenerationConfig(
                max_new_tokens=self.max_tokens,
                temperature=self.temperature,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1
            )
            
            # Initialize and load model
            self.manager = ModelManager()
            provider = self.manager.load_model(self.model_name, model_config=model_config)
            self.generator = TextGenerator(provider)
            
            print("✅ Model loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def cleanup_model(self) -> None:
        """Clean up the model after evaluation."""
        if self.manager:
            try:
                self.manager.unload_model()
                print("🧹 Model cleaned up")
            except Exception as e:
                print(f"⚠️ Warning: Error during cleanup: {e}")
    
    def generate_response(self, prompt: str) -> str:
        """Generate a response for the given prompt.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated response
        """
        if not self.generator:
            raise RuntimeError("Model not loaded. Call setup_model() first.")
        
        try:
            generation_config = GenerationConfig(
                max_new_tokens=self.max_tokens,
                temperature=self.temperature,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1
            )
            
            response = self.generator.generate(prompt, generation_config)
            return response.strip()
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return ""
    
    def run_single_test(
        self, 
        test_name: str, 
        prompt: str, 
        expected_output: Optional[str] = None
    ) -> EvaluationResult:
        """Run a single evaluation test.
        
        Args:
            test_name: Name of the test
            prompt: Input prompt
            expected_output: Expected output (optional)
            
        Returns:
            Evaluation result
        """
        start_time = time.time()
        
        try:
            actual_output = self.generate_response(prompt)
            execution_time = time.time() - start_time
            
            # Calculate score and metrics
            score, metrics = self.calculate_score(prompt, actual_output, expected_output)
            passed = score >= 0.7  # 70% threshold for passing
            
            return EvaluationResult(
                test_name=test_name,
                prompt=prompt,
                expected_output=expected_output,
                actual_output=actual_output,
                score=score,
                metrics=metrics,
                execution_time=execution_time,
                timestamp=datetime.now().isoformat(),
                passed=passed
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return EvaluationResult(
                test_name=test_name,
                prompt=prompt,
                expected_output=expected_output,
                actual_output=f"Error: {e}",
                score=0.0,
                metrics={"error": str(e)},
                execution_time=execution_time,
                timestamp=datetime.now().isoformat(),
                passed=False
            )
    
    @abstractmethod
    def calculate_score(
        self, 
        prompt: str, 
        actual_output: str, 
        expected_output: Optional[str] = None
    ) -> Tuple[float, Dict[str, Any]]:
        """Calculate score and metrics for the evaluation.
        
        Args:
            prompt: Input prompt
            actual_output: Generated output
            expected_output: Expected output (optional)
            
        Returns:
            Tuple of (score, metrics)
        """
        pass
    
    @abstractmethod
    def get_test_cases(self) -> List[Dict[str, Any]]:
        """Get list of test cases for evaluation.
        
        Returns:
            List of test case dictionaries
        """
        pass
    
    def run_evaluation(self) -> EvaluationSummary:
        """Run the complete evaluation.
        
        Returns:
            Evaluation summary
        """
        print(f"🚀 Starting {self.__class__.__name__} evaluation")
        print("=" * 50)
        
        # Setup model
        self.setup_model()
        
        try:
            # Get test cases
            test_cases = self.get_test_cases()
            results = []
            total_start_time = time.time()
            
            # Run tests
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n📝 Running test {i}/{len(test_cases)}: {test_case['name']}")
                
                result = self.run_single_test(
                    test_name=test_case['name'],
                    prompt=test_case['prompt'],
                    expected_output=test_case.get('expected_output')
                )
                
                results.append(result)
                
                # Print result
                status = "✅ PASSED" if result.passed else "❌ FAILED"
                print(f"   {status} - Score: {result.score:.2f} - Time: {result.execution_time:.2f}s")
            
            total_execution_time = time.time() - total_start_time
            
            # Calculate summary
            passed_tests = sum(1 for r in results if r.passed)
            failed_tests = len(results) - passed_tests
            average_score = sum(r.score for r in results) / len(results) if results else 0.0
            
            summary = EvaluationSummary(
                total_tests=len(results),
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                average_score=average_score,
                total_execution_time=total_execution_time,
                results=results
            )
            
            # Print summary
            self.print_summary(summary)
            
            return summary
            
        finally:
            # Cleanup
            self.cleanup_model()
    
    def print_summary(self, summary: EvaluationSummary) -> None:
        """Print evaluation summary.
        
        Args:
            summary: Evaluation summary
        """
        print("\n" + "=" * 50)
        print("📊 EVALUATION SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {summary.total_tests}")
        print(f"Passed: {summary.passed_tests} ({summary.passed_tests/summary.total_tests*100:.1f}%)")
        print(f"Failed: {summary.failed_tests} ({summary.failed_tests/summary.total_tests*100:.1f}%)")
        print(f"Average Score: {summary.average_score:.2f}")
        print(f"Total Execution Time: {summary.total_execution_time:.2f}s")
        print("=" * 50)
    
    def save_results(self, summary: EvaluationSummary, filename: str) -> None:
        """Save evaluation results to file.
        
        Args:
            summary: Evaluation summary
            filename: Output filename
        """
        # Convert to serializable format
        data = {
            "evaluator": self.__class__.__name__,
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
        
        print(f"💾 Results saved to: {filename}")
