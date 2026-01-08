from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import CompositeElement, Image as UImage, Table
from PIL import Image
from langchain.schema.document import Document
import base64
from io import BytesIO
import os
import pickle
import uuid

from summaries import summariesData, summariesImages

# --- Minimum size to filter unwanted images ---
MIN_WIDTH = 700
MIN_HEIGHT = 200

# --- Convert base64 to PIL Image ---
def base64_to_pil(b64_str):
    if not b64_str:
        return None
    try:
        return Image.open(BytesIO(base64.b64decode(b64_str)))
    except Exception as e:
        print("Failed to convert image:", e)
        return None

# --- Convert PIL Image to base64 string ---
def pil_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

# --- Extract and filter images from chunks ---
def get_images_from_chunks(chunks):
    images_b64 = []
    images_pil = []
    for chunk in chunks:
        if isinstance(chunk, CompositeElement):
            for el in getattr(chunk.metadata, "orig_elements", []):
                if isinstance(el, UImage):
                    b64 = el.metadata.image_base64
                    img = base64_to_pil(b64)
                    if img:
                        w, h = img.size
                        if w >= MIN_WIDTH and h >= MIN_HEIGHT:
                            images_b64.append(b64)
                            images_pil.append(img)
    return images_b64, images_pil

# --- Chunk PDF and show filtered images ---
def chunking(file_path, show_images=True):
    print("Chunking PDF:", file_path)

    # chunks = partition_pdf(
    #     filename=file_path,
    #     infer_table_structure=True,
    #     strategy="hi_res",
    #     extract_image_block_types=["Image"],  # important to detect images
    #     extract_image_block_to_payload=True,
    #     chunking_strategy="by_title",
    #     max_characters=10000,
    #     combine_text_under_n_chars=2000,
    #     new_after_n_chars=6000,
    # )

    chunks = partition_pdf(
        filename=file_path,
        infer_table_structure=True,  # still extract tables
        strategy="hi_res",
        extract_image_block_types=[],  # no images
        extract_image_block_to_payload=False,
        chunking_strategy="by_title",
        max_characters=10000,
        combine_text_under_n_chars=2000,
        new_after_n_chars=6000,
           pages=5
    )

    images_b64, images_pil = get_images_from_chunks(chunks)
    print(f"Found {len(images_pil)} filtered images (>{MIN_WIDTH}x{MIN_HEIGHT}px)")

    # Optionally show images
    if show_images:
        for idx, img in enumerate(images_pil):
            print(f"Displaying image {idx+1}: size={img.size}")
            img.show()

    return chunks, images_b64, images_pil


chunks, images, imag = chunking("LevelDataPdfs/AssessmentGuideL1v2.pdf")
texts = []
tables = []
for chunk in chunks:
    if "Table" in str(type(chunk)):
        tables.append(chunk)
    elif "CompositeElement" in str(type(chunk)):
        texts.append(chunk)
for text_ele in texts:
    print("next chunk /n")
    print(text_ele.text)
    print("-------")
print("len , ",len(chunks))
print("len texts ", len(texts))