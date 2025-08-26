import gradio as gr
import os
import glob
import time
from pinscrape import scraper, Pinterest

# --- Core Scraping Logic ---

def run_scraper(method, keyword, output_folder, images_to_download, num_workers, proxy_str):
    """
    Main function that runs the pinscrape logic based on user inputs from Gradio.
    """
    # --- 1. Input Validation ---
    if not keyword.strip():
        return "Error: Keyword cannot be empty.", []
    if not output_folder.strip():
        output_folder = "output" # Default if empty
    
    # Ensure folder exists
    os.makedirs(output_folder, exist_ok=True)

    # --- 2. Proxy Configuration ---
    proxies = {}
    if proxy_str and proxy_str.strip():
        proxies = {
            "http": proxy_str,
            "https": proxy_str
        }
        print(f"Using proxy: {proxies}")

    # --- 3. Run the selected scraping method ---
    log_output = f"Starting scrape for '{keyword}'...\n"
    log_output += f"Method: {method}\n"
    log_output += f"Output Folder: {output_folder}\n"
    log_output += "--------------------------------\n"
    
    try:
        if method == "Search Engine (Recommended)":
            log_output += "Note: 'Number of Workers' is ignored for the 'Search Engine' method.\n"
            details = scraper.scrape(
                keyword, 
                output_folder=output_folder, 
                proxies=proxies, 
                # FIXED: Removed the unsupported 'number_of_workers' argument.
                max_images=images_to_download
            )
            if details.get("isDownloaded"):
                log_output += "Downloading completed successfully!\n"
                log_output += f"Total URLs found: {len(details.get('extracted_urls', []))}\n"
                log_output += f"Total images downloaded: {len(details.get('urls_list', []))}\n"
            else:
                log_output += "Nothing new to download.\n"
                log_output += f"Message from scraper: {details.get('msg', 'No details provided.')}"

        elif method == "Direct API (Advanced)":
            p = Pinterest(proxies=proxies)
            images_urls = p.search(keyword, images_to_download)
            log_output += f"Found {len(images_urls)} image URLs via API.\n"
            if images_urls:
                # This part was already correct and remains unchanged.
                details = p.download(
                    url_list=images_urls, 
                    number_of_workers=num_workers, 
                    output_folder=output_folder
                )
                log_output += f"Successfully downloaded {len(details.get('success', []))} images.\n"
                if details.get('failed'):
                    log_output += f"Failed to download {len(details.get('failed', []))} images.\n"
            else:
                log_output += "No images found to download.\n"
        
        else:
            return "Error: Invalid method selected.", []

    except Exception as e:
        log_output += f"\nAn error occurred: {str(e)}"
        return log_output, []


    # --- 4. Fetch downloaded images for the gallery ---
    # Give a moment for files to be written to disk
    time.sleep(1) 
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif"]
    downloaded_images = []
    for ext in image_extensions:
        downloaded_images.extend(glob.glob(os.path.join(output_folder, ext)))
    
    # Sort by modification time to show newest first and limit display
    if downloaded_images:
        downloaded_images.sort(key=os.path.getmtime, reverse=True)
    
    log_output += f"\nFound {len(downloaded_images)} image files in '{output_folder}'."

    return log_output, downloaded_images[:100] # Return log and a limited number of images for the gallery

# --- Gradio UI Definition (No changes needed for this fix) ---

with gr.Blocks(theme=gr.themes.Soft(), title="PinScrape UI") as demo:
    gr.Markdown("# 🖼️ Pinterest Scraper UI")
    gr.Markdown("A user-friendly interface for the [pinscrape](https://github.com/derhnyel/pinscrape) library. Enter your settings and click 'Start Scraping'.")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## ⚙️ Settings")
            method_select = gr.Radio(
                ["Search Engine (Recommended)", "Direct API (Advanced)"],
                label="Scraping Method",
                value="Search Engine (Recommended)"
            )
            keyword_input = gr.Textbox(label="Search Keyword", placeholder="e.g., modern architecture")
            output_folder_input = gr.Textbox(label="Output Folder Name", value="output")
            
            with gr.Row():
                images_to_download_slider = gr.Slider(minimum=1, maximum=1000, value=100, step=1, label="Images to Download")
                num_workers_slider = gr.Slider(minimum=1, maximum=20, value=10, step=1, label="Download Workers")
            
            proxy_input = gr.Textbox(label="Proxy (Optional)", placeholder="http://user:pass@host:port")
            
            start_button = gr.Button("Start Scraping", variant="primary")

        with gr.Column(scale=2):
            gr.Markdown("## 📝 Results")
            log_output = gr.Textbox(label="Log Output", lines=10, interactive=False, placeholder="Scraping status will appear here...")
            image_gallery = gr.Gallery(label="Downloaded Images", show_label=True, elem_id="gallery", columns=5, height="auto")

    # Connect the button to the function
    start_button.click(
        fn=run_scraper,
        inputs=[
            method_select,
            keyword_input,
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