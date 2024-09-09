from io import BytesIO
from typing import List

from src.schemas.types import ImageInfo, Metadata
from lib.clients.chromadb_service import get_image_collection

from PIL import Image
import torch
from transformers import AutoProcessor, CLIPModel
import requests

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load processor and model
processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)


class ImageResolver:
    @staticmethod
    def search_images(query: str, limit: int = 10) -> List[ImageInfo]:
        collection = get_image_collection()
        if not collection:
            return []

        results = collection.query(
            query_texts=[query],
            n_results=limit,
            include=["metadatas", "documents"]
        )

        image_infos = []
        for i, id in enumerate(results["ids"][0]):
            metadatas = results["metadatas"]
            distances = results["distances"]

            if not metadatas or metadatas[0][i] or not distances or distances[0][i]:
                continue

            metadata = metadatas[0][i]
            similarity = 1 - distances[0][i]  # Convert distance to similarity
            image_infos.append(
                ImageInfo(
                    id=id,
                    metadata=Metadata(**metadata.__dict__),
                    similarity=similarity
                )
            )

        return image_infos

    @staticmethod
    def save_image_info(
        id: str,
        embedding: List[float],
        metadata: Metadata
    ) -> bool:
        collection = get_image_collection()
        if not collection:
            return False

        try:
            collection.upsert(
                ids=[id], embeddings=[embedding], metadatas=[metadata.__dict__]
            )
            return True
        except Exception as e:
            print(f"Error saving image info: {e}")
            return False

    @staticmethod
    def image_to_embedding(image_bytes: BytesIO) -> List[float]:
        image = ImageResolver.load_image_PIL(image_bytes)
        inputs = processor(images=image, return_tensors="pt").to(device)

        # Generate the embedding
        with torch.no_grad():
            outputs = model.get_image_features(**inputs)

        # Convert the tensor to a numpy array
        image_embedding = outputs.cpu().numpy().flatten()

        return image_embedding

    @staticmethod
    def load_image_PIL(url_or_path):
        if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
            return Image.open(requests.get(url_or_path, stream=True).raw)
        else:
            return Image.open(url_or_path)
