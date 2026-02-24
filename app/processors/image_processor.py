"""Image processing for MedGemma 1.5 4B medical imaging analysis.

Supports:
- Standard 2D images (X-ray, photos)
- CT/MRI slices (from DICOM/NIfTI)
- Histopathology patches
- Multiple image formats
"""

from pathlib import Path
from typing import Union, List

from PIL import Image

from app.config import settings
from app.utils.logger import app_logger


class ImageProcessor:
    """Process medical images for MedGemma 1.5 4B analysis."""

    @staticmethod
    def process_image(file_path: Union[str, Path]) -> dict:
        """Load and validate medical image."""
        try:
            app_logger.info(f"Processing image: {file_path}")
            path = Path(file_path)
            extension = path.suffix.lower().lstrip(".")

            # Handle different formats
            if extension in ("dcm", "dicom"):
                return ImageProcessor._process_dicom(path)
            elif extension in ("nii", "gz") or str(path).endswith(".nii.gz"):
                return ImageProcessor._process_nifti(path)
            elif extension not in settings.supported_image_formats_list:
                raise ValueError(
                    f"Unsupported image format: {extension}. "
                    f"Supported: {settings.supported_image_formats}"
                )

            # Standard image loading
            image = Image.open(path)
            metadata = {
                "format": image.format or extension.upper(),
                "mode": image.mode,
                "size": image.size,
                "width": image.width,
                "height": image.height,
                "type": "standard",
            }

            app_logger.info(f"Image loaded: {metadata}")
            return {"image": image, "metadata": metadata, "path": str(path)}

        except Exception as e:
            app_logger.error(f"Error processing image: {e}")
            raise ValueError(f"Failed to process image: {str(e)}")

    @staticmethod
    def _process_dicom(path: Path) -> dict:
        """Process DICOM file for CT/MRI analysis."""
        try:
            import pydicom
            from PIL import Image
            import numpy as np

            ds = pydicom.dcmread(str(path))
            arr = ds.pixel_array.astype(float)

            # Normalize to 0-255
            arr = ((arr - arr.min()) / (arr.max() - arr.min() + 1e-8) * 255).astype("uint8")
            image = Image.fromarray(arr)
            if image.mode != "RGB":
                image = image.convert("RGB")

            metadata = {
                "format": "DICOM",
                "mode": image.mode,
                "size": image.size,
                "width": image.width,
                "height": image.height,
                "type": "dicom",
                "modality": getattr(ds, "Modality", "Unknown"),
            }

            app_logger.info(f"DICOM loaded: {metadata}")
            return {"image": image, "metadata": metadata, "path": str(path)}

        except ImportError:
            raise ValueError("DICOM support requires: pip install pydicom")
        except Exception as e:
            raise ValueError(f"Failed to process DICOM: {str(e)}")

    @staticmethod
    def _process_nifti(path: Path) -> dict:
        """Process NIfTI file (CT/MRI volumes) - returns middle slice."""
        try:
            import nibabel as nib
            import numpy as np

            nii = nib.load(str(path))
            data = nii.get_fdata()

            # Get middle slice from largest dimension
            mid = data.shape[2] // 2
            slice_2d = data[:, :, mid].astype(float)

            # Normalize
            slice_2d = ((slice_2d - slice_2d.min()) / (slice_2d.max() - slice_2d.min() + 1e-8) * 255).astype("uint8")
            image = Image.fromarray(slice_2d).convert("RGB")

            metadata = {
                "format": "NIfTI",
                "mode": image.mode,
                "size": image.size,
                "width": image.width,
                "height": image.height,
                "type": "nifti",
                "volume_shape": data.shape,
                "slice_index": mid,
            }

            app_logger.info(f"NIfTI loaded: {metadata}")
            return {"image": image, "metadata": metadata, "path": str(path)}

        except ImportError:
            raise ValueError("NIfTI support requires: pip install nibabel")
        except Exception as e:
            raise ValueError(f"Failed to process NIfTI: {str(e)}")

    @staticmethod
    def preprocess_for_model(image: Image.Image) -> Image.Image:
        """Preprocess image for MedGemma model input."""
        # Convert to RGB
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Resize if too large
        max_size = settings.image_max_size
        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        return image

    @staticmethod
    def create_wsi_patches(image: Image.Image, patch_size: int = 256) -> List[Image.Image]:
        """Create patches from whole-slide histopathology image."""
        patches = []
        w, h = image.size
        max_patches = settings.max_wsi_patches

        for y in range(0, h - patch_size + 1, patch_size):
            for x in range(0, w - patch_size + 1, patch_size):
                if len(patches) >= max_patches:
                    break
                patch = image.crop((x, y, x + patch_size, y + patch_size))
                patches.append(ImageProcessor.preprocess_for_model(patch))
            if len(patches) >= max_patches:
                break

        app_logger.info(f"Created {len(patches)} WSI patches")
        return patches

