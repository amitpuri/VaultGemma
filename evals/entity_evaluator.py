"""Entity recognition and extraction evaluation tests."""

import re
from typing import Dict, List, Any, Tuple, Optional, Set
from .base_evaluator import BaseEvaluator


class EntityEvaluator(BaseEvaluator):
    """Evaluator for entity recognition and extraction capabilities."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Entity patterns and examples
        self.entity_patterns = {
            'person': {
                'pattern': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
                'examples': ['John Smith', 'Sarah Johnson', 'Michael Brown', 'Emily Davis']
            },
            'organization': {
                'pattern': r'\b[A-Z][a-z]+ (Inc|Corp|LLC|Ltd|Company|Corporation|Group|Systems|Technologies|Solutions)\b',
                'examples': ['Apple Inc', 'Microsoft Corp', 'Google LLC', 'Amazon Company']
            },
            'location': {
                'pattern': r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)*,? (?:[A-Z]{2}|[A-Z][a-z]+)\b',
                'examples': ['New York, NY', 'San Francisco, CA', 'London, UK', 'Tokyo, Japan']
            },
            'email': {
                'pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                'examples': ['john@example.com', 'sarah.johnson@company.com', 'info@business.org']
            },
            'phone': {
                'pattern': r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
                'examples': ['555-123-4567', '(555) 123-4567', '555.123.4567', '+1-555-123-4567']
            },
            'date': {
                'pattern': r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})\b',
                'examples': ['12/25/2024', '2024-12-25', 'Dec 25, 2024', '25/12/2024']
            },
            'time': {
                'pattern': r'\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\b',
                'examples': ['2:30 PM', '14:30', '9:00 AM', '23:45']
            },
            'currency': {
                'pattern': r'\$\d+(?:,\d{3})*(?:\.\d{2})?\b',
                'examples': ['$100', '$1,000', '$1,234.56', '$50,000']
            },
            'percentage': {
                'pattern': r'\b\d+(?:\.\d+)?%\b',
                'examples': ['25%', '50.5%', '100%', '0.1%']
            },
            'url': {
                'pattern': r'https?://[^\s]+',
                'examples': ['https://example.com', 'http://www.company.com', 'https://api.service.com/v1']
            },
            'product': {
                'pattern': r'\b[A-Z][a-z]+ (?:Pro|Plus|Max|Mini|Air|Studio|Enterprise|Standard|Premium)\b',
                'examples': ['iPhone Pro', 'MacBook Air', 'Surface Pro', 'iPad Mini']
            },
            'job_title': {
                'pattern': r'\b(?:CEO|CFO|CTO|VP|Director|Manager|Senior|Junior|Lead|Principal|Staff|Engineer|Developer|Analyst|Consultant|Specialist)\b',
                'examples': ['CEO', 'Senior Engineer', 'VP of Sales', 'Product Manager']
            },
            'industry': {
                'pattern': r'\b(?:Technology|Healthcare|Finance|Education|Retail|Manufacturing|Automotive|Aerospace|Pharmaceutical|Energy|Real Estate|Entertainment|Media|Telecommunications|Transportation|Logistics|Agriculture|Construction|Consulting|Legal|Government|Non-profit)\b',
                'examples': ['Technology', 'Healthcare', 'Finance', 'Education']
            }
        }
    
    def get_test_cases(self) -> List[Dict[str, Any]]:
        """Get entity extraction test cases."""
        return [
            {
                "name": "business_card_extraction",
                "prompt": "Extract all entities from this business card information: 'John Smith, CEO at TechCorp Inc, email: john.smith@techcorp.com, phone: (555) 123-4567, located in San Francisco, CA.'",
                "expected_entities": ['person', 'organization', 'email', 'phone', 'location', 'job_title']
            },
            {
                "name": "meeting_invitation",
                "prompt": "Identify entities in this meeting invitation: 'Meeting with Sarah Johnson from Microsoft Corp on Dec 15, 2024 at 2:30 PM. Budget discussion for $50,000 project. Contact: sarah.johnson@microsoft.com or call 555-987-6543.'",
                "expected_entities": ['person', 'organization', 'date', 'time', 'currency', 'email', 'phone']
            },
            {
                "name": "product_review",
                "prompt": "Extract entities from this review: 'I bought the iPhone Pro Max for $1,200 from Apple Inc. The delivery to New York, NY was fast. Contact support at support@apple.com or 1-800-APL-CARE.'",
                "expected_entities": ['product', 'currency', 'organization', 'location', 'email', 'phone']
            },
            {
                "name": "financial_report",
                "prompt": "Find entities in this financial data: 'Q3 2024 revenue increased by 15% to $2.5M. Our CFO, Michael Brown, will present at the board meeting on 10/15/2024 at 9:00 AM. Visit our website at https://company.com for details.'",
                "expected_entities": ['date', 'percentage', 'currency', 'person', 'job_title', 'date', 'time', 'url']
            },
            {
                "name": "job_posting",
                "prompt": "Extract entities from this job posting: 'Senior Software Engineer position at Google LLC in Mountain View, CA. Salary range $120,000-$180,000. Apply by 12/31/2024. Contact: careers@google.com or call (650) 253-0000.'",
                "expected_entities": ['job_title', 'organization', 'location', 'currency', 'date', 'email', 'phone']
            },
            {
                "name": "news_article",
                "prompt": "Identify entities in this news snippet: 'Tesla Inc announced a 25% increase in sales for 2024. CEO Elon Musk will speak at the conference in Austin, TX on Jan 20, 2025 at 3:00 PM. Stock price rose to $250.50.'",
                "expected_entities": ['organization', 'percentage', 'date', 'person', 'job_title', 'location', 'date', 'time', 'currency']
            },
            {
                "name": "customer_support",
                "prompt": "Extract entities from this support ticket: 'Customer: Jane Doe, Account #12345, purchased MacBook Air for $999.99 on 11/15/2024. Issue reported on 11/20/2024 at 10:30 AM. Contact: jane.doe@email.com, phone: 555-555-0123.'",
                "expected_entities": ['person', 'product', 'currency', 'date', 'date', 'time', 'email', 'phone']
            },
            {
                "name": "contract_information",
                "prompt": "Find entities in this contract excerpt: 'Agreement between ABC Corporation and XYZ Ltd, signed on March 1, 2024. Contract value: $100,000. Project completion by June 30, 2024. Contact: legal@abc.com, (212) 555-0199.'",
                "expected_entities": ['organization', 'organization', 'date', 'currency', 'date', 'email', 'phone']
            },
            {
                "name": "social_media_post",
                "prompt": "Extract entities from this social media post: 'Just had an amazing meeting with the team at Salesforce Inc in San Francisco, CA! Our VP of Marketing, Lisa Chen, presented our Q4 results showing 30% growth. #business #success'",
                "expected_entities": ['organization', 'location', 'person', 'job_title', 'percentage']
            },
            {
                "name": "complex_business_document",
                "prompt": "Identify all entities in this business document: 'Amazon Web Services (AWS) partnership with IBM Corp announced on 09/15/2024. Project budget: $5M over 18 months. Key contacts: John Smith (john@aws.com, 206-266-1000) and Mary Johnson (mary@ibm.com, 914-499-1900). Implementation in Seattle, WA and Armonk, NY.'",
                "expected_entities": ['organization', 'organization', 'date', 'currency', 'person', 'email', 'phone', 'person', 'email', 'phone', 'location', 'location']
            }
        ]
    
    def calculate_score(
        self, 
        prompt: str, 
        actual_output: str, 
        expected_output: Optional[str] = None
    ) -> Tuple[float, Dict[str, Any]]:
        """Calculate score for entity extraction evaluation.
        
        Scoring criteria:
        - Entity extraction accuracy (50%)
        - Entity type classification (25%)
        - Completeness (15%)
        - Format consistency (10%)
        """
        metrics = {}
        
        # Get expected entities from test case
        test_case = self._find_test_case(prompt)
        expected_entities = test_case.get('expected_entities', []) if test_case else []
        
        # Entity extraction accuracy (50%)
        extraction_accuracy = self._calculate_extraction_accuracy(actual_output, expected_entities)
        metrics['extraction_accuracy'] = extraction_accuracy
        
        # Entity type classification (25%)
        type_classification = self._calculate_type_classification(actual_output, expected_entities)
        metrics['type_classification'] = type_classification
        
        # Completeness (15%)
        completeness = self._calculate_completeness(actual_output, expected_entities)
        metrics['completeness'] = completeness
        
        # Format consistency (10%)
        format_consistency = self._calculate_format_consistency(actual_output)
        metrics['format_consistency'] = format_consistency
        
        # Calculate weighted score
        score = (
            extraction_accuracy * 0.50 +
            type_classification * 0.25 +
            completeness * 0.15 +
            format_consistency * 0.10
        )
        
        return score, metrics
    
    def _find_test_case(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Find the test case that matches the given prompt."""
        for test_case in self.get_test_cases():
            if test_case['prompt'] == prompt:
                return test_case
        return None
    
    def _calculate_extraction_accuracy(self, output: str, expected_entities: List[str]) -> float:
        """Calculate entity extraction accuracy."""
        if not expected_entities:
            return 1.0  # Perfect score if no entities expected
        
        # Extract entities from the output
        extracted_entities = self._extract_entities_from_output(output)
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
    
    def _calculate_type_classification(self, output: str, expected_entities: List[str]) -> float:
        """Calculate entity type classification accuracy."""
        if not expected_entities:
            return 1.0
        
        output_lower = output.lower()
        score = 0.0
        
        # Check for correct entity type mentions
        for entity_type in expected_entities:
            if entity_type in output_lower:
                score += 1.0
        
        # Check for entity type synonyms
        entity_synonyms = {
            'person': ['name', 'individual', 'people', 'person'],
            'organization': ['company', 'corporation', 'business', 'firm', 'organization'],
            'location': ['place', 'city', 'address', 'location'],
            'email': ['email', 'e-mail', 'mail'],
            'phone': ['phone', 'telephone', 'number', 'contact'],
            'date': ['date', 'day', 'time'],
            'time': ['time', 'hour', 'moment'],
            'currency': ['money', 'price', 'cost', 'amount', 'dollar'],
            'percentage': ['percent', 'rate', 'ratio'],
            'url': ['website', 'link', 'url', 'web'],
            'product': ['product', 'item', 'device'],
            'job_title': ['title', 'position', 'role', 'job'],
            'industry': ['sector', 'field', 'industry', 'domain']
        }
        
        for entity_type in expected_entities:
            synonyms = entity_synonyms.get(entity_type, [])
            if any(synonym in output_lower for synonym in synonyms):
                score += 0.5
        
        return min(score / len(expected_entities), 1.0) if expected_entities else 0.0
    
    def _calculate_completeness(self, output: str, expected_entities: List[str]) -> float:
        """Calculate completeness of entity extraction."""
        if not expected_entities:
            return 1.0
        
        # Count how many expected entity types are found
        output_lower = output.lower()
        found_entities = 0
        
        for entity_type in expected_entities:
            if entity_type in output_lower:
                found_entities += 1
        
        return found_entities / len(expected_entities)
    
    def _calculate_format_consistency(self, output: str) -> float:
        """Calculate format consistency score."""
        score = 0.0
        
        # Check for structured output
        if ':' in output and '\n' in output:
            score += 0.3
        
        # Check for consistent formatting
        lines = output.split('\n')
        formatted_lines = [line for line in lines if ':' in line and line.strip()]
        
        if len(formatted_lines) >= 2:
            score += 0.3
        
        # Check for JSON-like structure
        if '{' in output and '}' in output:
            score += 0.2
        
        # Check for bullet points or lists
        bullet_indicators = ['•', '-', '*', '1.', '2.', '3.']
        has_bullets = any(indicator in output for indicator in bullet_indicators)
        if has_bullets:
            score += 0.2
        
        return min(score, 1.0)
    
    def _extract_entities_from_output(self, output: str) -> Dict[str, List[str]]:
        """Extract entities from the model output."""
        entities = {}
        output_lower = output.lower()
        
        # Check for explicit entity type mentions
        for entity_type in self.entity_patterns.keys():
            if entity_type in output_lower:
                entities[entity_type] = []
                
                # Try to extract actual entity values using the pattern
                pattern = self.entity_patterns[entity_type]['pattern']
                matches = re.findall(pattern, output)
                if matches:
                    entities[entity_type] = matches
        
        # Also check for entity synonyms
        entity_synonyms = {
            'person': ['name', 'individual', 'people'],
            'organization': ['company', 'corporation', 'business', 'firm'],
            'location': ['place', 'city', 'address'],
            'email': ['email', 'e-mail', 'mail'],
            'phone': ['phone', 'telephone', 'number'],
            'date': ['date', 'day'],
            'time': ['time', 'hour'],
            'currency': ['money', 'price', 'cost', 'amount'],
            'percentage': ['percent', 'rate'],
            'url': ['website', 'link', 'url'],
            'product': ['product', 'item', 'device'],
            'job_title': ['title', 'position', 'role'],
            'industry': ['sector', 'field', 'domain']
        }
        
        for entity_type, synonyms in entity_synonyms.items():
            if any(synonym in output_lower for synonym in synonyms) and entity_type not in entities:
                entities[entity_type] = []
        
        return entities
