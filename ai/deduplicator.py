"""
AI-powered duplicate detection using sentence transformers
"""
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer, util
import torch
from config import MODEL_NAME, SIMILARITY_THRESHOLD

class Deduplicator:
    def __init__(self):
        # Load lightweight open-source model
        self.model = SentenceTransformer(MODEL_NAME)
    
    def find_duplicates(self, new_data: Dict[str, Any], 
                       existing_data: List[Dict[str, Any]]) -> Tuple[bool, List[Dict]]:
        """
        Check if new_data is a duplicate of any existing_data
        Returns: (is_duplicate, list_of_similar_records)
        """
        if not existing_data:
            return False, []
        
        # Create text representation of new data
        new_text = self._create_text_representation(new_data)
        
        # Create text representations of existing data
        existing_texts = [self._create_text_representation(item) for item in existing_data]
        
        # Encode texts
        new_embedding = self.model.encode(new_text, convert_to_tensor=True)
        existing_embeddings = self.model.encode(existing_texts, convert_to_tensor=True)
        
        # Calculate cosine similarities
        similarities = util.cos_sim(new_embedding, existing_embeddings)[0]
        
        # Find similar items
        similar_items = []
        for idx, similarity in enumerate(similarities):
            if similarity >= SIMILARITY_THRESHOLD:
                similar_items.append({
                    'data': existing_data[idx],
                    'similarity': float(similarity)
                })
        
        is_duplicate = len(similar_items) > 0
        return is_duplicate, similar_items
    
    def _create_text_representation(self, data: Dict[str, Any]) -> str:
        """Create a text representation of data for comparison"""
        # Combine key fields into a single text
        fields = ['name', 'city', 'state', 'address', 'contact']
        text_parts = []
        
        for field in fields:
            if field in data and data[field]:
                text_parts.append(str(data[field]))
        
        return " ".join(text_parts)
    
    def batch_deduplicate(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicates from a list of data
        Returns: List of unique items
        """
        if not data_list:
            return []
        
        unique_items = []
        
        for item in data_list:
            is_dup, _ = self.find_duplicates(item, unique_items)
            if not is_dup:
                unique_items.append(item)
        
        return unique_items
