import gradio as gr
import os
import glob
import time
from pinscrape import scraper

# --- Helper function for dynamic UI ---

def toggle_inputs(scrape_mode):
    """Updates the visibility of the input fields based on the selected mode."""
    if scrape_mode == "By Keyword":
        return gr.update(visible=True), gr.update(visible=False)
    else: # By URL
        return gr.update(visible=False), gr.update(visible=True)

# --- Core Scraping Logic ---

def run_scraper(scrape_mode, keyword, url, output_folder, images_to_download, num_workers, proxy_str):
    """
    Main function that runs the pinscrape logic based on user inputs from Gradio.
    """
    # --- 1. Determine the search query and validate input ---
    if scrape_mode == "By Keyword":
        if not keyword.strip():
            return "Error: Keyword cannot be empty.", []
        search_query = keyword
    else: # By URL
        if not url.strip():
            return "Error: URL cannot be empty.", []
        search_query = url

    if not output_folder.strip():
        output_folder = "output"  # Default if empty
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # --- 2. Proxy Configuration ---
    proxies = {}
    if proxy_str and proxy_str.strip():
        proxies = {"http": proxy_str, "https": proxy_str}
        print(f"Using proxy: {proxies}")

    # --- 3. Run the scraper ---
    log_output = f"Starting scrape for: '{search_query}'\n"
    log_output += f"Mode: {scrape_mode}\n"
    log_output += f"Output Folder: {output_folder}\n"
    log_output += "--------------------------------\n"
    
    try:
        # ** ERROR FIX APPLIED HERE **
        # The first argument is positional, not a keyword argument.
        details = scraper.scrape(
            search_query, 
            output_folder=output_folder, 
            proxies=proxies, 
            number_of_workers=num_workers, 
            max_images=images_to_download
        )
        
        if details.get("isDownloaded"):
            log_output += "Downloading completed successfully!\n"
            log_output += f"Total URLs found: {len(details.get('extracted_urls', []))}\n"
            log_output += f"Total images downloaded: {len(details.get('urls_list', []))}\n"
        else:
            log_output += "Nothing new to download.\n"
            log_output += f"Message from scraper: {details.get('msg', 'No details provided.')}"

    except Exception as e:
        log_output += f"\nAn error occurred: {str(e)}"
        return log_output, []

    # --- 4. Fetch downloaded images for the gallery ---
    time.sleep(1) # Give a moment for files to be written to disk
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif"]
    downloaded_images = []
    # Search in the subfolder created by pinscrape (e.g., output/messi)
    scrape_subfolder = os.path.join(output_folder, search_query.split("/")[-2] if "pinterest.com" in search_query else search_query)
    
    for ext in image_extensions:
        downloaded_images.extend(glob.glob(os.path.join(scrape_subfolder, ext)))
    
    if downloaded_images:
        downloaded_images.sort(key=os.path.getmtime, reverse=True)
        log_output += f"\nDisplaying images from '{scrape_subfolder}'."
    else:
        log_output += f"\nNo image files found in the expected output subfolder '{scrape_subfolder}'. Check logs for details."


    return log_output, downloaded_images[:100] # Return log and a limited number of images

# --- Gradio UI Definition ---

with gr.Blocks(theme=gr.themes.Soft(), title="PinScrape UI") as demo:
    gr.Markdown("# 🖼️ Pinterest Scraper UI")
    gr.Markdown("A user-friendly interface for the `pinscrape` library. Download images by keyword or from a specific board/pin URL.")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## ⚙️ Settings")
            
            scrape_mode_radio = gr.Radio(
                ["By Keyword", "By URL"],
                label="Scraping Mode",
                value="By Keyword"
            )
            
            keyword_input = gr.Textbox(label="Search Keyword", placeholder="e.g., modern architecture", visible=True)
            url_input = gr.Textbox(label="Pinterest Board/Pin URL", placeholder="https://www.pinterest.com/...", visible=False)
            
            # Add event listener to toggle visibility
            scrape_mode_radio.change(fn=toggle_inputs, inputs=scrape_mode_radio, outputs=[keyword_input, url_input])
            
            output_folder_input = gr.Textbox(label="Output Folder Name", value="output")
            
            with gr.Row():
                images_to_download_slider = gr.Slider(minimum=1, maximum=1000, value=100, step=1, label="Max Images to Download")
                num_workers_slider = gr.Slider(minimum=1, maximum=20, value=10, step=1, label="Download Workers")
            
            proxy_input = gr.Textbox(label="Proxy (Optional)", placeholder="http://user:pass@host:port")
            
            start_button = gr.Button("Start Scraping", variant="primary")

        with gr.Column(scale=2):
            gr.Markdown("## 📝 Results")
            log_output = gr.Textbox(label="Log Output", lines=10, interactive=False, placeholder="Scraping status will appear here...")
            image_gallery = gr.Gallery(label="Downloaded Images", show_label=True, elem_id="gallery", columns=5, height="auto")

    # Connect the button to the main function
    start_button.click(
        fn=run_scraper,
        inputs=[
            scrape_mode_radio,
            keyword_input,
            url_input,
            output_folder_input,
            images_to_download_slider,
            num_workers_slider,
            proxy_input
        ],
        outputs=[
            log_output,
            image_gallery
        ]
    )

if __name__ == "__main__":
    demo.launch()