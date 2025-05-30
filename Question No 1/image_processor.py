
# This inlcudes all image related stuff which is cropping, resizing and saving

import cv2
import numpy as np
from PIL import Image, ImageTk
import os
from tkinter import messagebox

class ImageProcessor:
    def __init__(self):
        # They se store all imag data in them
        self.original_image = None
        self.cropped_image = None
        self.resized_image = None
        
        # They are default values for resizing
        self.current_resize_scale = 1.0
        self.original_cropped_width = 0
        self.original_cropped_height = 0
        
        # to store the original file name for saving
        self.original_filename = ""
    
    def load_image(self, file_path):
        """Load an image from the specified file path"""
        try:
            # Load image using OpenCV
            self.original_image = cv2.imread(file_path)
            
            if self.original_image is None:
                messagebox.showerror("Error", "Could not load the selected image file.")
                return False
            
            # This converts BGR to RGB for proper display
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            
            # save orginial file name
            self.original_filename = os.path.splitext(os.path.basename(file_path))[0]
            
            # Reset all
            self.cropped_image = None
            self.resized_image = None
            
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            return False
    
    def prepare_image_for_display(self, image, canvas_width, canvas_height):
        """Prepare image for display on canvas with proper scaling"""
        if image is None:
            return None, 0, 0, 0, 0, 1.0
        
        # default size in case of error
        if canvas_width <= 1:
            canvas_width = 300
        if canvas_height <= 1:
            canvas_height = 250
        
        # image dimensions
        img_height, img_width = image.shape[:2]
        
        scale_x = (canvas_width - 20) / img_width
        scale_y = (canvas_height - 20) / img_height
        scale = min(scale_x, scale_y, 1.0) 
        
        # new dimensions
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Resize image for display
        resized_image = cv2.resize(image, (new_width, new_height))
        
        pil_image = Image.fromarray(resized_image)
        display_image = ImageTk.PhotoImage(pil_image)
        
        # Calculating center position
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        
        return display_image, x, y, new_width, new_height, scale
    
    def crop_image(self, crop_coords, display_info):
        """Crop the original image based on canvas coordinates"""
        if self.original_image is None:
            return False
        
        x1, y1, x2, y2 = crop_coords
        display_x, display_y, display_width, display_height, display_scale = display_info
        
        # Convert canvas coordinates to image coordinates
        x1 = max(0, x1 - display_x)
        y1 = max(0, y1 - display_y)
        x2 = min(display_width, x2 - display_x)
        y2 = min(display_height, y2 - display_y)
        
        # Convert to original image coordinates
        orig_x1 = int(x1 / display_scale)
        orig_y1 = int(y1 / display_scale)
        orig_x2 = int(x2 / display_scale)
        orig_y2 = int(y2 / display_scale)
        
        # to check coordinated are valid
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
        
        # copy of cropped image
        self.resized_image = self.cropped_image.copy()
        
        return True
    
    def resize_image(self, scale_factor):
        """Resize the cropped image by the given scale factor"""
        if self.cropped_image is None:
            return False
        
        self.current_resize_scale = scale_factor
        
        # new dimensions
        new_width = int(self.original_cropped_width * self.current_resize_scale)
        new_height = int(self.original_cropped_height * self.current_resize_scale)
        
        # 1x1 dimenions 
        new_width = max(1, new_width)
        new_height = max(1, new_height)
        
        # resized image
        self.resized_image = cv2.resize(self.cropped_image, (new_width, new_height))
        
        return True
    
    def get_resize_info(self):
        """Get current resize information"""
        if self.cropped_image is None:
            return None
        
        new_width = int(self.original_cropped_width * self.current_resize_scale)
        new_height = int(self.original_cropped_height * self.current_resize_scale)
        percentage = int(self.current_resize_scale * 100)
        
        return {
            'original_width': self.original_cropped_width,
            'original_height': self.original_cropped_height,
            'new_width': new_width,
            'new_height': new_height,
            'percentage': percentage
        }
    
    def save_image(self, image_type, file_path):
        """Save the specified image type to the given file path"""
        try:
            if image_type == "original":
                if self.original_image is None:
                    messagebox.showwarning("Warning", "No image loaded to save!")
                    return False
                image_to_save = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2BGR)
                
            elif image_type == "cropped":
                if self.cropped_image is None:
                    messagebox.showwarning("Warning", "No cropped image to save! Please crop an image first.")
                    return False
                image_to_save = cv2.cvtColor(self.cropped_image, cv2.COLOR_RGB2BGR)
                
            elif image_type == "final":
                if self.resized_image is None:
                    messagebox.showwarning("Warning", "No final image to save! Please crop and resize an image first.")
                    return False
                image_to_save = cv2.cvtColor(self.resized_image, cv2.COLOR_RGB2BGR)
                
            else:
                messagebox.showerror("Error", "Invalid image type specified!")
                return False
            
            # Save the image
            success = cv2.imwrite(file_path, image_to_save)
            
            if success:
                if image_type == "final":
                    height, width = self.resized_image.shape[:2]
                    scale_percentage = int(self.current_resize_scale * 100)
                    messagebox.showinfo("Success", 
                                       f"Final image saved successfully!\nLocation: {file_path}\nSize: {width}x{height} pixels\nScale: {scale_percentage}%")
                else:
                    messagebox.showinfo("Success", f"{image_type.capitalize()} image saved successfully!\nLocation: {file_path}")
                return True
            else:
                messagebox.showerror("Error", f"Failed to save the {image_type} image!")
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Error saving {image_type} image: {str(e)}")
            return False
    
    def reset(self):
        """Reset all processed images"""
        self.cropped_image = None
        self.resized_image = None
        self.current_resize_scale = 1.0
    
    def get_original_filename(self):
        """Get the original filename for saving purposes"""
        return self.original_filename