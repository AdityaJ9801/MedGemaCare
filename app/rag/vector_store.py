"""Vector store management for RAG system."""

from typing import List, Optional

from app.config import settings
from app.utils.logger import app_logger

# Try to import RAG dependencies - make them optional.
# LangChain >= 0.2 split text-splitters and HuggingFace embeddings into
# separate packages, so we try the new paths first then fall back to the old ones.
_import_error: Exception | None = None
try:
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        from langchain.text_splitter import RecursiveCharacterTextSplitter  # type: ignore[no-redef]

    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError:
        from langchain_community.embeddings import HuggingFaceEmbeddings  # type: ignore[no-redef]

    from langchain_community.vectorstores import Chroma
    RAG_AVAILABLE = True
except ImportError as _e:
    _import_error = _e
    RAG_AVAILABLE = False
    RecursiveCharacterTextSplitter = None  # type: ignore[assignment,misc]
    HuggingFaceEmbeddings = None           # type: ignore[assignment,misc]
    Chroma = None                          # type: ignore[assignment,misc]
    app_logger.warning(
        f"RAG dependencies failed to import ({_e}). "
        "Run: pip install langchain langchain-community langchain-text-splitters "
        "langchain-huggingface chromadb sentence-transformers"
    )


class VectorStoreManager:
    """Manages vector store for efficient document retrieval."""
    
    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        self.text_splitter = None
        self._initialize()
    
    def _initialize(self):
        """Initialize embeddings and text splitter."""
        if not RAG_AVAILABLE:
            app_logger.warning("RAG dependencies not available. Vector store features disabled.")
            return

        app_logger.info("Initializing vector store manager")

        try:
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.embedding_model,
                cache_folder=str(settings.model_cache_dir),
            )

            # Initialize text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", ". ", " ", ""],
            )

            app_logger.info("Vector store manager initialized")
        except Exception as e:
            app_logger.error(f"Failed to initialize vector store: {e}")
            app_logger.warning("Vector store features will be disabled")
    
    def create_vector_store(
        self,
        documents: List[str],
        collection_name: str = "medical_reports",
    ) -> None:
        """Create vector store from documents."""
        if not RAG_AVAILABLE:
            raise RuntimeError(
                "RAG dependencies not available. Please install: pip install langchain langchain-community chromadb sentence-transformers"
            )

        try:
            app_logger.info(f"Creating vector store with {len(documents)} documents")

            # Split documents into chunks
            all_chunks = []
            for doc in documents:
                chunks = self.text_splitter.split_text(doc)
                all_chunks.extend(chunks)

            app_logger.info(f"Split into {len(all_chunks)} chunks")

            # Create vector store
            if settings.vector_store_type == "chroma":
                self.vector_store = Chroma.from_texts(
                    texts=all_chunks,
                    embedding=self.embeddings,
                    collection_name=collection_name,
                    persist_directory=str(settings.vector_store_path),
                )
            else:
                raise ValueError(f"Unsupported vector store: {settings.vector_store_type}")

            app_logger.info("Vector store created successfully")

        except Exception as e:
            app_logger.error(f"Error creating vector store: {e}")
            raise
    
    def load_vector_store(self, collection_name: str = "medical_reports") -> None:
        """Load existing vector store."""
        if not RAG_AVAILABLE:
            raise RuntimeError(
                "RAG dependencies not available. Please install: pip install langchain langchain-community chromadb sentence-transformers"
            )

        try:
            app_logger.info(f"Loading vector store: {collection_name}")

            if settings.vector_store_type == "chroma":
                self.vector_store = Chroma(
                    collection_name=collection_name,
                    embedding_function=self.embeddings,
                    persist_directory=str(settings.vector_store_path),
                )

            app_logger.info("Vector store loaded successfully")

        except Exception as e:
            app_logger.error(f"Error loading vector store: {e}")
            raise
    
    def retrieve_relevant_chunks(
        self,
        query: str,
        top_k: Optional[int] = None,
    ) -> List[str]:
        """Retrieve relevant document chunks for a query."""
        if not RAG_AVAILABLE:
            raise RuntimeError(
                "RAG dependencies not available. Please install: pip install langchain langchain-community chromadb sentence-transformers"
            )

        if self.vector_store is None:
            raise RuntimeError("Vector store not initialized")

        try:
            k = top_k or settings.top_k_retrieval
            app_logger.info(f"Retrieving top {k} chunks for query")

            # Perform similarity search
            results = self.vector_store.similarity_search(query, k=k)

            # Extract text from results
            chunks = [doc.page_content for doc in results]

            app_logger.info(f"Retrieved {len(chunks)} relevant chunks")
            return chunks

        except Exception as e:
            app_logger.error(f"Error retrieving chunks: {e}")
            raise
    
    def add_documents(self, documents: List[str]) -> None:
        """Add new documents to existing vector store."""
        if not RAG_AVAILABLE:
            raise RuntimeError(
                "RAG dependencies not available. Please install: pip install langchain langchain-community chromadb sentence-transformers"
            )

        if self.vector_store is None:
            raise RuntimeError("Vector store not initialized")

        try:
            app_logger.info(f"Adding {len(documents)} documents to vector store")

            # Split documents
            all_chunks = []
            for doc in documents:
                chunks = self.text_splitter.split_text(doc)
                all_chunks.extend(chunks)

            # Add to vector store
            self.vector_store.add_texts(all_chunks)

            app_logger.info("Documents added successfully")

        except Exception as e:
            app_logger.error(f"Error adding documents: {e}")
            raise

    def clear_vector_store(self) -> None:
        """Clear the vector store."""
        if self.vector_store:
            self.vector_store.delete_collection()
            self.vector_store = None
            app_logger.info("Vector store cleared")

    def is_available(self) -> bool:
        """Check if RAG dependencies are available."""
        return RAG_AVAILABLE


# Global vector store instance
vector_store_manager = VectorStoreManager()

