

# this is all the UI of application 

import tkinter as tk
from tkinter import ttk, filedialog

class ImageEditorGUI:
    def __init__(self, root, processor):
        self.root = root
        self.processor = processor
        
        # Variables 
        self.display_x = 0
        self.display_y = 0
        self.display_width = 0
        self.display_height = 0
        self.display_scale = 1.0
        self.is_cropping = False
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.crop_rectangle = None
        self.resize_scale_var = tk.DoubleVar(value=1.0)
        self.display_image = None
        self.cropped_display_image = None
        self.resized_display_image = None
        
        # Create the UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI elements"""
        
        # Main window to hold everything
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # for responsive design
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
        
        # Saving controls section
        save_label = ttk.Label(control_frame, text="SAVING CONTROLS", font=('Arial', 9, 'bold'))
        save_label.pack(pady=(0, 5))
        
        # Save original image button
        self.save_original_button = ttk.Button(control_frame, text="Save Original Image", 
                                              command=self.save_original_image, state="disabled")
        self.save_original_button.pack(pady=2, fill=tk.X)
        
        # Save cropped image button
        self.save_cropped_button = ttk.Button(control_frame, text="Save Cropped Image", 
                                             command=self.save_cropped_image, state="disabled")
        self.save_cropped_button.pack(pady=2, fill=tk.X)
        
        # Save final image button (cropped + resized)
        self.save_final_button = ttk.Button(control_frame, text="Save Final Image", 
                                           command=self.save_final_image, state="disabled")
        self.save_final_button.pack(pady=2, fill=tk.X)
        
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
                                           text="Instructions:\n1. Load an image\n2. Enable cropping and select area\n3. Apply crop\n4. Use slider to resize\n5. Save your work\n6. Reset to start over",
                                           justify=tk.LEFT, wraplength=180, font=('Arial', 8))
        self.instructions_label.pack(pady=10)
        
        # Original image display area
        self.image_frame = ttk.LabelFrame(main_frame, text="Original Image", padding="5")
        self.image_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
       
        self.image_canvas = tk.Canvas(self.image_frame, bg="white", width=300, height=250)
        self.image_canvas.pack(expand=True, fill=tk.BOTH)
        
        # Cropped image display area
        self.cropped_frame = ttk.LabelFrame(main_frame, text="Cropped Image", padding="5")
        self.cropped_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=2)
        
      
        self.cropped_canvas = tk.Canvas(self.cropped_frame, bg="lightgray", width=300, height=250)
        self.cropped_canvas.pack(expand=True, fill=tk.BOTH)
        
        # shows text when no image
        self.cropped_canvas.create_text(150, 125, text="Cropped image\nwill appear here", 
                                       fill="gray", font=("Arial", 10), justify=tk.CENTER)
        
        # Resized image display area
        self.resized_frame = ttk.LabelFrame(main_frame, text="Resized Image (Final Result)", padding="5")
        self.resized_frame.grid(row=0, column=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Canvas to display the resized image
        self.resized_canvas = tk.Canvas(self.resized_frame, bg="lightblue", width=300, height=250)
        self.resized_canvas.pack(expand=True, fill=tk.BOTH)
        
        # shows text initiallly
        self.resized_canvas.create_text(150, 125, text="Final resized image\nwill appear here", 
                                       fill="darkblue", font=("Arial", 10), justify=tk.CENTER)
    
    def load_image(self):
        """Load an image from the local device"""
        
        # to select image
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
        
        # Use processor to load the image
        if self.processor.load_image(file_path):
            # Display the loaded image
            self.display_loaded_image()
            
            # Enable controls
            self.crop_button.config(state="normal")
            self.reset_button.config(state="normal")
            self.save_original_button.config(state="normal")
            
            # Reset resize controls
            self.resize_slider.config(state="disabled")
            self.resize_scale_var.set(1.0)
            self.resize_info_label.config(text="No cropped image to resize")
            self.scale_label.config(text="Scale: 100%")
            self.dimension_label.config(text="")
            
            # Reset save buttons for processed images
            self.save_cropped_button.config(state="disabled")
            self.save_final_button.config(state="disabled")
            
            # Update status
            self.status_label.config(text=f"Image loaded: {file_path.split('/')[-1]}")
            
            # Clear other 
            self.clear_secondary_canvases()
    
    def display_loaded_image(self):
        """Display the loaded image on the canvas"""
        
        if self.processor.original_image is None:
            return
        
        # Get canvas dimensions
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        # Prepare image for display
        display_info = self.processor.prepare_image_for_display(
            self.processor.original_image, canvas_width, canvas_height
        )
        
        self.display_image, x, y, width, height, scale = display_info
        
        # Store display properties
        self.display_x = x
        self.display_y = y
        self.display_width = width
        self.display_height = height
        self.display_scale = scale
        
        # Clear canvas and display image
        self.image_canvas.delete("all")
        self.image_canvas.create_image(x, y, anchor=tk.NW, image=self.display_image)
    
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
        
        if self.processor.original_image is None or self.crop_rectangle is None:
            return
        
        # Get crop coordinates
        x1 = min(self.crop_start_x, self.crop_end_x)
        y1 = min(self.crop_start_y, self.crop_end_y)
        x2 = max(self.crop_start_x, self.crop_end_x)
        y2 = max(self.crop_start_y, self.crop_end_y)
        
        # Crop the image using processor
        display_info = (self.display_x, self.display_y, self.display_width, 
                       self.display_height, self.display_scale)
        
        if self.processor.crop_image((x1, y1, x2, y2), display_info):
            # Display the cropped image
            self.display_cropped_image()
            
            # Enable resize controls
            self.resize_slider.config(state="normal")
            resize_info = self.processor.get_resize_info()
            self.resize_info_label.config(text=f"Original size: {resize_info['original_width']}x{resize_info['original_height']}")
            
            # Update resize display
            self.update_resize_display()
            
            # Display resized image 
            self.display_resized_image()
            
            # Enable save buttons for cropped and final images
            self.save_cropped_button.config(state="normal")
            self.save_final_button.config(state="normal")
            
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
        
        if self.processor.cropped_image is None:
            return
        
        # Get canvas dimensions
        canvas_width = self.cropped_canvas.winfo_width()
        canvas_height = self.cropped_canvas.winfo_height()
        
        # Prepare image for display
        display_info = self.processor.prepare_image_for_display(
            self.processor.cropped_image, canvas_width, canvas_height
        )
        
        self.cropped_display_image, x, y, width, height, scale = display_info
        
        # Clear canvas and display image
        self.cropped_canvas.delete("all")
        self.cropped_canvas.create_image(x, y, anchor=tk.NW, image=self.cropped_display_image)
    
    def on_resize_change(self, value):
        """Handle resize slider change"""
        
        if self.processor.cropped_image is None:
            return
        
        # Get current scale value
        scale_factor = float(value)
        
        # Resize image using processor
        if self.processor.resize_image(scale_factor):
            # Update display
            self.display_resized_image()
            self.update_resize_display()
            
            # Update status
            resize_info = self.processor.get_resize_info()
            self.status_label.config(text=f"Resizing: {resize_info['percentage']}% - Size: {resize_info['new_width']}x{resize_info['new_height']}")
    
    def update_resize_display(self):
        """Update the resize information display"""
        
        resize_info = self.processor.get_resize_info()
        if resize_info is None:
            return
        
        # Update labels
        self.scale_label.config(text=f"Scale: {resize_info['percentage']}%")
        self.dimension_label.config(text=f"New size: {resize_info['new_width']}x{resize_info['new_height']}")
    
    def display_resized_image(self):
        """Display the resized image on the resized canvas"""
        
        if self.processor.resized_image is None:
            return
        
        # Get canvas dimensions
        canvas_width = self.resized_canvas.winfo_width()
        canvas_height = self.resized_canvas.winfo_height()
        
        # Prepare image for display
        display_info = self.processor.prepare_image_for_display(
            self.processor.resized_image, canvas_width, canvas_height
        )
        
        self.resized_display_image, x, y, width, height, scale = display_info
        
        # Clear canvas and display image
        self.resized_canvas.delete("all")
        self.resized_canvas.create_image(x, y, anchor=tk.NW, image=self.resized_display_image)
    
    def save_original_image(self):
        """Save the original loaded image"""
        
        filename = self.processor.get_original_filename()
        file_path = filedialog.asksaveasfilename(
            title="Save Original Image",
            defaultextension=".png",
            initialfile=f"{filename}_original",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            if self.processor.save_image("original", file_path):
                self.status_label.config(text="Original image saved successfully")
    
    def save_cropped_image(self):
        """Save the cropped image"""
        
        filename = self.processor.get_original_filename()
        file_path = filedialog.asksaveasfilename(
            title="Save Cropped Image",
            defaultextension=".png",
            initialfile=f"{filename}_cropped",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            if self.processor.save_image("cropped", file_path):
                self.status_label.config(text="Cropped image saved successfully")
    
    def save_final_image(self):
        """Save the final image (cropped and resized)"""
        
        filename = self.processor.get_original_filename()
        resize_info = self.processor.get_resize_info()
        scale_percentage = resize_info['percentage'] if resize_info else 100
        
        file_path = filedialog.asksaveasfilename(
            title="Save Final Image",
            defaultextension=".png",
            initialfile=f"{filename}_final_{scale_percentage}percent",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            if self.processor.save_image("final", file_path):
                self.status_label.config(text="Final image saved successfully")
    
    def clear_secondary_canvases(self):
        """Clear the cropped and resized canvases"""
        
        self.cropped_canvas.delete("all")
        self.cropped_canvas.create_text(150, 125, text="Cropped image\nwill appear here", 
                                       fill="gray", font=("Arial", 10), justify=tk.CENTER)
        
        self.resized_canvas.delete("all")
        self.resized_canvas.create_text(150, 125, text="Final resized image\nwill appear here", 
                                       fill="darkblue", font=("Arial", 10), justify=tk.CENTER)
    
    def reset_image(self):
        """Reset to original image"""
        
        # Reset processor
        self.processor.reset()
        
        # Redisplay original image
        self.display_loaded_image()
        
        # Clear other canvases
        self.clear_secondary_canvases()
        
        # Reset cropping mode
        if self.is_cropping:
            self.toggle_cropping()
        
        # Reset buttons and controls
        self.apply_crop_button.config(state="disabled")
        self.resize_slider.config(state="disabled")
        self.resize_scale_var.set(1.0)
        
        # Reset save buttons for processed images
        self.save_cropped_button.config(state="disabled")
        self.save_final_button.config(state="disabled")
        
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