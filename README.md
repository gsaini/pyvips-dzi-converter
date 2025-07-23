# DZI Converter with Streamlit & pyvips

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)](https://www.python.org/) 
[![Streamlit](https://img.shields.io/badge/streamlit-%E2%9C%94%EF%B8%8F-brightgreen?logo=streamlit)](https://streamlit.io/) 
[![pyvips](https://img.shields.io/badge/pyvips-%E2%9C%94%EF%B8%8F-blueviolet?logo=python)](https://libvips.github.io/pyvips/)
[![pylint](https://github.com/gsaini/pyvips-dzi-converter/actions/workflows/pylint.yml/badge.svg)](https://github.com/gsaini/pyvips-dzi-converter/actions/workflows/pylint.yml)

This project provides a web-based Deep Zoom Image (DZI) converter using [Streamlit](https://streamlit.io/) and [pyvips](https://libvips.github.io/pyvips/). It allows users to upload large images, convert them to the DZI format (compatible with OpenSeadragon and similar viewers), and download the result as a zipped bundle containing the DZI descriptor and all image tiles.

## Features
- Upload large images (JPG, PNG, TIFF, etc.) via a web interface
- Convert images to DZI format using pyvips for high performance
- Download the DZI descriptor and all generated tiles as a single ZIP file
- See statistics on how many DZI files and tiles were generated
- Asynchronous processing for responsive UI
- Modular codebase for easy maintenance and extension

## Project Structure
```
dzi-converter/
├── dzi_converter.py      # Main Streamlit app
├── dzi_utils.py          # Utility functions for DZI conversion and packaging
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation (this file)
```

## Requirements
- Python 3.8+
- [libvips](https://libvips.github.io/libvips/) installed on your system (required by pyvips)
- pip (for installing Python dependencies)

## Installation
1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd dzi-converter
   ```
2. **Install system dependencies**
   - On macOS (with Homebrew):
     ```sh
     brew install vips
     ```
   - On Ubuntu/Debian:
     ```sh
     sudo apt-get install libvips-dev
     ```
3. **Set up Python environment and install dependencies**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Usage
1. **Start the Streamlit app**
   ```sh
   streamlit run dzi_converter.py
   ```
2. **Open your browser** and go to [http://localhost:8501](http://localhost:8501)
3. **Upload an image** (JPG, PNG, TIFF, etc.)
4. **Wait for conversion** (progress shown in the UI)
5. **Download the DZI + tiles as a ZIP** using the provided button

## How it Works
- The app uses pyvips to convert the uploaded image to DZI format with a tile size of 512px for performance.
- All generated files (the `.dzi` descriptor and the tile folder) are zipped in-memory and offered for download.
- The code is modular: all conversion and packaging logic is in `dzi_utils.py`, while the UI and workflow are in `dzi_converter.py`.

## Customization
- You can adjust tile size, compression, or other pyvips options in `dzi_utils.py`.
- To upload to Azure Blob Storage or other cloud storage, you can extend the app with additional upload logic.

## Troubleshooting
- **Large file uploads:** If you need to upload files larger than 200MB, set `maxUploadSize` in your Streamlit config (`~/.streamlit/config.toml`):
  ```toml
  [server]
  maxUploadSize = 1024
  ```
- **libvips not found:** Make sure `vips` is installed and available in your system path.
- **pyvips errors:** Ensure your image format is supported and that you have the latest version of pyvips and libvips.

## Serving DZI Output Files via HTTP
If you want to serve the generated DZI files and tiles over HTTP (for use with OpenSeadragon or remote access), you can use Python's built-in HTTP server:

1. Open a terminal and navigate to the dzi_output directory:
   ```sh
   cd /path/to/dzi-converter/dzi_output
   python3 -m http.server 8080
   ```
2. Access your files at `http://localhost:8080/` or replace `localhost` with your server's IP address for remote access.
3. You can now use OpenSeadragon or other viewers to load the DZI descriptor and tiles directly from the server.

**Note:** For production, consider using a more robust web server (e.g., nginx, Apache) and secure your files as needed.

## License
MIT License

## Credits
- [Streamlit](https://streamlit.io/)
- [pyvips](https://libvips.github.io/pyvips/)
- [libvips](https://libvips.github.io/libvips/)
- [OpenSeadragon](https://openseadragon.github.io/)
