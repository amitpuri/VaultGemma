"""Business-focused evaluation tests for enterprise scenarios."""

import re
from typing import Dict, List, Any, Tuple, Optional
from .base_evaluator import BaseEvaluator, EvaluationResult


class BusinessEvaluator(BaseEvaluator):
    """Evaluator for business and enterprise scenarios."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.business_keywords = {
            'strategy': ['strategy', 'strategic', 'planning', 'roadmap', 'vision', 'mission'],
            'finance': ['budget', 'cost', 'revenue', 'profit', 'investment', 'roi', 'financial'],
            'operations': ['process', 'workflow', 'efficiency', 'productivity', 'optimization'],
            'leadership': ['leadership', 'management', 'team', 'collaboration', 'decision'],
            'technology': ['digital', 'automation', 'innovation', 'technology', 'system'],
            'customer': ['customer', 'client', 'user', 'experience', 'satisfaction', 'service'],
            'market': ['market', 'competition', 'competitive', 'industry', 'trends'],
            'risk': ['risk', 'security', 'compliance', 'governance', 'audit']
        }
    
    def get_test_cases(self) -> List[Dict[str, Any]]:
        """Get business-focused test cases."""
        return [
            {
                "name": "strategic_planning",
                "prompt": "As a CEO of a mid-size technology company, I need to develop a 3-year strategic plan to expand into the European market. Our current revenue is $50M annually, and we have 200 employees. What are the key strategic initiatives I should consider, and what resources will I need?",
                "expected_output": None
            },
            {
                "name": "financial_analysis",
                "prompt": "Our company's Q3 financial results show declining profit margins from 15% to 12% while revenue increased by 8%. Our main competitor just launched a similar product at 20% lower price. As CFO, what immediate actions should I recommend to the board?",
                "expected_output": None
            },
            {
                "name": "operational_efficiency",
                "prompt": "Our manufacturing plant has been experiencing 15% higher production costs due to supply chain disruptions and increased energy prices. We need to reduce costs by 10% while maintaining quality. What operational improvements would you recommend?",
                "expected_output": None
            },
            {
                "name": "digital_transformation",
                "prompt": "We're a traditional retail company with 500 stores nationwide. Our online sales represent only 15% of total revenue, but our competitors are at 40%. The board wants to accelerate digital transformation. What's your recommended approach and timeline?",
                "expected_output": None
            },
            {
                "name": "talent_management",
                "prompt": "Our software engineering team has 30% turnover rate, and we're struggling to hire senior developers. Our main competitor is offering 25% higher salaries. As VP of Engineering, what retention and recruitment strategies should I implement?",
                "expected_output": None
            },
            {
                "name": "customer_experience",
                "prompt": "Our customer satisfaction scores dropped from 4.2 to 3.8 in the last quarter. Complaints about response time and product quality have increased by 40%. As Head of Customer Experience, what immediate and long-term actions should I take?",
                "expected_output": None
            },
            {
                "name": "market_expansion",
                "prompt": "We're a B2B SaaS company with strong presence in North America. We want to expand to Asia-Pacific markets, specifically Singapore, Australia, and Japan. What market entry strategy would you recommend, and what are the key considerations?",
                "expected_output": None
            },
            {
                "name": "risk_management",
                "prompt": "Our company handles sensitive customer data and is subject to GDPR, CCPA, and SOX compliance. We're planning to migrate to cloud infrastructure. As Chief Risk Officer, what security and compliance measures should I prioritize?",
                "expected_output": None
            },
            {
                "name": "merger_acquisition",
                "prompt": "We're considering acquiring a smaller competitor for $25M. They have complementary technology and 50 employees. Our due diligence shows potential integration challenges and cultural differences. What factors should influence our decision?",
                "expected_output": None
            },
            {
                "name": "sustainability_initiative",
                "prompt": "Our board has committed to achieving net-zero emissions by 2030. We're a manufacturing company with 20 facilities worldwide. What sustainability initiatives should we prioritize, and how can we measure progress while maintaining profitability?",
                "expected_output": None
            }
        ]
    
    def calculate_score(
        self, 
        prompt: str, 
        actual_output: str, 
        expected_output: Optional[str] = None
    ) -> Tuple[float, Dict[str, Any]]:
        """Calculate score for business evaluation.
        
        Scoring criteria:
        - Business relevance (30%)
        - Actionability (25%)
        - Structure and clarity (20%)
        - Specificity (15%)
        - Professional tone (10%)
        """
        metrics = {}
        
        # Business relevance (30%)
        business_relevance = self._calculate_business_relevance(actual_output)
        metrics['business_relevance'] = business_relevance
        
        # Actionability (25%)
        actionability = self._calculate_actionability(actual_output)
        metrics['actionability'] = actionability
        
        # Structure and clarity (20%)
        structure_clarity = self._calculate_structure_clarity(actual_output)
        metrics['structure_clarity'] = structure_clarity
        
        # Specificity (15%)
        specificity = self._calculate_specificity(actual_output)
        metrics['specificity'] = specificity
        
        # Professional tone (10%)
        professional_tone = self._calculate_professional_tone(actual_output)
        metrics['professional_tone'] = professional_tone
        
        # Calculate weighted score
        score = (
            business_relevance * 0.30 +
            actionability * 0.25 +
            structure_clarity * 0.20 +
            specificity * 0.15 +
            professional_tone * 0.10
        )
        
        return score, metrics
    
    def _calculate_business_relevance(self, output: str) -> float:
        """Calculate business relevance score."""
        score = 0.0
        output_lower = output.lower()
        
        # Check for business keywords
        keyword_matches = 0
        total_keywords = 0
        
        for category, keywords in self.business_keywords.items():
            total_keywords += len(keywords)
            for keyword in keywords:
                if keyword in output_lower:
                    keyword_matches += 1
        
        if total_keywords > 0:
            score += (keyword_matches / total_keywords) * 0.4
        
        # Check for business concepts
        business_concepts = [
            'roi', 'kpi', 'metrics', 'benchmark', 'stakeholder',
            'quarterly', 'annual', 'budget', 'forecast', 'analysis',
            'implementation', 'execution', 'timeline', 'milestone'
        ]
        
        concept_matches = sum(1 for concept in business_concepts if concept in output_lower)
        score += min(concept_matches / len(business_concepts), 1.0) * 0.3
        
        # Check for quantitative elements
        numbers = re.findall(r'\d+[%$MKB]?', output)
        if len(numbers) >= 2:
            score += 0.3
        
        return min(score, 1.0)
    
    def _calculate_actionability(self, output: str) -> float:
        """Calculate actionability score."""
        score = 0.0
        output_lower = output.lower()
        
        # Action words
        action_words = [
            'implement', 'execute', 'develop', 'create', 'establish',
            'build', 'launch', 'deploy', 'initiate', 'start',
            'recommend', 'suggest', 'propose', 'plan', 'strategy'
        ]
        
        action_matches = sum(1 for word in action_words if word in output_lower)
        score += min(action_matches / len(action_words), 1.0) * 0.4
        
        # Specific steps or phases
        step_indicators = ['first', 'second', 'third', 'step', 'phase', 'stage']
        step_matches = sum(1 for indicator in step_indicators if indicator in output_lower)
        score += min(step_matches / len(step_indicators), 1.0) * 0.3
        
        # Timeline references
        timeline_words = ['immediately', 'short-term', 'long-term', 'within', 'by', 'timeline']
        timeline_matches = sum(1 for word in timeline_words if word in output_lower)
        score += min(timeline_matches / len(timeline_words), 1.0) * 0.3
        
        return min(score, 1.0)
    
    def _calculate_structure_clarity(self, output: str) -> float:
        """Calculate structure and clarity score."""
        score = 0.0
        
        # Check for clear structure
        lines = output.split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        
        if len(non_empty_lines) >= 3:
            score += 0.3
        
        # Check for bullet points or numbered lists
        bullet_indicators = ['•', '-', '*', '1.', '2.', '3.']
        has_bullets = any(indicator in output for indicator in bullet_indicators)
        if has_bullets:
            score += 0.3
        
        # Check for paragraph structure
        paragraphs = [p.strip() for p in output.split('\n\n') if p.strip()]
        if len(paragraphs) >= 2:
            score += 0.2
        
        # Check for clear sentences
        sentences = re.split(r'[.!?]+', output)
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences) if sentences else 0
        
        if 10 <= avg_sentence_length <= 25:
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_specificity(self, output: str) -> float:
        """Calculate specificity score."""
        score = 0.0
        
        # Check for specific numbers and metrics
        numbers = re.findall(r'\d+[%$MKB]?', output)
        if len(numbers) >= 3:
            score += 0.4
        
        # Check for specific timeframes
        timeframes = ['days', 'weeks', 'months', 'quarters', 'years', 'Q1', 'Q2', 'Q3', 'Q4']
        timeframe_matches = sum(1 for tf in timeframes if tf in output.lower())
        if timeframe_matches >= 2:
            score += 0.3
        
        # Check for specific roles or departments
        roles = ['ceo', 'cfo', 'cto', 'vp', 'director', 'manager', 'team', 'department']
        role_matches = sum(1 for role in roles if role in output.lower())
        if role_matches >= 2:
            score += 0.3
        
        return min(score, 1.0)
    
    def _calculate_professional_tone(self, output: str) -> float:
        """Calculate professional tone score."""
        score = 0.0
        output_lower = output.lower()
        
        # Check for professional language
        professional_words = [
            'recommend', 'suggest', 'propose', 'consider', 'evaluate',
            'analyze', 'assess', 'implement', 'execute', 'strategic',
            'tactical', 'operational', 'systematic', 'comprehensive'
        ]
        
        professional_matches = sum(1 for word in professional_words if word in output_lower)
        score += min(professional_matches / len(professional_words), 1.0) * 0.5
        
        # Check for formal structure
        formal_indicators = ['furthermore', 'moreover', 'however', 'therefore', 'consequently']
        formal_matches = sum(1 for indicator in formal_indicators if indicator in output_lower)
        score += min(formal_matches / len(formal_indicators), 1.0) * 0.3
        
        # Check for appropriate length (not too casual, not too verbose)
        word_count = len(output.split())
        if 50 <= word_count <= 300:
            score += 0.2
        
        return min(score, 1.0)
