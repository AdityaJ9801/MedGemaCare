"""Tests for document and image processors."""

import tempfile
from pathlib import Path

import pytest

from app.processors.document_processor import DocumentProcessor


def test_process_text_file():
    """Test text file processing."""
    # Create temporary text file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("This is a test medical report.\nPatient: John Doe\nDiagnosis: Common cold")
        temp_path = f.name
    
    try:
        text = DocumentProcessor.process_text(temp_path)
        assert "test medical report" in text
        assert "John Doe" in text
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_validate_file_size():
    """Test file size validation."""
    # Create small file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("Small file")
        temp_path = f.name
    
    try:
        result = DocumentProcessor.validate_file_size(temp_path)
        assert result is True
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_unsupported_format():
    """Test handling of unsupported file format."""
    with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
        temp_path = f.name
    
    try:
        with pytest.raises(ValueError, match="Unsupported document format"):
            DocumentProcessor.process_document(temp_path)
    finally:
        Path(temp_path).unlink(missing_ok=True)

