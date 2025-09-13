"""VaultGemma Evaluation Framework

This package contains comprehensive evaluation tests for VaultGemma models,
focusing on business scenarios, user intent recognition, entity extraction,
and sentiment analysis.
"""

__version__ = "1.0.0"
__author__ = "VaultGemma Team"

# Import classes only when needed to avoid circular import issues
def __getattr__(name):
    """Lazy import to avoid circular import warnings."""
    if name == "BaseEvaluator":
        from .base_evaluator import BaseEvaluator
        return BaseEvaluator
    elif name == "BusinessEvaluator":
        from .business_evaluator import BusinessEvaluator
        return BusinessEvaluator
    elif name == "IntentEvaluator":
        from .intent_evaluator import IntentEvaluator
        return IntentEvaluator
    elif name == "SentimentEvaluator":
        from .sentiment_evaluator import SentimentEvaluator
        return SentimentEvaluator
    elif name == "EntityEvaluator":
        from .entity_evaluator import EntityEvaluator
        return EntityEvaluator
    elif name == "EvaluationRunner":
        from .evaluation_runner import EvaluationRunner
        return EvaluationRunner
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    "BaseEvaluator",
    "BusinessEvaluator", 
    "IntentEvaluator",
    "SentimentEvaluator",
    "EntityEvaluator",
    "EvaluationRunner"
]
