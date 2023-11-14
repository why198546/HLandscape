import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from pdfminer.high_level import extract_text
import pyperclip

def clean_text(text):
    # 去除多余的空白字符
    text = ' '.join(text.split())
    # 可以添加更多的清理步骤...
    return text

def ocr_files(folder_path):
    """
    Extracts text from images and PDFs in a folder and saves the cleaned text to separate text files.
    Also merges the cleaned text into a single file named 'merged.txt'.

    Args:
        folder_path (str): The path to the folder containing the images and PDFs.

    Returns:
        None
    """
    merged_text_path = os.path.join(folder_path, 'merged.txt')

    # Ensure the merged.txt file is empty before starting
    with open(merged_text_path, 'w', encoding='utf-8') as merged_file:
        merged_file.write('')

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        try:
            full_path = os.path.join(folder_path, filename)
            # Check if the file is an image
            if filename.lower().endswith((".jpg", ".png")):
                # Open the image file
                img = Image.open(full_path)
                # Perform OCR on the image
                text = pytesseract.image_to_string(img, lang='chi_sim')
                # Clean the extracted text
                cleaned_text = clean_text(text)
                # Write the cleaned text to a separate file
                text_filename = os.path.splitext(filename)[0] + ".txt"
                with open(os.path.join(folder_path, text_filename), "w", encoding='utf-8') as f:
                    f.write(cleaned_text)
                # Append the cleaned text to the merged file
                with open(merged_text_path, 'a', encoding='utf-8') as merged_file:
                    merged_file.write(cleaned_text + '\n')

            # Check if the file is a PDF
            elif filename.lower().endswith(".pdf"):
                # Extract text from PDF using pdfminer.six
                text = extract_text(full_path)
                # Clean the extracted text
                cleaned_text = clean_text(text)

                # If no text is extracted, assume it's a scanned document and use OCR
                if not cleaned_text.strip():
                    images = convert_from_path(full_path)
                    cleaned_text = ''.join([clean_text(pytesseract.image_to_string(image, lang='chi_sim')) for image in images])

                # Write the cleaned text to a separate file
                text_filename = os.path.splitext(filename)[0] + ".txt"
                with open(os.path.join(folder_path, text_filename), "w", encoding='utf-8') as f:
                    f.write(cleaned_text)
                # Append the cleaned text to the merged file
                with open(merged_text_path, 'a', encoding='utf-8') as merged_file:
                    merged_file.write(cleaned_text + '\n')

        except Exception as e:
            print(f"An error occurred with file {filename}: {e}")

if __name__ == "__main__":
    # Set the path to the folder containing the files to be processed
    folder_path = pyperclip.paste()
    ocr_files(folder_path)
