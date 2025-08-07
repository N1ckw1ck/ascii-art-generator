import sys
import math
import os
import platform
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QCheckBox, QHBoxLayout, QComboBox, QSizePolicy)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image, ImageDraw, ImageFont

# ASCII character array from darkest to lightest (removed [::-1] reversal)
chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^'. "
charArray = list(chars)
interval = len(charArray) / 256
scaleFactor = 0.25  # Increased from 0.09 for much more detail
oneCharWidth = 6    # Smaller spacing for tighter packing
oneCharHeight = 10  # Smaller spacing for tighter packing

# Cross-platform font handling
def get_monospace_font():
    """Get a monospace font path based on the operating system."""
    system = platform.system()
    
    if system == "Windows":
        # Windows font paths
        font_paths = [
            "C:/Windows/Fonts/consola.ttf",      # Consolas
            "C:/Windows/Fonts/cour.ttf",         # Courier New
            "C:/Windows/Fonts/courbd.ttf",       # Courier New Bold
            "C:/Windows/Fonts/lucon.ttf",        # Lucida Console
        ]
    elif system == "Darwin":  # macOS
        # macOS font paths (commented out for Windows usage)
        font_paths = [
            # "/System/Library/Fonts/Menlo.ttc",
            # "/System/Library/Fonts/Monaco.ttf",
            # "/Library/Fonts/Courier New.ttf",
        ]
    else:  # Linux and others
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
            "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
        ]
    
    # Try to find an existing font
    for font_path in font_paths:
        if os.path.exists(font_path):
            return font_path
    
    # Fallback: try to use system default
    return None

def getChar(inputInt):
    """Convert grayscale value to ASCII character."""
    return charArray[math.floor(inputInt * interval)]

def convert_image_to_ascii(path, dark_theme=False, detail_level="High"):
    """Convert an image to ASCII art with theme and detail support."""
    try:
        # Open and convert image
        im = Image.open(path).convert('RGB')
        
        # Set detail parameters based on level
        detail_settings = {
            "Low": {"scale": 0.15, "char_width": 8, "char_height": 14, "font_size": 10},
            "Medium": {"scale": 0.20, "char_width": 7, "char_height": 12, "font_size": 9},
            "High": {"scale": 0.25, "char_width": 6, "char_height": 10, "font_size": 8},
            "Ultra": {"scale": 0.35, "char_width": 5, "char_height": 8, "font_size": 7}
        }
        
        settings = detail_settings[detail_level]
        current_scaleFactor = settings["scale"]
        current_oneCharWidth = settings["char_width"]
        current_oneCharHeight = settings["char_height"]
        current_font_size = settings["font_size"]
        
        # Choose character array based on theme
        if dark_theme:
            # Dark theme: light characters on dark background
            theme_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^'. "[::-1]
            bg_color = (0, 0, 0)  # Black background
        else:
            # Light theme: dark characters on light background
            theme_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^'. "
            bg_color = (255, 255, 255)  # White background
        
        theme_charArray = list(theme_chars)
        theme_interval = len(theme_charArray) / 256
        
        def getThemeChar(inputInt):
            return theme_charArray[math.floor(inputInt * theme_interval)]
        
        # Get font
        font_path = get_monospace_font()
        if font_path:
            try:
                fnt = ImageFont.truetype(font_path, current_font_size)
            except:
                fnt = ImageFont.load_default()
        else:
            fnt = ImageFont.load_default()
        
        # Resize image
        width, height = im.size
        im = im.resize((int(current_scaleFactor * width), int(current_scaleFactor * height * (current_oneCharWidth / current_oneCharHeight))))
        width, height = im.size
        pix = im.load()
        
        # Create output image with theme-appropriate background
        outputImage = Image.new('RGB', (current_oneCharWidth * width, current_oneCharHeight * height), color=bg_color)
        d = ImageDraw.Draw(outputImage)
        
        # Process each pixel
        for i in range(height):
            for j in range(width):
                r, g, b = pix[j, i]
                # Convert to grayscale
                h = int(r / 3 + g / 3 + b / 3)
                pix[j, i] = (h, h, h)
                # Draw ASCII character with original color
                d.text((j * current_oneCharWidth, i * current_oneCharHeight), getThemeChar(h), font=fnt, fill=(r, g, b))
        
        return outputImage
    
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")

class DragDropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASCII Art Generator")
        self.setAcceptDrops(True)
        
        # Set larger window size - about 75% of typical screen size
        self.resize(1200, 900)
        self.setMinimumSize(800, 600)  # Set minimum size for usability
        
        # Create UI elements
        self.label = QLabel("Drag and drop an image here\n(Supports PNG, JPG, JPEG, BMP, GIF)", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { background-color: lightgray; padding: 40px; border: 2px dashed gray; }")
        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("QLabel { border: 1px solid gray; }")
        self.image_label.setMinimumSize(400, 300)  # Minimum size for the image display
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.save_button = QPushButton("Save ASCII Art", self)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_image)
        
        # Browse button as alternative to drag-drop
        self.browse_button = QPushButton("Browse for Image", self)
        self.browse_button.clicked.connect(self.browse_image)
        
        # Theme toggle
        self.theme_toggle = QCheckBox("Dark Theme", self)
        self.theme_toggle.setToolTip("Toggle between light theme (dark text on white) and dark theme (light text on black)")
        self.theme_toggle.stateChanged.connect(self.on_theme_changed)
        
        # Detail level selector
        self.detail_label = QLabel("Detail:", self)
        self.detail_combo = QComboBox(self)
        self.detail_combo.addItems(["Low", "Medium", "High", "Ultra"])
        self.detail_combo.setCurrentText("High")  # Default to high detail
        self.detail_combo.setToolTip("Low: Fast, basic detail\nMedium: Balanced\nHigh: More characters, better quality\nUltra: Maximum detail (slower)")
        self.detail_combo.currentTextChanged.connect(self.on_detail_changed)
        
        # Bottom layout for controls
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.browse_button)
        controls_layout.addStretch()  # Add space between controls
        controls_layout.addWidget(self.detail_label)
        controls_layout.addWidget(self.detail_combo)
        controls_layout.addWidget(self.theme_toggle)
        
        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.image_label)
        layout.addLayout(controls_layout)  # Add the controls layout
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        
        self.ascii_image = None
        self.current_image_path = None  # Store current image path for theme switching
    
    def dragEnterEvent(self, event):
        """Handle drag enter event."""
        if event.mimeData() and event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and any(url.toLocalFile().lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) for url in urls):
                self.label.setText("Drop the image!")
                self.label.setStyleSheet("QLabel { background-color: lightgreen; padding: 40px; border: 2px dashed green; }")
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        """Handle drag leave event."""
        self.label.setText("Drag and drop an image here\n(Supports PNG, JPG, JPEG, BMP, GIF)")
        self.label.setStyleSheet("QLabel { background-color: lightgray; padding: 40px; border: 2px dashed gray; }")
    
    def dropEvent(self, event):
        """Handle drop event."""
        self.label.setText("Processing image...")
        self.label.setStyleSheet("QLabel { background-color: lightyellow; padding: 40px; border: 2px solid orange; }")
        
        if event.mimeData() and event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    self.process_image(file_path)
                    break
    
    def browse_image(self):
        """Open file dialog to browse for image."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Image", 
            "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.process_image(file_path)
    
    def on_theme_changed(self):
        """Handle theme toggle change."""
        if self.current_image_path:
            # Regenerate ASCII art with new theme
            self.process_image(self.current_image_path)
    
    def on_detail_changed(self):
        """Handle detail level change."""
        if self.current_image_path:
            # Regenerate ASCII art with new detail level
            self.process_image(self.current_image_path)
    
    def process_image(self, path):
        """Process the selected image."""
        try:
            self.current_image_path = path  # Store path for theme switching
            dark_theme = self.theme_toggle.isChecked()
            detail_level = self.detail_combo.currentText()
            
            self.ascii_image = convert_image_to_ascii(path, dark_theme, detail_level)
            self.update_image_display()
            
            self.save_button.setEnabled(True)
            theme_text = "Dark Theme" if dark_theme else "Light Theme"
            self.label.setText(f"ASCII Art Preview ({theme_text}, {detail_level} Detail) - drag another image or use browse button:")
            self.label.setStyleSheet("QLabel { background-color: lightblue; padding: 20px; }")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process image:\n{str(e)}")
            self.label.setText("Error processing image. Try another one.")
            self.label.setStyleSheet("QLabel { background-color: lightcoral; padding: 40px; border: 2px solid red; }")
    
    def update_image_display(self):
        """Update the image display to fit the current window size."""
        if self.ascii_image:
            qt_image = self.pil2pixmap(self.ascii_image)
            
            # Get available size for the image (leave some margin)
            available_size = self.image_label.size()
            margin = 20
            max_width = max(400, available_size.width() - margin)
            max_height = max(300, available_size.height() - margin)
            
            # Scale image to fit available space while maintaining aspect ratio
            scaled_pixmap = qt_image.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
    
    def resizeEvent(self, event):
        """Handle window resize events to rescale the image."""
        super().resizeEvent(event)
        # Update image display when window is resized
        if hasattr(self, 'ascii_image') and self.ascii_image:
            self.update_image_display()
    
    def save_image(self):
        """Save the ASCII art image."""
        if self.ascii_image:
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Save ASCII Art", 
                "ascii_art.png", 
                "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)"
            )
            if file_path:
                try:
                    self.ascii_image.save(file_path)
                    QMessageBox.information(self, "Success", f"ASCII art saved to:\n{file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to save image:\n{str(e)}")
    
    def pil2pixmap(self, im):
        """Convert PIL image to QPixmap."""
        im = im.convert("RGBA")
        data = im.tobytes("raw", "RGBA")
        qimage = QImage(data, im.size[0], im.size[1], QImage.Format_RGBA8888)
        return QPixmap.fromImage(qimage)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DragDropWidget()
    window.show()
    sys.exit(app.exec_())