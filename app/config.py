"""Configuration management for the Medical Report Analysis API."""

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_workers: int = Field(default=4, description="Number of workers")
    api_reload: bool = Field(default=False, description="Auto-reload on code changes")
    
    # Model Configuration
    model_name: str = Field(
        default="google/medgemma-1.5-4b-it",
        description="HuggingFace model identifier"
    )
    model_cache_dir: Path = Field(
        default=Path("./models"),
        description="Directory to cache models"
    )
    model_device: Literal["cuda", "cpu", "mps"] = Field(
        default="cuda",
        description="Device for model inference"
    )
    model_quantization: Literal["4bit", "8bit", "none"] = Field(
        default="4bit",
        description="Model quantization strategy"
    )
    max_model_length: int = Field(
        default=2048,
        description="Maximum sequence length for model"
    )
    
    # RAG Configuration
    vector_store_type: Literal["chroma", "faiss"] = Field(
        default="chroma",
        description="Vector store backend"
    )
    vector_store_path: Path = Field(
        default=Path("./vector_store"),
        description="Path to vector store"
    )
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model for RAG"
    )
    chunk_size: int = Field(default=512, description="Text chunk size for RAG")
    chunk_overlap: int = Field(default=50, description="Overlap between chunks")
    top_k_retrieval: int = Field(default=5, description="Number of chunks to retrieve")
    
    # Processing Configuration
    max_file_size_mb: int = Field(default=50, description="Maximum file size in MB")
    supported_image_formats: str = Field(
        default="jpg,jpeg,png,tiff,dcm,nii,nii.gz",
        description="Supported image formats (including DICOM and NIfTI)"
    )
    supported_doc_formats: str = Field(
        default="pdf,txt",
        description="Supported document formats"
    )

    # MedGemma 1.5 4B specific settings
    max_images_longitudinal: int = Field(
        default=5,
        description="Maximum images for longitudinal comparison"
    )
    max_wsi_patches: int = Field(
        default=16,
        description="Maximum patches for whole-slide imaging"
    )
    image_max_size: int = Field(
        default=1024,
        description="Maximum dimension for image preprocessing"
    )
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Path = Field(default=Path("./logs/app.log"), description="Log file path")
    
    # Security
    api_key_enabled: bool = Field(default=False, description="Enable API key auth")
    api_key: str = Field(default="", description="API key for authentication")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create necessary directories
        self.model_cache_dir.mkdir(parents=True, exist_ok=True)
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    @property
    def supported_image_formats_list(self) -> list[str]:
        """Get list of supported image formats."""
        return [fmt.strip() for fmt in self.supported_image_formats.split(",")]
    
    @property
    def supported_doc_formats_list(self) -> list[str]:
        """Get list of supported document formats."""
        return [fmt.strip() for fmt in self.supported_doc_formats.split(",")]


# Global settings instance
settings = Settings()

