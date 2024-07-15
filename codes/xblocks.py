import os
import win32com.client
import pythoncom
import time
import pyperclip

def explode_blocks_in_dwg(file_path):
    # Initialize AutoCAD application
    acad = win32com.client.Dispatch("AutoCAD.Application")
    acad.Visible = True
    doc = acad.Documents.Open(file_path)
    
    # Wait to ensure the document is fully loaded
    time.sleep(1)

    # Create a new selection set
    selection_set_name = "MyBlockSelectionSet"
    try:
        selection_set = doc.SelectionSets.Item(selection_set_name)
        selection_set.Clear()
    except Exception:
        try:
            selection_set = doc.SelectionSets.Add(selection_set_name)
        except Exception as e:
            print(f"Error creating selection set: {str(e)}")
            return

    # Define selection criteria to select all block references
    filter_type = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_I2, [0])
    filter_data = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, ['INSERT'])

    # Select all block references automatically
    try:
        selection_set.Select(5, filter_type, filter_data)  # 5 - SelectAll
    except Exception as e:
        print(f"Error selecting blocks: {str(e)}")
        return

    # Send command to explode the selected blocks
    for i in range(selection_set.Count):
        for attempt in range(3):  # Retry up to 3 times
            try:
                entity = selection_set.Item(i)
                if entity.ObjectName == 'AcDbBlockReference':
                    handle = entity.Handle
                    doc.SendCommand(f'_.SELECT _Handle {handle} _EXPLODE _P\n\n')
                    time.sleep(0.1)  # Allow some time for the command to execute
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} - Error exploding entity: {str(e)}")
                time.sleep(0.5)  # Wait a bit before retrying
                if attempt == 2:
                    print(f"Skipping entity after 3 failed attempts: Handle {entity.Handle if 'entity' in locals() else 'unknown'}")

    # Clear selection set
    selection_set.Clear()
    
    # Save and close the document
    doc.Save()
    doc.Close()

def process_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.dwg'):
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_path}")
            explode_blocks_in_dwg(file_path)
            time.sleep(0.5)

# Specify the folder containing the DWG files
# folder_path = r"C:\Users\why19\Desktop\献给敬爱的张总"
if __name__ == "__main__":
    folder_path = r"C:\Users\why19\Desktop\献给敬爱的张总"
    process_folder(folder_path)
