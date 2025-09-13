# VaultGemma Evaluation Framework

A comprehensive evaluation suite for testing VaultGemma models across business scenarios, user intent recognition, entity extraction, and sentiment analysis.

## Overview

This evaluation framework provides structured testing for VaultGemma models with focus on:

- **Business Scenarios**: Enterprise use cases, strategic planning, financial analysis
- **User Intent Recognition**: Understanding user goals and extracting actionable insights
- **Sentiment Analysis**: Analyzing emotional tone and sentiment in text
- **Entity Extraction**: Identifying and categorizing named entities

## Features

- **Modular Design**: Separate evaluators for different capabilities
- **Comprehensive Scoring**: Multi-dimensional scoring with detailed metrics
- **Business-Focused**: Enterprise scenarios and real-world use cases
- **Detailed Reporting**: JSON output with recommendations
- **Configurable**: Customizable model parameters and test cases

## Installation

The evaluation framework is part of the VaultGemma package. Ensure you have the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Run All Evaluations

```bash
# Option 1: Using the standalone script (recommended)
python run_evaluations.py --model google/vaultgemma-1b

# Option 2: Using the module (may show warnings)
python -m evals.evaluation_runner --model google/vaultgemma-1b
```

### Run Specific Evaluator

```bash
# Business scenarios
python run_evaluations.py --evaluator business

# Intent recognition
python run_evaluations.py --evaluator intent

# Sentiment analysis
python run_evaluations.py --evaluator sentiment

# Entity extraction
python run_evaluations.py --evaluator entity
```

### Custom Configuration

```bash
python run_evaluations.py \
    --model google/vaultgemma-1b \
    --max-tokens 500 \
    --temperature 0.8 \
    --output-dir my_results
```

## Evaluators

### Business Evaluator

Tests enterprise scenarios including:
- Strategic planning and decision making
- Financial analysis and budgeting
- Operational efficiency improvements
- Digital transformation initiatives
- Talent management and HR scenarios
- Customer experience optimization
- Market expansion strategies
- Risk management and compliance
- Merger and acquisition analysis
- Sustainability initiatives

**Scoring Criteria:**
- Business relevance (30%)
- Actionability (25%)
- Structure and clarity (20%)
- Specificity (15%)
- Professional tone (10%)

### Intent Evaluator

Tests user intent recognition including:
- Information seeking
- Problem solving
- Decision making
- Action requests
- Confirmations
- Complaints and praise
- Clarification requests

**Scoring Criteria:**
- Intent recognition accuracy (40%)
- Entity extraction accuracy (30%)
- Response relevance (20%)
- Structured output (10%)

### Sentiment Evaluator

Tests sentiment analysis capabilities including:
- Positive, negative, and neutral sentiment
- Mixed sentiment detection
- Sarcasm and irony recognition
- Business communication sentiment
- Social media sentiment
- Product review analysis

**Scoring Criteria:**
- Sentiment accuracy (40%)
- Intensity detection (25%)
- Emotion recognition (20%)
- Context understanding (15%)

### Entity Evaluator

Tests entity extraction including:
- Person names and job titles
- Organizations and companies
- Locations and addresses
- Contact information (email, phone)
- Dates and times
- Financial data (currency, percentages)
- URLs and products
- Industry classifications

**Scoring Criteria:**
- Entity extraction accuracy (50%)
- Entity type classification (25%)
- Completeness (15%)
- Format consistency (10%)

## Usage Examples

### Python API

```python
from evals import BusinessEvaluator, EvaluationRunner

# Run specific evaluator
evaluator = BusinessEvaluator(model_name="google/vaultgemma-1b")
summary = evaluator.run_evaluation()

# Run all evaluators
runner = EvaluationRunner(model_name="google/vaultgemma-1b")
results = runner.run_all_evaluations()
```

### Custom Test Cases

```python
from evals import BusinessEvaluator

class CustomBusinessEvaluator(BusinessEvaluator):
    def get_test_cases(self):
        return [
            {
                "name": "custom_scenario",
                "prompt": "Your custom business prompt here...",
                "expected_output": None
            }
        ]

evaluator = CustomBusinessEvaluator()
summary = evaluator.run_evaluation()
```

## Output Format

### Individual Results

Each evaluator generates a JSON file with:

```json
{
  "evaluator": "business",
  "model_name": "google/vaultgemma-1b",
  "timestamp": "2024-01-15T10:30:00",
  "summary": {
    "total_tests": 10,
    "passed_tests": 8,
    "failed_tests": 2,
    "average_score": 0.75,
    "total_execution_time": 45.2
  },
  "results": [
    {
      "test_name": "strategic_planning",
      "prompt": "...",
      "actual_output": "...",
      "score": 0.85,
      "metrics": {
        "business_relevance": 0.9,
        "actionability": 0.8,
        "structure_clarity": 0.85
      },
      "execution_time": 4.2,
      "passed": true
    }
  ]
}
```

### Overall Summary

The overall summary includes:

```json
{
  "model_name": "google/vaultgemma-1b",
  "timestamp": "2024-01-15T10:30:00",
  "overall_metrics": {
    "total_tests": 40,
    "total_passed": 32,
    "overall_score": 0.78,
    "overall_pass_rate": 80.0
  },
  "evaluator_summaries": {
    "business": { "average_score": 0.75, "pass_rate": 80.0 },
    "intent": { "average_score": 0.82, "pass_rate": 90.0 }
  },
  "recommendations": [
    "Model performance is good. Consider optimizing for specific use cases.",
    "Business evaluator performance is moderate. Consider prompt engineering improvements."
  ]
}
```

## Configuration

### Model Configuration

```python
from evals import BusinessEvaluator

evaluator = BusinessEvaluator(
    model_name="google/vaultgemma-1b",
    max_tokens=500,
    temperature=0.8
)
```

### Generation Parameters

- `max_tokens`: Maximum tokens to generate (default: 300)
- `temperature`: Sampling temperature (default: 0.7)
- `top_p`: Nucleus sampling parameter (default: 0.9)
- `repetition_penalty`: Repetition penalty (default: 1.1)

## Best Practices

1. **Run Full Suite**: Always run all evaluators for comprehensive assessment
2. **Review Failures**: Analyze failed test cases for improvement opportunities
3. **Customize Prompts**: Adapt test cases for your specific use cases
4. **Monitor Performance**: Track evaluation metrics over time
5. **Iterate**: Use results to improve model performance and prompts

## Troubleshooting

### Common Issues

1. **Model Loading Errors**: Ensure model name is correct and accessible
2. **Memory Issues**: Reduce max_tokens or use smaller models
3. **Timeout Errors**: Increase timeout or reduce test complexity
4. **Authentication Errors**: Check HuggingFace/Kaggle credentials

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

To add new evaluators:

1. Inherit from `BaseEvaluator`
2. Implement `get_test_cases()` and `calculate_score()`
3. Add to `EvaluationRunner.evaluators`
4. Update documentation

## License

This evaluation framework is part of the VaultGemma project and follows the same license terms.
