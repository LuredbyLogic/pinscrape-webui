# PinScrape Gradio UI

A user-friendly web interface for the powerful `pinscrape` Python library. This application allows you to easily download images from Pinterest by searching for keywords or providing a direct board/pin URL, all without writing any code.

<img width="249" height="218" alt="logo" src="https://github.com/user-attachments/assets/7e4c4464-d7c1-48b1-bc08-faa9fff9039f" />

---

## ✨ Features

- **Intuitive Web Interface**: Built with Gradio for a clean and simple user experience.
- **Multiple Scraping Modes**:
  - **Search by Keyword**: Find and download images related to any search term.
  - **Scrape from URL**: Extract all images from a specific Pinterest board or pin link.
- **Customizable Parameters**: Easily configure settings like:
  - Output folder for downloaded images.
  - Maximum number of images to download.
  - Number of concurrent download workers for speed.
- **Proxy Support**: Option to use an HTTP/HTTPS proxy for requests.
- **Real-time Logging**: See the status and progress of the scraping job directly in the UI.
- **Image Gallery**: Instantly preview the downloaded images once the job is complete.

## ⚙️ Installation

Make sure you have Python 3.7+ installed.

1.  **Clone the repository (or just save the script):**
    ```bash
    git clone https://github.com/your-username/pinscrape-gradio.git
    cd pinscrape-gradio
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install pinscrape gradio
    ```

## 🚀 How to Run

1.  Navigate to the project directory in your terminal.
2.  Run the application script:
    ```bash
    python app.py
    ```
3.  The terminal will display a local URL, usually `http://127.0.0.1:7860`.
4.  Open this URL in your web browser to access the interface.

## 📋 Usage Guide

1.  **Choose a Scraping Mode**: Select either "By Keyword" or "By URL".
2.  **Provide Input**:
    - If using "By Keyword", enter your search term (e.g., `modern architecture`).
    - If using "By URL", paste the full Pinterest board or pin URL.
3.  **Adjust Settings**:
    - Set the **Output Folder Name**. It will be created if it doesn't exist.
    - Use the sliders to set the **Max Images to Download** and the number of **Download Workers**.
    - (Optional) Enter a proxy URL if you need one.
4.  **Start Scraping**: Click the "Start Scraping" button.
5.  **Monitor Progress**: Watch the "Log Output" for real-time updates.
6.  **View Results**: Once complete, the downloaded images will appear in the "Downloaded Images" gallery. The files will also be saved in your specified output folder.

---

## Credits

- This UI is a wrapper for the excellent [pinscrape](https://github.com/derhnyel/pinscrape) library by derhnyel.
- The web interface is built using the [Gradio](https://www.gradio.app/) framework.
