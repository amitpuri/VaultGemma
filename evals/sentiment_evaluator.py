"""Sentiment analysis evaluation tests."""

import re
from typing import Dict, List, Any, Tuple, Optional
from .base_evaluator import BaseEvaluator


class SentimentEvaluator(BaseEvaluator):
    """Evaluator for sentiment analysis capabilities."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Sentiment lexicons
        self.positive_words = {
            'excellent', 'amazing', 'wonderful', 'fantastic', 'great', 'good', 'awesome',
            'brilliant', 'outstanding', 'perfect', 'superb', 'marvelous', 'terrific',
            'love', 'like', 'enjoy', 'pleased', 'satisfied', 'happy', 'delighted',
            'impressed', 'thrilled', 'excited', 'grateful', 'thankful', 'appreciate',
            'recommend', 'best', 'top', 'quality', 'reliable', 'trustworthy', 'professional'
        }
        
        self.negative_words = {
            'terrible', 'awful', 'horrible', 'bad', 'poor', 'worst', 'disappointing',
            'frustrated', 'angry', 'upset', 'annoyed', 'disgusted', 'hate', 'dislike',
            'unhappy', 'dissatisfied', 'displeased', 'furious', 'irritated', 'outraged',
            'complaint', 'problem', 'issue', 'error', 'broken', 'failed', 'useless',
            'waste', 'regret', 'disappointed', 'let down', 'betrayed', 'cheated'
        }
        
        self.neutral_words = {
            'okay', 'fine', 'average', 'normal', 'standard', 'typical', 'regular',
            'acceptable', 'adequate', 'sufficient', 'moderate', 'reasonable'
        }
        
        # Intensity modifiers
        self.intensifiers = {
            'very', 'extremely', 'incredibly', 'absolutely', 'completely', 'totally',
            'highly', 'really', 'quite', 'rather', 'somewhat', 'slightly', 'barely'
        }
        
        # Negation words
        self.negations = {
            'not', 'no', 'never', 'none', 'nothing', 'nobody', 'nowhere', 'neither',
            'nor', 'cannot', 'can\'t', 'won\'t', 'don\'t', 'doesn\'t', 'didn\'t',
            'isn\'t', 'aren\'t', 'wasn\'t', 'weren\'t', 'haven\'t', 'hasn\'t', 'hadn\'t'
        }
    
    def get_test_cases(self) -> List[Dict[str, Any]]:
        """Get sentiment analysis test cases."""
        return [
            {
                "name": "positive_feedback",
                "prompt": "Analyze the sentiment of this customer review: 'I absolutely love this product! The quality is outstanding and the customer service was excellent. I would definitely recommend it to anyone.'",
                "expected_sentiment": "positive",
                "expected_intensity": "high"
            },
            {
                "name": "negative_complaint",
                "prompt": "What is the sentiment of this message: 'This is the worst experience I've ever had. The product is completely broken and the support team was terrible. I'm extremely disappointed and will never buy from this company again.'",
                "expected_sentiment": "negative",
                "expected_intensity": "high"
            },
            {
                "name": "neutral_feedback",
                "prompt": "Determine the sentiment: 'The product is okay. It works as expected but nothing special. The delivery was fine and the price is reasonable.'",
                "expected_sentiment": "neutral",
                "expected_intensity": "low"
            },
            {
                "name": "mixed_sentiment",
                "prompt": "Analyze the sentiment of this review: 'The product quality is amazing and I love the design, but the customer service was horrible and the shipping took forever. Overall, I'm satisfied with the purchase but disappointed with the experience.'",
                "expected_sentiment": "mixed",
                "expected_intensity": "medium"
            },
            {
                "name": "sarcasm_detection",
                "prompt": "What is the sentiment of this comment: 'Oh great, another software update that breaks everything. Just what I needed today. Thanks for nothing!'",
                "expected_sentiment": "negative",
                "expected_intensity": "high"
            },
            {
                "name": "business_email_positive",
                "prompt": "Analyze the sentiment of this business email: 'Thank you for the excellent presentation yesterday. Your team did a fantastic job and we're very impressed with the results. We look forward to working with you on future projects.'",
                "expected_sentiment": "positive",
                "expected_intensity": "high"
            },
            {
                "name": "business_email_negative",
                "prompt": "What is the sentiment of this email: 'I'm writing to express my concern about the recent issues with our account. The service has been unreliable and we're experiencing significant problems. This is unacceptable for a business relationship.'",
                "expected_sentiment": "negative",
                "expected_intensity": "high"
            },
            {
                "name": "social_media_positive",
                "prompt": "Analyze this social media post: 'Just had the best coffee ever at @CoffeeShop! The barista was so friendly and the atmosphere is perfect for working. Highly recommend! ☕️❤️'",
                "expected_sentiment": "positive",
                "expected_intensity": "high"
            },
            {
                "name": "social_media_negative",
                "prompt": "What is the sentiment of this tweet: 'Ugh, stuck in traffic again. This commute is killing me. Why can't they fix these roads? #frustrated #traffic'",
                "expected_sentiment": "negative",
                "expected_intensity": "medium"
            },
            {
                "name": "product_review_detailed",
                "prompt": "Analyze the sentiment of this detailed product review: 'I've been using this product for 3 months now. The build quality is solid and it performs well for most tasks. However, the battery life is disappointing and the software could be more intuitive. It's a decent product but not worth the premium price. I'd give it 3 out of 5 stars.'",
                "expected_sentiment": "neutral",
                "expected_intensity": "medium"
            }
        ]
    
    def calculate_score(
        self, 
        prompt: str, 
        actual_output: str, 
        expected_output: Optional[str] = None
    ) -> Tuple[float, Dict[str, Any]]:
        """Calculate score for sentiment analysis evaluation.
        
        Scoring criteria:
        - Sentiment accuracy (40%)
        - Intensity detection (25%)
        - Emotion recognition (20%)
        - Context understanding (15%)
        """
        metrics = {}
        
        # Get expected sentiment from test case
        test_case = self._find_test_case(prompt)
        expected_sentiment = test_case.get('expected_sentiment') if test_case else None
        expected_intensity = test_case.get('expected_intensity') if test_case else None
        
        # Sentiment accuracy (40%)
        sentiment_accuracy = self._calculate_sentiment_accuracy(actual_output, expected_sentiment)
        metrics['sentiment_accuracy'] = sentiment_accuracy
        
        # Intensity detection (25%)
        intensity_accuracy = self._calculate_intensity_accuracy(actual_output, expected_intensity)
        metrics['intensity_accuracy'] = intensity_accuracy
        
        # Emotion recognition (20%)
        emotion_recognition = self._calculate_emotion_recognition(actual_output)
        metrics['emotion_recognition'] = emotion_recognition
        
        # Context understanding (15%)
        context_understanding = self._calculate_context_understanding(prompt, actual_output)
        metrics['context_understanding'] = context_understanding
        
        # Calculate weighted score
        score = (
            sentiment_accuracy * 0.40 +
            intensity_accuracy * 0.25 +
            emotion_recognition * 0.20 +
            context_understanding * 0.15
        )
        
        return score, metrics
    
    def _find_test_case(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Find the test case that matches the given prompt."""
        for test_case in self.get_test_cases():
            if test_case['prompt'] == prompt:
                return test_case
        return None
    
    def _calculate_sentiment_accuracy(self, output: str, expected_sentiment: Optional[str]) -> float:
        """Calculate sentiment classification accuracy."""
        if not expected_sentiment:
            return 0.5  # Neutral score if no expected sentiment
        
        output_lower = output.lower()
        
        # Check for explicit sentiment mentions
        if expected_sentiment in output_lower:
            return 1.0
        
        # Check for sentiment-related keywords
        if expected_sentiment == 'positive':
            positive_indicators = ['positive', 'good', 'favorable', 'optimistic', 'upbeat']
            if any(indicator in output_lower for indicator in positive_indicators):
                return 0.8
        elif expected_sentiment == 'negative':
            negative_indicators = ['negative', 'bad', 'unfavorable', 'pessimistic', 'downbeat']
            if any(indicator in output_lower for indicator in negative_indicators):
                return 0.8
        elif expected_sentiment == 'neutral':
            neutral_indicators = ['neutral', 'balanced', 'mixed', 'moderate', 'average']
            if any(indicator in output_lower for indicator in neutral_indicators):
                return 0.8
        elif expected_sentiment == 'mixed':
            mixed_indicators = ['mixed', 'both', 'combination', 'varied', 'conflicting']
            if any(indicator in output_lower for indicator in mixed_indicators):
                return 0.8
        
        # Check for sentiment words in the output
        positive_words_found = sum(1 for word in self.positive_words if word in output_lower)
        negative_words_found = sum(1 for word in self.negative_words if word in output_lower)
        neutral_words_found = sum(1 for word in self.neutral_words if word in output_lower)
        
        if expected_sentiment == 'positive' and positive_words_found > negative_words_found:
            return 0.6
        elif expected_sentiment == 'negative' and negative_words_found > positive_words_found:
            return 0.6
        elif expected_sentiment == 'neutral' and neutral_words_found > 0:
            return 0.6
        elif expected_sentiment == 'mixed' and positive_words_found > 0 and negative_words_found > 0:
            return 0.6
        
        return 0.0
    
    def _calculate_intensity_accuracy(self, output: str, expected_intensity: Optional[str]) -> float:
        """Calculate intensity detection accuracy."""
        if not expected_intensity:
            return 0.5  # Neutral score if no expected intensity
        
        output_lower = output.lower()
        
        # Check for explicit intensity mentions
        if expected_intensity in output_lower:
            return 1.0
        
        # Check for intensity-related keywords
        intensity_indicators = {
            'high': ['strong', 'intense', 'extreme', 'very', 'highly', 'extremely'],
            'medium': ['moderate', 'somewhat', 'fairly', 'reasonably', 'quite'],
            'low': ['mild', 'slight', 'barely', 'minimal', 'low']
        }
        
        expected_indicators = intensity_indicators.get(expected_intensity, [])
        if any(indicator in output_lower for indicator in expected_indicators):
            return 0.8
        
        # Check for intensifier words
        intensifier_count = sum(1 for intensifier in self.intensifiers if intensifier in output_lower)
        
        if expected_intensity == 'high' and intensifier_count >= 2:
            return 0.6
        elif expected_intensity == 'medium' and intensifier_count == 1:
            return 0.6
        elif expected_intensity == 'low' and intensifier_count == 0:
            return 0.6
        
        return 0.0
    
    def _calculate_emotion_recognition(self, output: str) -> float:
        """Calculate emotion recognition score."""
        output_lower = output.lower()
        score = 0.0
        
        # Check for emotion words
        emotion_words = {
            'joy': ['happy', 'joyful', 'cheerful', 'delighted', 'thrilled'],
            'anger': ['angry', 'furious', 'irritated', 'outraged', 'mad'],
            'sadness': ['sad', 'depressed', 'disappointed', 'upset', 'down'],
            'fear': ['afraid', 'scared', 'worried', 'anxious', 'concerned'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned'],
            'disgust': ['disgusted', 'revolted', 'repulsed', 'sickened', 'appalled']
        }
        
        emotions_found = 0
        for emotion, words in emotion_words.items():
            if any(word in output_lower for word in words):
                emotions_found += 1
        
        if emotions_found > 0:
            score += min(emotions_found / len(emotion_words), 1.0) * 0.6
        
        # Check for emotional intensity indicators
        emotional_intensifiers = ['very', 'extremely', 'incredibly', 'absolutely', 'completely']
        intensifier_count = sum(1 for intensifier in emotional_intensifiers if intensifier in output_lower)
        
        if intensifier_count > 0:
            score += min(intensifier_count / len(emotional_intensifiers), 1.0) * 0.4
        
        return min(score, 1.0)
    
    def _calculate_context_understanding(self, prompt: str, output: str) -> float:
        """Calculate context understanding score."""
        score = 0.0
        
        # Check if output addresses the specific text being analyzed
        if 'analyze' in prompt.lower() or 'sentiment' in prompt.lower():
            if any(word in output.lower() for word in ['analyze', 'analysis', 'sentiment', 'feeling', 'tone']):
                score += 0.4
        
        # Check for reference to the source text
        if 'this' in prompt.lower() or 'the following' in prompt.lower():
            if any(word in output.lower() for word in ['text', 'message', 'review', 'comment', 'statement']):
                score += 0.3
        
        # Check for appropriate response length and structure
        word_count = len(output.split())
        if 20 <= word_count <= 150:
            score += 0.2
        
        # Check for confidence indicators
        confidence_indicators = ['confident', 'certain', 'likely', 'probably', 'appears', 'seems']
        if any(indicator in output.lower() for indicator in confidence_indicators):
            score += 0.1
        
        return min(score, 1.0)
