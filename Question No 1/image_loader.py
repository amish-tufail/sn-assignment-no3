import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

class ImageEditor:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Image Editor")
        self.root.geometry("800x600")
        
        # Variables to store image data
        self.original_image = None
        self.display_image = None
        
        # Create the user interface
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI elements"""
        
        # Main frame to hold all widgets
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weight for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Control panel on the left
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Load image button
        self.load_button = ttk.Button(control_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=5, fill=tk.X)
        
        # Status label to show current operation
        self.status_label = ttk.Label(control_frame, text="No image loaded")
        self.status_label.pack(pady=5)
        
        # Image display area
        self.image_frame = ttk.LabelFrame(main_frame, text="Original Image", padding="5")
        self.image_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas to display the image
        self.image_canvas = tk.Canvas(self.image_frame, bg="white", width=500, height=400)
        self.image_canvas.pack(expand=True, fill=tk.BOTH)
        
    def load_image(self):
        """Load an image from the local device"""
        
        # Open file dialog to select image
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        # Check if user selected a file
        if not file_path:
            return
            
        try:
            # Load image using OpenCV
            self.original_image = cv2.imread(file_path)
            
            if self.original_image is None:
                messagebox.showerror("Error", "Could not load the selected image file.")
                return
            
            # Convert BGR to RGB for proper display
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            
            # Display the loaded image
            self.display_loaded_image()
            
            # Update status
            self.status_label.config(text=f"Image loaded: {file_path.split('/')[-1]}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def display_loaded_image(self):
        """Display the loaded image on the canvas"""
        
        if self.original_image is None:
            return
        
        # Get canvas dimensions
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        # If canvas hasn't been drawn yet, use default size
        if canvas_width <= 1:
            canvas_width = 500
        if canvas_height <= 1:
            canvas_height = 400
        
        # Get image dimensions
        img_height, img_width = self.original_image.shape[:2]
        
        # Calculate scaling factor to fit image in canvas while maintaining aspect ratio
        scale_x = (canvas_width - 20) / img_width
        scale_y = (canvas_height - 20) / img_height
        scale = min(scale_x, scale_y, 1.0)  # Don't scale up, only down
        
        # Calculate new dimensions
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Resize image for display
        resized_image = cv2.resize(self.original_image, (new_width, new_height))
        
        # Convert to PIL Image and then to PhotoImage for Tkinter
        pil_image = Image.fromarray(resized_image)
        self.display_image = ImageTk.PhotoImage(pil_image)
        
        # Clear canvas and display image
        self.image_canvas.delete("all")
        
        # Center the image on canvas
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        
        self.image_canvas.create_image(x, y, anchor=tk.NW, image=self.display_image)
        
        # Store image position and size for later use
        self.display_x = x
        self.display_y = y
        self.display_width = new_width
        self.display_height = new_height
        self.display_scale = scale
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Create and run the application
if __name__ == "__main__":
    app = ImageEditor()
    app.run()