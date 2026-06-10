import logging
from src.legal_ai.rag import retrieve, documents, filenames, embeddings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_retrieval():
    """Test RAG retrieval system."""
    
    if not documents:
        logger.error("No documents loaded. Add .txt files to the data/contracts/ directory.")
        return
    
    test_queries = [
        "confidentiality obligations",
        "payment terms",
        "liability limitations",
        "termination clause"
    ]
    
    logger.info(f"Running RAG tests with {len(documents)} documents")
    print(f"\nTesting RAG with {len(documents)} documents\n")
    
    for query in test_queries:
        try:
            results = retrieve(
                query,
                documents,
                filenames,
                embeddings,
                top_k=2
            )
            
            print(f"Query: '{query}'")
            print("-" * 60)
            
            if results:
                for i, (score, doc, filename) in enumerate(results, 1):
                    print(f"Result {i}: {filename}")
                    print(f"Similarity Score: {score:.4f}")
                    print(f"Preview: {doc[:200]}...\n")
            else:
                print("No results found\n")
            
        except Exception as e:
            logger.error(f"Error retrieving results for '{query}': {e}")
            print(f"ERROR: {e}\n")


if __name__ == "__main__":
    test_retrieval()
