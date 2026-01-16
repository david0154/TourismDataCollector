"""
AI-powered duplicate detection using lightweight sentence transformer (61MB)
Model: paraphrase-MiniLM-L3-v2
"""
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer, util
import torch
from config import MODEL_NAME, SIMILARITY_THRESHOLD

class Deduplicator:
    def __init__(self):
        """Load lightweight open-source model (61MB)"""
        print(f"Loading AI model: {MODEL_NAME} (this is a one-time download)...")
        self.model = SentenceTransformer(MODEL_NAME)
        print("✓ AI model loaded successfully!")
    
    def find_duplicates(self, new_data: Dict[str, Any], 
                       existing_data: List[Dict[str, Any]]) -> Tuple[bool, List[Dict]]:
        """
        Check if new_data is a duplicate using semantic similarity
        Returns: (is_duplicate, list_of_similar_records)
        """
        if not existing_data:
            return False, []
        
        # Create text representation
        new_text = self._create_text_representation(new_data)
        existing_texts = [self._create_text_representation(item) for item in existing_data]
        
        # Encode and compare
        new_embedding = self.model.encode(new_text, convert_to_tensor=True)
        existing_embeddings = self.model.encode(existing_texts, convert_to_tensor=True)
        
        similarities = util.cos_sim(new_embedding, existing_embeddings)[0]
        
        # Find similar items
        similar_items = []
        for idx, similarity in enumerate(similarities):
            if similarity >= SIMILARITY_THRESHOLD:
                similar_items.append({
                    'data': existing_data[idx],
                    'similarity': float(similarity),
                    'similarity_percent': f"{float(similarity) * 100:.1f}%"
                })
        
        return len(similar_items) > 0, similar_items
    
    def _create_text_representation(self, data: Dict[str, Any]) -> str:
        """Create text representation for comparison"""
        fields = ['name', 'city', 'state', 'address', 'contact']
        text_parts = [str(data.get(field, '')) for field in fields if data.get(field)]
        return " ".join(text_parts)
