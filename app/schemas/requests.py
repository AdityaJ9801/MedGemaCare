"""Request schemas for API endpoints."""

from typing import Optional, List

from pydantic import BaseModel, Field


class TextSummaryRequest(BaseModel):
    """Request schema for text summarization."""

    text: str = Field(..., description="Medical report text to summarize")
    max_length: Optional[int] = Field(
        None,
        description="Maximum length of summary",
        ge=50,
        le=2048,
    )
    temperature: float = Field(
        default=0.7,
        description="Sampling temperature for generation",
        ge=0.1,
        le=1.0,
    )


class QuestionAnswerRequest(BaseModel):
    """Request schema for question answering."""

    text: str = Field(..., description="Medical report text")
    question: str = Field(..., description="Question to answer")


class RAGSummaryRequest(BaseModel):
    """Request schema for RAG-based summarization."""

    query: str = Field(
        default="Provide a comprehensive summary of the medical report",
        description="Query for retrieval",
    )
    top_k: Optional[int] = Field(
        None,
        description="Number of chunks to retrieve",
        ge=1,
        le=20,
    )


class RAGQuestionRequest(BaseModel):
    """Request schema for RAG-based question answering."""

    question: str = Field(..., description="Question to answer")
    top_k: Optional[int] = Field(
        None,
        description="Number of chunks to retrieve",
        ge=1,
        le=20,
    )


# ── MedGemma 1.5 4B New Capabilities ──────────────────────────────────────────

class ImageAnalysisRequest(BaseModel):
    """Request for medical image analysis (X-ray, CT, MRI, histopathology)."""
    query: str = Field(
        default="Describe this medical image in detail, including any abnormalities.",
        description="Analysis query/prompt"
    )


class LongitudinalAnalysisRequest(BaseModel):
    """Request for comparing multiple images over time."""
    query: str = Field(
        default="Compare these images and describe any changes or progression.",
        description="Comparison query"
    )


class LocalizationRequest(BaseModel):
    """Request for anatomical localization with bounding boxes."""
    query: str = Field(
        default="Identify and localize anatomical features and any abnormalities with bounding boxes.",
        description="Localization query"
    )


class LabExtractionRequest(BaseModel):
    """Request for extracting structured data from lab reports."""
    text: str = Field(..., description="Lab report text")


class EHRAnalysisRequest(BaseModel):
    """Request for EHR text analysis."""
    ehr_text: str = Field(..., description="Electronic Health Record text data")
    query: str = Field(
        default="Summarize the key clinical information including diagnoses, medications, and treatment plans.",
        description="Analysis query"
    )

