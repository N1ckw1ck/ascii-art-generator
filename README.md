# ASCII Art Generator

A desktop application that converts images into beautiful ASCII art with customizable themes and detail levels.

## ✨ Features

- **Drag & Drop Interface**: Simply drag images into the window or use the browse button
- **Dual Themes**: 
  - Light Theme: Dark characters on white background (perfect for printing)
  - Dark Theme: Light characters on dark background (great for displays)
- **4 Detail Levels**: 
  - Low: Fast processing, basic detail
  - Medium: Balanced quality and speed
  - High: Enhanced detail with more characters
  - Ultra: Maximum detail for incredible quality
- **Live Preview**: See your ASCII art instantly with responsive window scaling
- **Save as PNG**: Export your ASCII art as high-quality image files
- **Cross-Platform Fonts**: Automatically detects and uses the best monospace font available

## 🚀 Quick Start

### For Users (No Installation Required)
1. Download the latest `ASCII_Art_Generator.exe` from [Releases](../../releases)
2. Double-click to run - that's it! No installation needed.

### How to Use
1. **Load Image**: Drag & drop an image or click "Browse for Image"
2. **Choose Theme**: Toggle "Dark Theme" checkbox for light-on-dark or leave unchecked for dark-on-light
3. **Select Detail**: Choose from Low, Medium, High, or Ultra detail in the dropdown
4. **Preview**: Watch your ASCII art generate in real-time
5. **Resize Window**: Drag corners to make the preview larger or smaller
6. **Save**: Click "Save ASCII Art" to export as PNG

### Supported Image Formats
- PNG
- JPG/JPEG  
- BMP
- GIF

## 🛠️ Development Setup

### Prerequisites
- Python 3.7+
- Windows (tested), should work on macOS/Linux with minor font adjustments

### Install and Run from Source
```bash
# Clone the repository
git clone https://github.com/N1ckw1ck/ascii-art-generator.git
cd ascii_art_gen

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the application
python ascii_art_src_final.py
```

### Building Executable
```bash
# Make sure venv is activated
venv\Scripts\activate

# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "ASCII_Art_Generator" ascii_art_src_final.py

# Find executable in dist/ folder
```

## 🎯 Technical Details

### How It Works
1. **Image Processing**: Uses PIL (Pillow) to load and resize images
2. **Character Mapping**: Maps grayscale values to ASCII characters
3. **Font Rendering**: Uses system monospace fonts for consistent character spacing
4. **GUI Framework**: Built with PyQt5 for cross-platform compatibility
5. **Color Preservation**: Maintains original image colors in the ASCII output

### Performance
- **Low Detail**: ~0.1-0.5 seconds for typical images
- **Ultra Detail**: ~1-3 seconds for complex images
- **Memory Efficient**: Processes images in manageable chunks
- **Responsive UI**: Non-blocking interface during processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [PyQt5](https://riverbankcomputing.com/software/pyqt/) for the GUI framework
- [Pillow](https://pillow.readthedocs.io/) for powerful image processing
- Inspired by classic ASCII art generators with modern UI improvements

---

**Enjoy creating ASCII art! 🎨**
