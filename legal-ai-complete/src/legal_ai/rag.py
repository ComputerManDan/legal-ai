import logging
import pickle
from pathlib import Path
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer

from src.legal_ai.config import config

# Configure logging
logger = logging.getLogger(__name__)

# LOAD MODEL
try:
    model = SentenceTransformer(config.EMBEDDING_MODEL)
    logger.info("Successfully loaded SentenceTransformer model")
except Exception as e:
    logger.error(f"Failed to load SentenceTransformer model: {e}")
    raise

# LOAD CONTRACT DOCUMENTS
def load_documents(contracts_path: Path = None, chunk_size: int = None) -> Tuple[List[str], List[str]]:
    """
    Load contract documents and optionally chunk them.
    
    Args:
        contracts_path: Path to contracts directory
        chunk_size: Number of words per chunk (0 = no chunking)
    
    Returns:
        Tuple of (documents, filenames)
    """
    if contracts_path is None:
        contracts_path = config.CONTRACTS_DIR
    if chunk_size is None:
        chunk_size = config.CHUNK_SIZE
    
    if not contracts_path.exists():
        logger.warning(f"Contracts directory not found: {contracts_path}")
        return [], []
    
    documents = []
    filenames = []
    
    txt_files = list(contracts_path.glob("*.txt"))
    
    if not txt_files:
        logger.warning(f"No .txt files found in {contracts_path}")
    
    try:
        for file in txt_files:
            try:
                text = file.read_text(encoding="utf-8")
                
                if chunk_size > 0:
                    words = text.split()
                    for i in range(0, len(words), chunk_size):
                        chunk = " ".join(words[i:i + chunk_size])
                        documents.append(chunk)
                        filenames.append(f"{file.name} (chunk {i // chunk_size + 1})")
                else:
                    documents.append(text)
                    filenames.append(file.name)
                
                logger.info(f"Loaded {file.name}: {len(text)} characters")
            
            except Exception as e:
                logger.error(f"Failed to load {file.name}: {e}")
                continue
        
        logger.info(f"Total documents loaded: {len(documents)}")
        return documents, filenames
    
    except Exception as e:
        logger.error(f"Error loading documents: {e}")
        return [], []


def load_or_create_embeddings(
    documents: List[str],
    embedding_cache_path: Path = None
) -> np.ndarray:
    """
    Load embeddings from cache or create and cache them.
    
    Args:
        documents: List of document texts
        embedding_cache_path: Path to cache file
    
    Returns:
        Numpy array of embeddings
    """
    if embedding_cache_path is None:
        embedding_cache_path = config.EMBEDDING_CACHE_PATH
    
    embedding_cache_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Try to load from cache
    if embedding_cache_path.exists():
        try:
            with open(embedding_cache_path, "rb") as f:
                embeddings = pickle.load(f)
            logger.info(f"Loaded embeddings from cache: {embedding_cache_path}")
            return embeddings
        except Exception as e:
            logger.warning(f"Failed to load embedding cache: {e}. Regenerating...")
    
    # Create embeddings
    try:
        logger.info("Generating embeddings (this may take a moment)...")
        embeddings = model.encode(documents, show_progress_bar=True)
        
        # Cache embeddings
        try:
            with open(embedding_cache_path, "wb") as f:
                pickle.dump(embeddings, f)
            logger.info(f"Cached embeddings to {embedding_cache_path}")
        except Exception as e:
            logger.warning(f"Failed to cache embeddings: {e}")
        
        return embeddings
    
    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}")
        return np.array([])


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.
    Normalized version that accounts for vector magnitude.
    """
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return float(np.dot(a, b) / (norm_a * norm_b))


def retrieve(
    query: str,
    documents: List[str],
    filenames: List[str],
    embeddings: np.ndarray,
    top_k: int = 2
) -> List[Tuple[float, str, str]]:
    """
    Retrieve top-k most relevant documents for a query.
    
    Args:
        query: Search query
        documents: List of document texts
        filenames: List of document filenames
        embeddings: Precomputed embeddings
        top_k: Number of results to return
    
    Returns:
        List of (similarity_score, document_text, filename) tuples
    """
    if not query or not query.strip():
        logger.warning("Empty query provided")
        return []
    
    if len(documents) == 0:
        logger.warning("No documents available for retrieval")
        return []
    
    try:
        query_embedding = model.encode([query])[0]
        similarities = []
        
        for i, embedding in enumerate(embeddings):
            similarity = cosine_similarity(query_embedding, embedding)
            similarities.append((similarity, documents[i], filenames[i]))
        
        similarities.sort(reverse=True, key=lambda x: x[0])
        results = similarities[:top_k]
        logger.info(f"Retrieved {len(results)} results for query: {query[:50]}...")
        
        return results
    
    except Exception as e:
        logger.error(f"Error during retrieval: {e}")
        return []


# Initialize on module load
documents, filenames = load_documents()
embeddings = load_or_create_embeddings(documents)

if len(documents) > 0:
    logger.info("RAG system initialized successfully")
else:
    logger.warning("RAG system initialized with no documents")
