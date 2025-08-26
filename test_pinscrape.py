# test_pinscrape.py
from pinscrape import scraper

print("Testing pinscrape...")

# This is the exact function your Gradio app calls for the recommended method
details = scraper.scrape(
    keyword="racecar",
    output_folder="test_output",
    max_images=10
)

print("\n--- Results ---")
print(details)
print("----------------")

if details.get("isDownloaded"):
    print(f"Success! Downloaded {len(details.get('urls_list', []))} images.")
else:
    print(f"Failed to download. Message: {details.get('msg', 'No details provided.')}")