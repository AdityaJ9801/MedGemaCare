"""Document processing for medical reports, lab data, and EHR.

Supports:
- PDF and TXT documents
- Lab report text processing
- EHR data preprocessing
"""

from pathlib import Path
from typing import Union, Dict, Any
import re

from pypdf import PdfReader

from app.config import settings
from app.utils.logger import app_logger


class DocumentProcessor:
    """Process text-based medical documents."""

    @staticmethod
    def process_pdf(file_path: Union[str, Path]) -> str:
        """Extract text from PDF file."""
        try:
            app_logger.info(f"Processing PDF: {file_path}")
            reader = PdfReader(file_path)

            text_content = []
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text.strip():
                    text_content.append(f"--- Page {page_num} ---\n{text}")

            full_text = "\n\n".join(text_content)
            app_logger.info(f"Extracted {len(full_text)} characters from PDF")
            return full_text

        except Exception as e:
            app_logger.error(f"Error processing PDF: {e}")
            raise ValueError(f"Failed to process PDF: {str(e)}")

    @staticmethod
    def process_text(file_path: Union[str, Path]) -> str:
        """Read text from TXT file."""
        try:
            app_logger.info(f"Processing text file: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            app_logger.info(f"Read {len(text)} characters from text file")
            return text

        except Exception as e:
            app_logger.error(f"Error processing text file: {e}")
            raise ValueError(f"Failed to process text file: {str(e)}")

    @staticmethod
    def process_document(file_path: Union[str, Path]) -> str:
        """Process document based on file extension."""
        path = Path(file_path)
        extension = path.suffix.lower().lstrip(".")

        if extension == "pdf":
            return DocumentProcessor.process_pdf(path)
        elif extension == "txt":
            return DocumentProcessor.process_text(path)
        else:
            raise ValueError(
                f"Unsupported document format: {extension}. "
                f"Supported formats: {settings.supported_doc_formats}"
            )

    @staticmethod
    def validate_file_size(file_path: Union[str, Path]) -> bool:
        """Validate file size is within limits."""
        path = Path(file_path)
        size_mb = path.stat().st_size / (1024 * 1024)

        if size_mb > settings.max_file_size_mb:
            raise ValueError(
                f"File size ({size_mb:.2f} MB) exceeds maximum allowed "
                f"size ({settings.max_file_size_mb} MB)"
            )

        return True

    @staticmethod
    def preprocess_lab_report(text: str) -> str:
        """Clean and preprocess lab report text for extraction."""
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        # Preserve line breaks for tabular data
        text = re.sub(r'(\d)\s+([A-Za-z])', r'\1\n\2', text)
        app_logger.info(f"Preprocessed lab report: {len(text)} chars")
        return text.strip()

    @staticmethod
    def preprocess_ehr(text: str) -> str:
        """Clean and preprocess EHR text data."""
        # Remove excessive whitespace while preserving structure
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned = '\n'.join(lines)
        app_logger.info(f"Preprocessed EHR: {len(cleaned)} chars")
        return cleaned

