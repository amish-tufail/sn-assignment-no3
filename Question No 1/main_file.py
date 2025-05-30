
# Main file which includes all other things and two files

import tkinter as tk
from gui_components import ImageEditorGUI
from image_processor import ImageProcessor

class ImageEditor:
    def __init__(self):
        # this initialize  main window
        self.root = tk.Tk()
        self.root.title("Image Editor")
        self.root.geometry("1200x800")
        
        # initialize image processor
        self.processor = ImageProcessor()
        
        # initialize UI
        self.gui = ImageEditorGUI(self.root, self.processor)
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

# run the application
if __name__ == "__main__":
    app = ImageEditor()
    app.run()