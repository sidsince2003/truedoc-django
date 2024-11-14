# utils.py
import pytesseract
from PIL import Image
import io
# utils.py

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def perform_ocr(file_data, file_extension):
    """
    Perform OCR (Optical Character Recognition) on the given document data.
    
    :param file_data: The binary data of the document file
    :param file_extension: The extension of the document (for file type detection)
    :return: Extracted text from the document
    """
    # Check if the file is an image or PDF. We will assume the file extension determines the type.
    if file_extension in ['jpg', 'jpeg', 'png']:
        # If it's an image, we process it using pytesseract
        image = Image.open(io.BytesIO(file_data))
        extracted_text = pytesseract.image_to_string(image)
    elif file_extension == 'pdf':
        # For PDF files, you can add PDF parsing logic if required.
        # Alternatively, use a library like PyPDF2 for text extraction or OCR on each page of the PDF.
        extracted_text = "PDF OCR functionality not implemented."
    else:
        extracted_text = "Unsupported file type for OCR."
    
    return extracted_text
