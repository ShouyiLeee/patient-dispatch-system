import re
import logging

def preprocess_text(text):
    """
    Preprocess text for NLP analysis
    
    Args:
        text: Raw text input
        
    Returns:
        Preprocessed text
    """
    if not text:
        return ""
        
    # Convert to lowercase
    text = text.lower()
    
    # Replace common medical abbreviations
    abbreviations = {
        "dr.": "doctor",
        "hr": "heart rate",
        "bp": "blood pressure",
        "temp": "temperature",
        "meds": "medications",
        "med": "medication"
    }
    
    for abbr, full in abbreviations.items():
        pattern = r'\b' + abbr + r'\b'
        text = re.sub(pattern, full, text)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_medical_entities(text):
    """
    Extract medical entities from text
    
    Args:
        text: Preprocessed text
        
    Returns:
        Dictionary of extracted entities
    """
    # This would use a medical NER model in a real implementation
    # For demonstration, using a simple rule-based approach
    
    entities = {
        "symptoms": [],
        "medications": [],
        "conditions": []
    }
    
    # Simple pattern matching for common symptoms
    symptom_patterns = [
        (r'\b(head ?aches?|migraine)\b', 'headache'),
        (r'\bfever\b', 'fever'),
        (r'\bcough(ing)?\b', 'cough'),
        (r'\b(short|difficulty) of breath\b', 'shortness of breath'),
        (r'\bchest pain\b', 'chest pain'),
        (r'\bnause(a|ated)\b', 'nausea'),
        (r'\bvomit(ing)?\b', 'vomiting'),
        (r'\bdizziness\b', 'dizziness')
    ]
    
    for pattern, entity in symptom_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            entities["symptoms"].append(entity)
    
    return entities

def calculate_similarity(text1, text2):
    """
    Calculate similarity between two texts
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score between 0 and 1
    """
    # This would use more sophisticated methods in a real implementation
    # For demonstration, using a simple Jaccard similarity
    
    if not text1 or not text2:
        return 0
        
    # Tokenize
    tokens1 = set(text1.lower().split())
    tokens2 = set(text2.lower().split())
    
    # Calculate Jaccard similarity
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1.union(tokens2))
    
    if union == 0:
        return 0
        
    return intersection / union