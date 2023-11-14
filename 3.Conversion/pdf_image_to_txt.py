import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import pyperclip
def pdf_to_text(PDF_file):
    # Store all the pages of the PDF in a variable
    pages = convert_from_path(PDF_file, 500)

    # Variable to get count of total number of pages
    filelimit = len(pages)

    # Creating a text file to write the output
    outfile = os.path.splitext(PDF_file)[0] + ".txt"

    # Open the file in append mode so that
    # All contents of all images are added to the same file
    with open(outfile, 'w', encoding='utf-8') as f:
        for i in range(1, filelimit + 1):
                # Recognize the text as string in image using pytesserct
                text = str(((pytesseract.image_to_string(pages[i-1]))))

                # The recognized text is stored in variable text
                # Any string processing may be applied on text
                # Here, basic formatting has been done:
                # In many PDFs, at line ending, if a word can't
                # be written fully, a 'hyphen' is added.
                # The rest of the word is written in the next line
                # Eg: This is a sample text this word here GeeksF-
                # orGeeks is half on first line, remaining on next.
                # To remove this, we replace every '-\n' to ''.
                text = text.replace('-\n', '')

                f.write(text)

def is_scanned_pdf(pdf_file):
    # Check if the file exists
    if not os.path.isfile(pdf_file):
        return False

    # Check if the file is a PDF
    if not pdf_file.lower().endswith('.pdf'):
        return False

    # Try to extract text from the PDF
    with open(pdf_file, 'rb') as f:
        reader = PdfReader(f)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        
        # If no text could be extracted, the PDF is likely scanned
        if not text.strip():
            return True

    return False
def recognize_text_in_folder(folder_path):
    # initialize an empty string to store the recognized text from all images
    all_text = ''

    # loop through all files in the folder
    for filename in os.listdir(folder_path):
        # check if the file is an image file
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # open the image file
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)

            # recognize the text in the image
            text = pytesseract.image_to_string(image, lang='chi_sim')

            # append the recognized text to the all_text string
            all_text += text + '\n'

            # create a new file with the same name as the image file, but with .txt extension
            text_path = os.path.join(folder_path, os.path.splitext(filename)[0] + '.txt')

            # write the recognized text to the text file
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text)
    # # create a new file to store the merged text
    # merged_text_path = os.path.join(folder_path, 'merged_text.txt')

    # # write the merged text to the file
    # with open(merged_text_path, 'w', encoding='utf-8') as f:
    #     f.write(all_text)
if __name__ == '__main__':
    # set the path of the folder containing the images
    folder_path = pyperclip.paste()
    recognize_text_in_folder(folder_path)

    # Iterate through all the files in the folder
    for file_name in os.listdir(folder_path):
        # Check if the file is a scanned PDF
        if is_scanned_pdf(os.path.join(folder_path, file_name)):
            print(f"{file_name} is a scanned PDF")
            pdf_to_text(os.path.join(folder_path, file_name))
        else:
            print(f"{file_name} is not a scanned PDF")
            # Export text from the PDF
            with open(os.path.join(folder_path, file_name), 'rb') as f:
                reader = PdfReader(f)
                text = ""
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()
            
            # Write the text to a file
            with open(os.path.splitext(os.path.join(folder_path, file_name))[0] + ".txt", 'w', encoding='utf-8') as f:
                f.write(text)

    # Merge all the text files into a single file
    with open(os.path.join(folder_path, "all_text.txt"), 'w', encoding='utf-8') as outfile:
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                with open(os.path.join(folder_path, file_name), 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
