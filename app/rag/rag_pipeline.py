"""RAG pipeline for enhanced medical report analysis."""

from typing import List, Optional

from app.models.model_loader import model_loader
from app.rag.vector_store import vector_store_manager
from app.utils.logger import app_logger


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline for medical reports."""
    
    def __init__(self):
        self.vector_store = vector_store_manager
        self.model = model_loader
    
    def process_large_document(
        self,
        document: str,
        collection_name: str = "medical_reports",
    ) -> None:
        """Process and index a large medical document."""
        try:
            app_logger.info("Processing large document with RAG")
            
            # Create vector store from document
            self.vector_store.create_vector_store(
                documents=[document],
                collection_name=collection_name,
            )
            
            app_logger.info("Document indexed successfully")
            
        except Exception as e:
            app_logger.error(f"Error processing large document: {e}")
            raise
    
    def generate_summary_with_rag(
        self,
        query: str = "Provide a comprehensive summary of the medical report",
        top_k: Optional[int] = None,
    ) -> str:
        """Generate summary using RAG approach."""
        try:
            app_logger.info("Generating summary with RAG")
            
            # Retrieve relevant chunks
            relevant_chunks = self.vector_store.retrieve_relevant_chunks(
                query=query,
                top_k=top_k,
            )
            
            # Combine chunks into context
            context = "\n\n".join(relevant_chunks)
            
            # Generate summary using model
            summary = self.model.generate_summary(context)
            
            app_logger.info("Summary generated successfully")
            return summary
            
        except Exception as e:
            app_logger.error(f"Error generating summary with RAG: {e}")
            raise
    
    def answer_question_with_rag(
        self,
        question: str,
        top_k: Optional[int] = None,
    ) -> dict:
        """Answer specific question about medical report using RAG."""
        try:
            app_logger.info(f"Answering question with RAG: {question}")
            
            # Retrieve relevant chunks
            relevant_chunks = self.vector_store.retrieve_relevant_chunks(
                query=question,
                top_k=top_k,
            )
            
            # Combine chunks into context
            context = "\n\n".join(relevant_chunks)
            
            # Generate answer using model
            answer = self.model.analyze_report(context, question)
            
            app_logger.info("Answer generated successfully")
            
            return {
                "question": question,
                "answer": answer,
                "relevant_chunks": relevant_chunks,
                "num_chunks_used": len(relevant_chunks),
            }
            
        except Exception as e:
            app_logger.error(f"Error answering question with RAG: {e}")
            raise
    
    def batch_process_documents(
        self,
        documents: List[str],
        collection_name: str = "medical_reports",
    ) -> None:
        """Process multiple documents and add to vector store."""
        try:
            app_logger.info(f"Batch processing {len(documents)} documents")
            
            # Create or update vector store
            self.vector_store.create_vector_store(
                documents=documents,
                collection_name=collection_name,
            )
            
            app_logger.info("Batch processing completed")
            
        except Exception as e:
            app_logger.error(f"Error in batch processing: {e}")
            raise


# Global RAG pipeline instance
rag_pipeline = RAGPipeline()

