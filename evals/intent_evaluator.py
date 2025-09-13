"""User intent recognition and extraction evaluation tests."""

import re
from typing import Dict, List, Any, Tuple, Optional
from .base_evaluator import BaseEvaluator


class IntentEvaluator(BaseEvaluator):
    """Evaluator for user intent recognition and extraction."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Intent categories and their indicators
        self.intent_categories = {
            'information_seeking': {
                'keywords': ['what', 'how', 'why', 'when', 'where', 'who', 'explain', 'tell me', 'describe'],
                'patterns': [r'what is', r'how does', r'why is', r'when does', r'where can']
            },
            'problem_solving': {
                'keywords': ['problem', 'issue', 'error', 'fix', 'solve', 'troubleshoot', 'help', 'broken'],
                'patterns': [r'how to fix', r'how to solve', r'what\'s wrong', r'not working']
            },
            'decision_making': {
                'keywords': ['should', 'choose', 'decide', 'recommend', 'better', 'best', 'compare', 'option'],
                'patterns': [r'should i', r'which is better', r'what should', r'recommend']
            },
            'action_request': {
                'keywords': ['do', 'make', 'create', 'build', 'generate', 'write', 'send', 'call'],
                'patterns': [r'can you', r'please', r'would you', r'could you']
            },
            'confirmation': {
                'keywords': ['confirm', 'verify', 'check', 'validate', 'correct', 'right', 'true'],
                'patterns': [r'is this', r'are you sure', r'confirm that']
            },
            'complaint': {
                'keywords': ['complaint', 'dissatisfied', 'unhappy', 'disappointed', 'frustrated', 'angry'],
                'patterns': [r'i\'m not happy', r'this is wrong', r'terrible', r'awful']
            },
            'praise': {
                'keywords': ['great', 'excellent', 'amazing', 'wonderful', 'love', 'perfect', 'fantastic'],
                'patterns': [r'thank you', r'well done', r'good job', r'impressed']
            },
            'clarification': {
                'keywords': ['clarify', 'explain more', 'elaborate', 'details', 'specific', 'precise'],
                'patterns': [r'can you explain', r'more details', r'be more specific']
            }
        }
        
        # Entity types to extract
        self.entity_types = {
            'person': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            'organization': r'\b[A-Z][a-z]+ (Inc|Corp|LLC|Ltd|Company|Corporation)\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            'time': r'\b\d{1,2}:\d{2}\s*(AM|PM|am|pm)?\b',
            'currency': r'\$\d+(?:,\d{3})*(?:\.\d{2})?\b',
            'percentage': r'\b\d+(?:\.\d+)?%\b',
            'url': r'https?://[^\s]+',
            'product': r'\b[A-Z][a-z]+ (Pro|Plus|Max|Mini|Air|Studio)\b'
        }
    
    def get_test_cases(self) -> List[Dict[str, Any]]:
        """Get intent recognition test cases."""
        return [
            {
                "name": "information_seeking_basic",
                "prompt": "What is the difference between machine learning and artificial intelligence?",
                "expected_intent": "information_seeking",
                "expected_entities": []
            },
            {
                "name": "problem_solving_technical",
                "prompt": "My computer keeps crashing when I run the new software. How can I fix this issue?",
                "expected_intent": "problem_solving",
                "expected_entities": []
            },
            {
                "name": "decision_making_business",
                "prompt": "Should I choose AWS or Google Cloud for our new project? We have a budget of $10,000 per month.",
                "expected_intent": "decision_making",
                "expected_entities": ["currency"]
            },
            {
                "name": "action_request_creation",
                "prompt": "Can you create a presentation about our Q3 sales results? The meeting is on 12/15/2024 at 2:00 PM.",
                "expected_intent": "action_request",
                "expected_entities": ["date", "time"]
            },
            {
                "name": "confirmation_check",
                "prompt": "Is this the correct email address for John Smith: john.smith@company.com?",
                "expected_intent": "confirmation",
                "expected_entities": ["person", "email"]
            },
            {
                "name": "complaint_service",
                "prompt": "I'm very disappointed with the customer service. I've been waiting for 3 hours and no one has helped me.",
                "expected_intent": "complaint",
                "expected_entities": []
            },
            {
                "name": "praise_positive",
                "prompt": "Thank you so much! The solution you provided worked perfectly. You're amazing!",
                "expected_intent": "praise",
                "expected_entities": []
            },
            {
                "name": "clarification_request",
                "prompt": "Can you explain more about the pricing structure? I need specific details about the enterprise plan.",
                "expected_intent": "clarification",
                "expected_entities": []
            },
            {
                "name": "complex_business_inquiry",
                "prompt": "Hi, I'm Sarah Johnson from TechCorp Inc. We're interested in your enterprise solution. Can you send me a quote for 100 licenses? My email is sarah.johnson@techcorp.com and my phone is 555-123-4567.",
                "expected_intent": "action_request",
                "expected_entities": ["person", "organization", "email", "phone"]
            },
            {
                "name": "multi_intent_mixed",
                "prompt": "I have a problem with my iPhone Pro Max. The battery drains too fast. Should I get it repaired or buy a new one? The repair costs $200 and a new phone is $1,200.",
                "expected_intent": "problem_solving",  # Primary intent
                "expected_entities": ["product", "currency"]
            }
        ]
    
    def calculate_score(
        self, 
        prompt: str, 
        actual_output: str, 
        expected_output: Optional[str] = None
    ) -> Tuple[float, Dict[str, Any]]:
        """Calculate score for intent recognition evaluation.
        
        Scoring criteria:
        - Intent recognition accuracy (40%)
        - Entity extraction accuracy (30%)
        - Response relevance (20%)
        - Structured output (10%)
        """
        metrics = {}
        
        # Get expected intent and entities from test case
        test_case = self._find_test_case(prompt)
        expected_intent = test_case.get('expected_intent') if test_case else None
        expected_entities = test_case.get('expected_entities', []) if test_case else []
        
        # Intent recognition accuracy (40%)
        intent_accuracy = self._calculate_intent_accuracy(actual_output, expected_intent)
        metrics['intent_accuracy'] = intent_accuracy
        
        # Entity extraction accuracy (30%)
        entity_accuracy = self._calculate_entity_accuracy(actual_output, expected_entities)
        metrics['entity_accuracy'] = entity_accuracy
        
        # Response relevance (20%)
        response_relevance = self._calculate_response_relevance(prompt, actual_output)
        metrics['response_relevance'] = response_relevance
        
        # Structured output (10%)
        structured_output = self._calculate_structured_output(actual_output)
        metrics['structured_output'] = structured_output
        
        # Calculate weighted score
        score = (
            intent_accuracy * 0.40 +
            entity_accuracy * 0.30 +
            response_relevance * 0.20 +
            structured_output * 0.10
        )
        
        return score, metrics
    
    def _find_test_case(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Find the test case that matches the given prompt."""
        for test_case in self.get_test_cases():
            if test_case['prompt'] == prompt:
                return test_case
        return None
    
    def _calculate_intent_accuracy(self, output: str, expected_intent: Optional[str]) -> float:
        """Calculate intent recognition accuracy."""
        if not expected_intent:
            return 0.5  # Neutral score if no expected intent
        
        output_lower = output.lower()
        
        # Check if the expected intent is mentioned
        if expected_intent.replace('_', ' ') in output_lower:
            return 1.0
        
        # Check for intent-related keywords
        expected_keywords = self.intent_categories.get(expected_intent, {}).get('keywords', [])
        keyword_matches = sum(1 for keyword in expected_keywords if keyword in output_lower)
        
        if keyword_matches > 0:
            return min(keyword_matches / len(expected_keywords), 1.0)
        
        # Check for intent patterns
        expected_patterns = self.intent_categories.get(expected_intent, {}).get('patterns', [])
        pattern_matches = sum(1 for pattern in expected_patterns if re.search(pattern, output_lower))
        
        if pattern_matches > 0:
            return 0.7  # Partial credit for pattern matching
        
        return 0.0
    
    def _calculate_entity_accuracy(self, output: str, expected_entities: List[str]) -> float:
        """Calculate entity extraction accuracy."""
        if not expected_entities:
            return 1.0  # Perfect score if no entities expected
        
        extracted_entities = self._extract_entities(output)
        expected_entities_set = set(expected_entities)
        extracted_entities_set = set(extracted_entities.keys())
        
        # Calculate precision and recall
        true_positives = len(expected_entities_set.intersection(extracted_entities_set))
        precision = true_positives / len(extracted_entities_set) if extracted_entities_set else 0
        recall = true_positives / len(expected_entities_set) if expected_entities_set else 0
        
        # F1 score
        if precision + recall == 0:
            return 0.0
        
        f1_score = 2 * (precision * recall) / (precision + recall)
        return f1_score
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from text."""
        entities = {}
        
        for entity_type, pattern in self.entity_types.items():
            matches = re.findall(pattern, text)
            if matches:
                entities[entity_type] = matches
        
        return entities
    
    def _calculate_response_relevance(self, prompt: str, output: str) -> float:
        """Calculate response relevance to the prompt."""
        score = 0.0
        
        # Check for prompt keywords in response
        prompt_words = set(prompt.lower().split())
        output_words = set(output.lower().split())
        
        common_words = prompt_words.intersection(output_words)
        if len(prompt_words) > 0:
            score += len(common_words) / len(prompt_words) * 0.5
        
        # Check for appropriate response length
        word_count = len(output.split())
        if 10 <= word_count <= 200:
            score += 0.3
        
        # Check for question answering (if prompt is a question)
        if '?' in prompt:
            if any(word in output.lower() for word in ['answer', 'response', 'explanation', 'solution']):
                score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_structured_output(self, output: str) -> float:
        """Calculate structured output score."""
        score = 0.0
        
        # Check for clear structure indicators
        structure_indicators = ['intent:', 'entities:', 'confidence:', 'analysis:']
        structure_matches = sum(1 for indicator in structure_indicators if indicator in output.lower())
        score += min(structure_matches / len(structure_indicators), 1.0) * 0.4
        
        # Check for JSON-like structure
        if '{' in output and '}' in output:
            score += 0.3
        
        # Check for bullet points or lists
        bullet_indicators = ['•', '-', '*', '1.', '2.', '3.']
        has_bullets = any(indicator in output for indicator in bullet_indicators)
        if has_bullets:
            score += 0.3
        
        return min(score, 1.0)
