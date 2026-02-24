"""API route definitions for MedGemma 1.5 4B Medical AI."""

import tempfile
from pathlib import Path
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image

from app import __version__
from app.models.model_loader import model_loader
from app.processors.document_processor import DocumentProcessor
from app.processors.image_processor import ImageProcessor
from app.rag.rag_pipeline import rag_pipeline
from app.schemas.requests import (
    EHRAnalysisRequest,
    ImageAnalysisRequest,
    LabExtractionRequest,
    LocalizationRequest,
    LongitudinalAnalysisRequest,
    QuestionAnswerRequest,
    RAGQuestionRequest,
    RAGSummaryRequest,
    TextSummaryRequest,
)
from app.schemas.responses import (
    AnswerResponse,
    DocumentUploadResponse,
    EHRAnalysisResponse,
    ErrorResponse,
    HealthResponse,
    ImageAnalysisResponse,
    LabExtractionResponse,
    LocalizationResponse,
    LongitudinalAnalysisResponse,
    RAGAnswerResponse,
    SummaryResponse,
)
from app.utils.logger import app_logger

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model_loaded=model_loader.is_loaded() if model_loader.is_available() else False,
        version=__version__,
        ml_available=model_loader.is_available(),
    )


@router.post("/summarize", response_model=SummaryResponse)
async def summarize_text(request: TextSummaryRequest):
    """Generate summary from medical report text."""
    try:
        app_logger.info("Received summarization request")

        # Check if ML dependencies are available
        if not model_loader.is_available():
            raise HTTPException(
                status_code=503,
                detail="ML dependencies not available. Install: pip install torch transformers accelerate"
            )

        # Ensure model is loaded
        if not model_loader.is_loaded():
            model_loader.load_model()

        # Generate summary
        summary = model_loader.generate_summary(
            text=request.text,
            max_length=request.max_length,
            temperature=request.temperature,
        )

        return SummaryResponse(
            summary=summary,
            input_length=len(request.text),
            summary_length=len(summary),
        )

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error in summarization: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze", response_model=AnswerResponse)
async def analyze_report(request: QuestionAnswerRequest):
    """Analyze medical report and answer specific question."""
    try:
        app_logger.info("Received analysis request")

        # Check if ML dependencies are available
        if not model_loader.is_available():
            raise HTTPException(
                status_code=503,
                detail="ML dependencies not available. Install: pip install torch transformers accelerate"
            )

        # Ensure model is loaded
        if not model_loader.is_loaded():
            model_loader.load_model()

        # Generate answer
        answer = model_loader.analyze_report(
            text=request.text,
            query=request.question,
        )

        return AnswerResponse(
            question=request.question,
            answer=answer,
        )

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error in analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/document", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process medical document (PDF, TXT)."""
    try:
        app_logger.info(f"Received document upload: {file.filename}")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Validate file size
            DocumentProcessor.validate_file_size(tmp_path)

            # Process document
            text = DocumentProcessor.process_document(tmp_path)

            # Index with RAG
            rag_pipeline.process_large_document(text)

            return DocumentUploadResponse(
                filename=file.filename,
                file_size=len(content),
                format=Path(file.filename).suffix.lstrip("."),
                processed=True,
                message="Document processed and indexed successfully",
            )

        finally:
            # Clean up temp file
            Path(tmp_path).unlink(missing_ok=True)

    except Exception as e:
        app_logger.error(f"Error processing document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/image", response_model=DocumentUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """Upload and process medical image."""
    try:
        app_logger.info(f"Received image upload: {file.filename}")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Process image and extract text
            text = ImageProcessor.extract_text_from_image(tmp_path)

            # Index with RAG if text extracted
            if text.strip():
                rag_pipeline.process_large_document(text)
                message = "Image processed and text indexed successfully"
            else:
                message = "Image processed but no text extracted"

            return DocumentUploadResponse(
                filename=file.filename,
                file_size=len(content),
                format=Path(file.filename).suffix.lstrip("."),
                processed=True,
                message=message,
            )

        finally:
            # Clean up temp file
            Path(tmp_path).unlink(missing_ok=True)

    except Exception as e:
        app_logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rag/summarize", response_model=SummaryResponse)
async def rag_summarize(request: RAGSummaryRequest):
    """Generate summary using RAG for large documents."""
    try:
        app_logger.info("Received RAG summarization request")

        # Check if ML dependencies are available
        if not model_loader.is_available():
            raise HTTPException(
                status_code=503,
                detail="ML dependencies not available. Install: pip install torch transformers accelerate"
            )

        # Ensure model is loaded
        if not model_loader.is_loaded():
            model_loader.load_model()

        # Generate summary with RAG
        summary = rag_pipeline.generate_summary_with_rag(
            query=request.query,
            top_k=request.top_k,
        )

        return SummaryResponse(
            summary=summary,
            input_length=0,  # Not applicable for RAG
            summary_length=len(summary),
        )

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error in RAG summarization: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rag/question", response_model=RAGAnswerResponse)
async def rag_question(request: RAGQuestionRequest):
    """Answer question using RAG for large documents."""
    try:
        app_logger.info("Received RAG question request")

        # Check if ML dependencies are available
        if not model_loader.is_available():
            raise HTTPException(
                status_code=503,
                detail="ML dependencies not available. Install: pip install torch transformers accelerate"
            )

        # Ensure model is loaded
        if not model_loader.is_loaded():
            model_loader.load_model()

        # Answer question with RAG
        result = rag_pipeline.answer_question_with_rag(
            question=request.question,
            top_k=request.top_k,
        )

        return RAGAnswerResponse(
            question=result["question"],
            answer=result["answer"],
            num_chunks_used=result["num_chunks_used"],
            relevant_chunks=result["relevant_chunks"],
        )

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error in RAG question answering: {e}")
        raise HTTPException(status_code=500, detail=str(e))



# ══════════════════════════════════════════════════════════════════════════════
# MedGemma 1.5 4B NEW CAPABILITIES
# ══════════════════════════════════════════════════════════════════════════════

def _ensure_model():
    """Helper to check ML availability and load model."""
    if not model_loader.is_available():
        raise HTTPException(
            status_code=503,
            detail="ML dependencies not available. Install: pip install torch transformers accelerate"
        )
    if not model_loader.is_loaded():
        model_loader.load_model()


@router.post("/analyze/image", response_model=ImageAnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    query: str = "Describe this medical image in detail, including any abnormalities."
):
    """Analyze medical image (X-ray, CT slice, MRI slice, histopathology)."""
    try:
        app_logger.info(f"Received image analysis request: {file.filename}")
        _ensure_model()

        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            image_data = ImageProcessor.process_image(tmp_path)
            image = ImageProcessor.preprocess_for_model(image_data["image"])
            analysis = model_loader.analyze_image(image, query)

            return ImageAnalysisResponse(
                analysis=analysis,
                image_type=image_data["metadata"].get("format", "unknown"),
                filename=file.filename,
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error in image analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/longitudinal", response_model=LongitudinalAnalysisResponse)
async def analyze_longitudinal(
    files: List[UploadFile] = File(...),
    query: str = "Compare these images and describe any changes or progression over time."
):
    """Compare multiple medical images for longitudinal analysis."""
    try:
        app_logger.info(f"Received longitudinal analysis request: {len(files)} images")
        _ensure_model()

        if len(files) < 2:
            raise HTTPException(status_code=400, detail="At least 2 images required for comparison")

        images = []
        filenames = []
        tmp_paths = []

        try:
            for f in files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(f.filename).suffix) as tmp:
                    content = await f.read()
                    tmp.write(content)
                    tmp_paths.append(tmp.name)

                image_data = ImageProcessor.process_image(tmp_paths[-1])
                images.append(ImageProcessor.preprocess_for_model(image_data["image"]))
                filenames.append(f.filename)

            analysis = model_loader.analyze_images_longitudinal(images, query)

            return LongitudinalAnalysisResponse(
                analysis=analysis,
                num_images=len(images),
                filenames=filenames,
            )
        finally:
            for p in tmp_paths:
                Path(p).unlink(missing_ok=True)

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error in longitudinal analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/localize/anatomy", response_model=LocalizationResponse)
async def localize_anatomy(
    file: UploadFile = File(...),
    query: str = "Identify and localize anatomical features and any abnormalities with bounding boxes."
):
    """Localize anatomical features in chest X-ray with bounding boxes."""
    try:
        app_logger.info(f"Received localization request: {file.filename}")
        _ensure_model()

        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            image_data = ImageProcessor.process_image(tmp_path)
            image = ImageProcessor.preprocess_for_model(image_data["image"])
            result = model_loader.localize_anatomy(image, query)

            return LocalizationResponse(
                raw_response=result["raw_response"],
                image_size=result["image_size"],
                filename=file.filename,
            )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error in localization: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract/lab", response_model=LabExtractionResponse)
async def extract_lab_data(request: LabExtractionRequest):
    """Extract structured data from lab report text."""
    try:
        app_logger.info("Received lab extraction request")
        _ensure_model()

        result = model_loader.extract_lab_data(request.text)

        return LabExtractionResponse(
            raw_response=result["raw_response"],
            input_length=result["input_length"],
        )

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error in lab extraction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/ehr", response_model=EHRAnalysisResponse)
async def analyze_ehr(request: EHRAnalysisRequest):
    """Analyze electronic health record text data."""
    try:
        app_logger.info("Received EHR analysis request")
        _ensure_model()

        analysis = model_loader.analyze_ehr(request.ehr_text, request.query)

        return EHRAnalysisResponse(
            analysis=analysis,
            input_length=len(request.ehr_text),
        )

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error in EHR analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))
