import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

class ImageEditor:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Image Editor - Step 3: Cropping & Resizing")
        self.root.geometry("1200x800")
        
        # Variables to store image data
        self.original_image = None
        self.cropped_image = None
        self.resized_image = None
        self.display_image = None
        self.cropped_display_image = None
        self.resized_display_image = None
        
        # Variables for cropping functionality
        self.is_cropping = False
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.crop_rectangle = None
        
        # Variables to store display properties
        self.display_x = 0
        self.display_y = 0
        self.display_width = 0
        self.display_height = 0
        self.display_scale = 1.0
        
        # Variables for resizing functionality
        self.current_resize_scale = 1.0
        self.original_cropped_width = 0
        self.original_cropped_height = 0
        
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
        main_frame.columnconfigure(2, weight=1)
        main_frame.columnconfigure(3, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Control panel on the left
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Load image button
        self.load_button = ttk.Button(control_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=5, fill=tk.X)
        
        # Separator
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Cropping controls section
        crop_label = ttk.Label(control_frame, text="CROPPING CONTROLS", font=('Arial', 9, 'bold'))
        crop_label.pack(pady=(0, 5))
        
        # Crop button
        self.crop_button = ttk.Button(control_frame, text="Enable Cropping", 
                                     command=self.toggle_cropping, state="disabled")
        self.crop_button.pack(pady=2, fill=tk.X)
        
        # Apply crop button
        self.apply_crop_button = ttk.Button(control_frame, text="Apply Crop", 
                                           command=self.apply_crop, state="disabled")
        self.apply_crop_button.pack(pady=2, fill=tk.X)
        
        # Separator
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Resizing controls section
        resize_label = ttk.Label(control_frame, text="RESIZING CONTROLS", font=('Arial', 9, 'bold'))
        resize_label.pack(pady=(0, 5))
        
        # Resize scale label
        self.resize_info_label = ttk.Label(control_frame, text="No cropped image to resize")
        self.resize_info_label.pack(pady=2)
        
        # Resize slider
        self.resize_scale_var = tk.DoubleVar(value=1.0)
        self.resize_slider = ttk.Scale(control_frame, from_=0.1, to=3.0, 
                                      variable=self.resize_scale_var, 
                                      orient=tk.HORIZONTAL,
                                      command=self.on_resize_change,
                                      state="disabled")
        self.resize_slider.pack(pady=5, fill=tk.X)
        
        # Scale percentage label
        self.scale_label = ttk.Label(control_frame, text="Scale: 100%")
        self.scale_label.pack(pady=2)
        
        # Dimension labels
        self.dimension_label = ttk.Label(control_frame, text="")
        self.dimension_label.pack(pady=2)
        
        # Separator
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Reset button
        self.reset_button = ttk.Button(control_frame, text="Reset to Original", 
                                      command=self.reset_image, state="disabled")
        self.reset_button.pack(pady=5, fill=tk.X)
        
        # Status label to show current operation
        self.status_label = ttk.Label(control_frame, text="No image loaded", wraplength=180)
        self.status_label.pack(pady=10)
        
        # Instructions label
        self.instructions_label = ttk.Label(control_frame, 
                                           text="Instructions:\n1. Load an image\n2. Enable cropping and select area\n3. Apply crop\n4. Use slider to resize\n5. Reset to start over",
                                           justify=tk.LEFT, wraplength=180, font=('Arial', 8))
        self.instructions_label.pack(pady=10)
        
        # Original image display area
        self.image_frame = ttk.LabelFrame(main_frame, text="Original Image", padding="5")
        self.image_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Canvas to display the original image
        self.image_canvas = tk.Canvas(self.image_frame, bg="white", width=300, height=250)
        self.image_canvas.pack(expand=True, fill=tk.BOTH)
        
        # Cropped image display area
        self.cropped_frame = ttk.LabelFrame(main_frame, text="Cropped Image", padding="5")
        self.cropped_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=2)
        
        # Canvas to display the cropped image
        self.cropped_canvas = tk.Canvas(self.cropped_frame, bg="lightgray", width=300, height=250)
        self.cropped_canvas.pack(expand=True, fill=tk.BOTH)
        
        # Add text to cropped canvas initially
        self.cropped_canvas.create_text(150, 125, text="Cropped image\nwill appear here", 
                                       fill="gray", font=("Arial", 10), justify=tk.CENTER)
        
        # Resized image display area
        self.resized_frame = ttk.LabelFrame(main_frame, text="Resized Image (Final Result)", padding="5")
        self.resized_frame.grid(row=0, column=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Canvas to display the resized image
        self.resized_canvas = tk.Canvas(self.resized_frame, bg="lightblue", width=300, height=250)
        self.resized_canvas.pack(expand=True, fill=tk.BOTH)
        
        # Add text to resized canvas initially
        self.resized_canvas.create_text(150, 125, text="Final resized image\nwill appear here", 
                                       fill="darkblue", font=("Arial", 10), justify=tk.CENTER)
        
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
            
            # Reset all processed images
            self.cropped_image = None
            self.resized_image = None
            
            # Display the loaded image
            self.display_loaded_image()
            
            # Enable controls
            self.crop_button.config(state="normal")
            self.reset_button.config(state="normal")
            
            # Reset resize controls
            self.resize_slider.config(state="disabled")
            self.resize_scale_var.set(1.0)
            self.resize_info_label.config(text="No cropped image to resize")
            self.scale_label.config(text="Scale: 100%")
            self.dimension_label.config(text="")
            
            # Update status
            self.status_label.config(text=f"Image loaded: {file_path.split('/')[-1]}")
            
            # Clear other canvases
            self.cropped_canvas.delete("all")
            self.cropped_canvas.create_text(150, 125, text="Cropped image\nwill appear here", 
                                           fill="gray", font=("Arial", 10), justify=tk.CENTER)
            
            self.resized_canvas.delete("all")
            self.resized_canvas.create_text(150, 125, text="Final resized image\nwill appear here", 
                                           fill="darkblue", font=("Arial", 10), justify=tk.CENTER)
            
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
            canvas_width = 300
        if canvas_height <= 1:
            canvas_height = 250
        
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
    
    def toggle_cropping(self):
        """Enable or disable cropping mode"""
        
        if not self.is_cropping:
            # Enable cropping mode
            self.is_cropping = True
            self.crop_button.config(text="Disable Cropping")
            self.status_label.config(text="Cropping enabled - Click and drag to select area")
            
            # Bind mouse events for cropping
            self.image_canvas.bind("<Button-1>", self.start_crop)
            self.image_canvas.bind("<B1-Motion>", self.update_crop)
            self.image_canvas.bind("<ButtonRelease-1>", self.end_crop)
            
        else:
            # Disable cropping mode
            self.is_cropping = False
            self.crop_button.config(text="Enable Cropping")
            self.status_label.config(text="Cropping disabled")
            
            # Unbind mouse events
            self.image_canvas.unbind("<Button-1>")
            self.image_canvas.unbind("<B1-Motion>")
            self.image_canvas.unbind("<ButtonRelease-1>")
            
            # Remove crop rectangle if exists
            if self.crop_rectangle:
                self.image_canvas.delete(self.crop_rectangle)
                self.crop_rectangle = None
    
    def start_crop(self, event):
        """Start cropping - mouse button pressed"""
        
        # Store starting position
        self.crop_start_x = event.x
        self.crop_start_y = event.y
        
        # Remove previous crop rectangle if exists
        if self.crop_rectangle:
            self.image_canvas.delete(self.crop_rectangle)
    
    def update_crop(self, event):
        """Update crop rectangle while dragging"""
        
        # Store current position
        self.crop_end_x = event.x
        self.crop_end_y = event.y
        
        # Remove previous rectangle
        if self.crop_rectangle:
            self.image_canvas.delete(self.crop_rectangle)
        
        # Draw new rectangle
        self.crop_rectangle = self.image_canvas.create_rectangle(
            self.crop_start_x, self.crop_start_y, 
            self.crop_end_x, self.crop_end_y,
            outline="red", width=2, dash=(5, 5)
        )
    
    def end_crop(self, event):
        """End cropping - mouse button released"""
        
        # Update final position
        self.crop_end_x = event.x
        self.crop_end_y = event.y
        
        # Check if we have a valid selection
        if abs(self.crop_end_x - self.crop_start_x) > 10 and abs(self.crop_end_y - self.crop_start_y) > 10:
            # Enable apply crop button
            self.apply_crop_button.config(state="normal")
            self.status_label.config(text="Selection made - Click 'Apply Crop' to crop the image")
        else:
            # Selection too small
            self.status_label.config(text="Selection too small - Try again")
            if self.crop_rectangle:
                self.image_canvas.delete(self.crop_rectangle)
                self.crop_rectangle = None
    
    def apply_crop(self):
        """Apply the crop to the original image"""
        
        if self.original_image is None or self.crop_rectangle is None:
            return
        
        # Calculate crop coordinates relative to the original image
        # Convert canvas coordinates to image coordinates
        
        # Get the bounds of the crop rectangle
        x1 = min(self.crop_start_x, self.crop_end_x) - self.display_x
        y1 = min(self.crop_start_y, self.crop_end_y) - self.display_y
        x2 = max(self.crop_start_x, self.crop_end_x) - self.display_x
        y2 = max(self.crop_start_y, self.crop_end_y) - self.display_y
        
        # Make sure coordinates are within image bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(self.display_width, x2)
        y2 = min(self.display_height, y2)
        
        # Convert to original image coordinates
        orig_x1 = int(x1 / self.display_scale)
        orig_y1 = int(y1 / self.display_scale)
        orig_x2 = int(x2 / self.display_scale)
        orig_y2 = int(y2 / self.display_scale)
        
        # Make sure coordinates are valid
        img_height, img_width = self.original_image.shape[:2]
        orig_x1 = max(0, min(orig_x1, img_width))
        orig_y1 = max(0, min(orig_y1, img_height))
        orig_x2 = max(0, min(orig_x2, img_width))
        orig_y2 = max(0, min(orig_y2, img_height))
        
        # Crop the image
        self.cropped_image = self.original_image[orig_y1:orig_y2, orig_x1:orig_x2]
        
        # Store original cropped dimensions for resizing
        self.original_cropped_height, self.original_cropped_width = self.cropped_image.shape[:2]
        
        # Reset resize scale
        self.current_resize_scale = 1.0
        self.resize_scale_var.set(1.0)
        
        # Display the cropped image
        self.display_cropped_image()
        
        # Enable resize controls
        self.resize_slider.config(state="normal")
        self.resize_info_label.config(text=f"Original size: {self.original_cropped_width}x{self.original_cropped_height}")
        
        # Update resize display
        self.update_resize_display()
        
        # Initialize resized image as copy of cropped image
        self.resized_image = self.cropped_image.copy()
        self.display_resized_image()
        
        # Update status
        self.status_label.config(text="Image cropped successfully - Use slider to resize")
        
        # Disable apply crop button
        self.apply_crop_button.config(state="disabled")
        
        # Remove crop rectangle
        if self.crop_rectangle:
            self.image_canvas.delete(self.crop_rectangle)
            self.crop_rectangle = None
    
    def display_cropped_image(self):
        """Display the cropped image on the cropped canvas"""
        
        if self.cropped_image is None:
            return
        
        # Get canvas dimensions
        canvas_width = self.cropped_canvas.winfo_width()
        canvas_height = self.cropped_canvas.winfo_height()
        
        # If canvas hasn't been drawn yet, use default size
        if canvas_width <= 1:
            canvas_width = 300
        if canvas_height <= 1:
            canvas_height = 250
        
        # Get image dimensions
        img_height, img_width = self.cropped_image.shape[:2]
        
        # Calculate scaling factor to fit image in canvas while maintaining aspect ratio
        scale_x = (canvas_width - 20) / img_width
        scale_y = (canvas_height - 20) / img_height
        scale = min(scale_x, scale_y, 1.0)  # Don't scale up, only down
        
        # Calculate new dimensions
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Resize image for display
        resized_image = cv2.resize(self.cropped_image, (new_width, new_height))
        
        # Convert to PIL Image and then to PhotoImage for Tkinter
        pil_image = Image.fromarray(resized_image)
        self.cropped_display_image = ImageTk.PhotoImage(pil_image)
        
        # Clear canvas and display image
        self.cropped_canvas.delete("all")
        
        # Center the image on canvas
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        
        self.cropped_canvas.create_image(x, y, anchor=tk.NW, image=self.cropped_display_image)
    
    def on_resize_change(self, value):
        """Handle resize slider change"""
        
        if self.cropped_image is None:
            return
        
        # Get current scale value
        self.current_resize_scale = float(value)
        
        # Calculate new dimensions
        new_width = int(self.original_cropped_width * self.current_resize_scale)
        new_height = int(self.original_cropped_height * self.current_resize_scale)
        
        # Make sure dimensions are at least 1x1
        new_width = max(1, new_width)
        new_height = max(1, new_height)
        
        # Create resized image
        self.resized_image = cv2.resize(self.cropped_image, (new_width, new_height))
        
        # Update display
        self.display_resized_image()
        self.update_resize_display()
        
        # Update status
        percentage = int(self.current_resize_scale * 100)
        self.status_label.config(text=f"Resizing: {percentage}% - Size: {new_width}x{new_height}")
    
    def update_resize_display(self):
        """Update the resize information display"""
        
        if self.cropped_image is None:
            return
        
        # Calculate current dimensions
        new_width = int(self.original_cropped_width * self.current_resize_scale)
        new_height = int(self.original_cropped_height * self.current_resize_scale)
        percentage = int(self.current_resize_scale * 100)
        
        # Update labels
        self.scale_label.config(text=f"Scale: {percentage}%")
        self.dimension_label.config(text=f"New size: {new_width}x{new_height}")
    
    def display_resized_image(self):
        """Display the resized image on the resized canvas"""
        
        if self.resized_image is None:
            return
        
        # Get canvas dimensions
        canvas_width = self.resized_canvas.winfo_width()
        canvas_height = self.resized_canvas.winfo_height()
        
        # If canvas hasn't been drawn yet, use default size
        if canvas_width <= 1:
            canvas_width = 300
        if canvas_height <= 1:
            canvas_height = 250
        
        # Get image dimensions
        img_height, img_width = self.resized_image.shape[:2]
        
        # Calculate scaling factor to fit image in canvas while maintaining aspect ratio
        scale_x = (canvas_width - 20) / img_width
        scale_y = (canvas_height - 20) / img_height
        scale = min(scale_x, scale_y, 1.0)  # Don't scale up, only down
        
        # Calculate new dimensions
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Resize image for display
        display_resized_image = cv2.resize(self.resized_image, (new_width, new_height))
        
        # Convert to PIL Image and then to PhotoImage for Tkinter
        pil_image = Image.fromarray(display_resized_image)
        self.resized_display_image = ImageTk.PhotoImage(pil_image)
        
        # Clear canvas and display image
        self.resized_canvas.delete("all")
        
        # Center the image on canvas
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        
        self.resized_canvas.create_image(x, y, anchor=tk.NW, image=self.resized_display_image)
    
    def reset_image(self):
        """Reset to original image"""
        
        # Clear processed images
        self.cropped_image = None
        self.resized_image = None
        
        # Redisplay original image
        self.display_loaded_image()
        
        # Clear other canvases
        self.cropped_canvas.delete("all")
        self.cropped_canvas.create_text(150, 125, text="Cropped image\nwill appear here", 
                                       fill="gray", font=("Arial", 10), justify=tk.CENTER)
        
        self.resized_canvas.delete("all")
        self.resized_canvas.create_text(150, 125, text="Final resized image\nwill appear here", 
                                       fill="darkblue", font=("Arial", 10), justify=tk.CENTER)
        
        # Reset cropping mode
        if self.is_cropping:
            self.toggle_cropping()
        
        # Reset buttons and controls
        self.apply_crop_button.config(state="disabled")
        self.resize_slider.config(state="disabled")
        self.resize_scale_var.set(1.0)
        
        # Reset resize display
        self.resize_info_label.config(text="No cropped image to resize")
        self.scale_label.config(text="Scale: 100%")
        self.dimension_label.config(text="")
        
        # Remove crop rectangle if exists
        if self.crop_rectangle:
            self.image_canvas.delete(self.crop_rectangle)
            self.crop_rectangle = None
        
        # Update status
        self.status_label.config(text="Reset to original image")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Create and run the application
if __name__ == "__main__":
    app = ImageEditor()
    app.run()