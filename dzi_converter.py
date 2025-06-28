"""Streamlit app for DZI conversion using pyvips."""
import asyncio
from concurrent.futures import ThreadPoolExecutor
import streamlit as st
from dzi_utils import (
    ensure_output_dir,
    count_dzi_files,
    convert_to_dzi,
    count_dzi_related_files,
    create_dzi_zip
)

# Async wrapper for blocking DZI conversion
def async_convert_to_dzi(input_path, output_dir, loop=None):
    """
    Runs the blocking DZI conversion in a background thread for better UI responsiveness.
    Args:
        input_path (str): Path to the input image file.
        output_dir (str): Directory to save the DZI output.
        loop (asyncio.AbstractEventLoop, optional): Event loop to use.
    Returns:
        concurrent.futures.Future: Future for the conversion result.
    """
    loop = loop or asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return loop.run_in_executor(pool, convert_to_dzi, input_path, output_dir)

st.set_page_config(page_title="DZI Converter", page_icon="🖼️")

st.title("DZI Converter with pyvips & Streamlit")

uploaded_file = st.file_uploader(
    "Upload an image to convert to DZI", type=["jpg", "jpeg", "png", "tif", "tiff"]
)

if uploaded_file is not None:
    with st.spinner("Converting to DZI format..."):
        TEMP_INPUT_FILEPATH = f"/tmp/{uploaded_file.name}"
        with open(TEMP_INPUT_FILEPATH, "wb") as file_handle:
            file_handle.write(uploaded_file.getbuffer())
        dzi_output_dir = ensure_output_dir()
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        dzi_file = event_loop.run_until_complete(
            async_convert_to_dzi(TEMP_INPUT_FILEPATH, dzi_output_dir, event_loop)
        )
        dzi_base_path = dzi_file.rsplit('.', 1)[0]
        dzi_related_count = count_dzi_related_files(dzi_base_path)
        dzi_count = count_dzi_files(dzi_output_dir)
        st.success(f"Conversion complete! DZI file saved at: {dzi_file}")
        st.write(f"DZI descriptor: {dzi_file}")
        st.info(f"Total DZI files generated: {dzi_count}")
        st.info(f"Files generated for this conversion (including tiles): {dzi_related_count}")
        # Download button for zipped DZI and tiles
        zip_buffer = create_dzi_zip(dzi_base_path)
        st.download_button(
            label="Download DZI + Tiles as ZIP",
            data=zip_buffer,
            file_name=f"{dzi_base_path.split('/')[-1]}_dzi_bundle.zip",
            mime="application/zip"
        )
