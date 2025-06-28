"""
dzi_utils.py
Utility functions for DZI conversion and packaging using pyvips.
"""
import io
import os
import shutil
import zipfile

import pyvips


def ensure_output_dir():
    """
    Ensures the output directory for DZI files exists.
    Returns:
        str: The absolute path to the output directory.
    """
    output_dir = os.path.join(os.getcwd(), "dzi_output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def count_dzi_files(output_dir):
    """
    Counts the number of DZI descriptor (.dzi) files in the output directory.
    Args:
        output_dir (str): Path to the output directory.
    Returns:
        int: Number of .dzi files found.
    """
    return len([f for f in os.listdir(output_dir) if f.endswith('.dzi')])


def convert_to_dzi(input_path, output_dir):
    """
    Converts an image to Deep Zoom Image (DZI) format using pyvips.
    Overwrites any existing DZI output for the same base name.
    Args:
        input_path (str): Path to the input image file.
        output_dir (str): Directory to save the DZI output.
    Returns:
        str: Path to the generated .dzi descriptor file.
    """
    image = pyvips.Image.new_from_file(input_path, access="sequential")
    dzi_basename = os.path.splitext(os.path.basename(input_path))[0]
    dzi_path = os.path.join(output_dir, dzi_basename)
    # Remove existing DZI descriptor and tile folder if they exist
    dzi_descriptor = dzi_path + ".dzi"
    tiles_folder = dzi_path + "_files"
    if os.path.exists(dzi_descriptor):
        os.remove(dzi_descriptor)
    if os.path.exists(tiles_folder):
        shutil.rmtree(tiles_folder)
    image.dzsave(dzi_path, tile_size=512)
    return dzi_path + ".dzi"


def count_dzi_related_files(dzi_base_path):
    """
    Counts all files generated for a DZI conversion, including the .dzi descriptor and all tile files in the folder.
    Args:
        dzi_base_path (str): Base path (without extension) of the DZI output.
    Returns:
        int: Total number of files generated for this DZI conversion.
    """
    count = 0
    dzi_descriptor = dzi_base_path + ".dzi"
    if os.path.exists(dzi_descriptor):
        count += 1
    tiles_folder = dzi_base_path + '_files'
    for _, _, files in os.walk(tiles_folder):
        count += len(files)
    return count


def create_dzi_zip(dzi_base_path):
    """
    Creates an in-memory zip containing the .dzi descriptor and all tile files in the folder.
    Args:
        dzi_base_path (str): Base path (without extension) of the DZI output.
    Returns:
        io.BytesIO: BytesIO object containing the zipped DZI and tiles.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add DZI descriptor
        dzi_descriptor = dzi_base_path + ".dzi"
        if os.path.exists(dzi_descriptor):
            zipf.write(dzi_descriptor, os.path.basename(dzi_descriptor))
        # Add all tile files
        tiles_folder = dzi_base_path + '_files'
        for _, _, files in os.walk(tiles_folder):
            for file in files:
                abs_path = os.path.join(tiles_folder, file)
                rel_path = os.path.relpath(abs_path, os.path.dirname(dzi_base_path))
                zipf.write(abs_path, rel_path)
    zip_buffer.seek(0)
    return zip_buffer
