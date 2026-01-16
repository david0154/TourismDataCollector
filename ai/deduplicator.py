"""
AI-powered duplicate detection with AUTO MODEL DOWNLOAD
Model downloads automatically from Hugging Face on first run
"""
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer, util
import torch
import os
from config import MODEL_NAME, SIMILARITY_THRESHOLD, AUTO_DOWNLOAD_MODEL

class Deduplicator:
    def __init__(self):
        """
        Load lightweight AI model (61MB)
        AUTO-DOWNLOADS from Hugging Face on first run
        """
        print(f"\n{'='*60}")
        print(f"🤖 Initializing AI Model: {MODEL_NAME}")
        print(f"{'='*60}")
        
        if AUTO_DOWNLOAD_MODEL:
            print("📥 Model will download automatically if not present...")
            print("🌐 Source: Hugging Face (Open Source)")
            print("💾 Size: ~61MB (one-time download)")
            print("⏳ Please wait...")
        
        try:
            self.model = SentenceTransformer(MODEL_NAME)
            print("\n✅ AI Model loaded successfully!")
            print(f"✅ Model: {MODEL_NAME}")
            print(f"✅ Size: 61MB")
            print(f"✅ Ready for duplicate detection!")
            print(f"{'='*60}\n")
        except Exception as e:
            print(f"\n❌ Error loading model: {e}")
            print("💡 Tip: Check internet connection for first-time download")
            raise
    
    def find_duplicates(self, new_data: Dict[str, Any], 
                       existing_data: List[Dict[str, Any]]) -> Tuple[bool, List[Dict]]:
        """
        Check if new_data is a duplicate using AI semantic similarity
        Returns: (is_duplicate, list_of_similar_records)
        """
        if not existing_data:
            return False, []
        
        # Create text representation
        new_text = self._create_text_representation(new_data)
        existing_texts = [self._create_text_representation(item) for item in existing_data]
        
        # Encode and compare using AI
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
        """Create text representation for AI comparison"""
        fields = ['name', 'city', 'state', 'address', 'contact']
        text_parts = [str(data.get(field, '')) for field in fields if data.get(field)]
        return " ".join(text_parts)
