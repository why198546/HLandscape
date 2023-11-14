import os
from PIL import Image
import pytesseract
import pyperclip

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

    # create a new file to store the merged text
    merged_text_path = os.path.join(folder_path, 'merged_text.txt')

    # write the merged text to the file
    with open(merged_text_path, 'w', encoding='utf-8') as f:
        f.write(all_text)

if __name__ == '__main__':
    # set the path of the folder containing the images
    folder_path = pyperclip.paste()
    recognize_text_in_folder(folder_path)
