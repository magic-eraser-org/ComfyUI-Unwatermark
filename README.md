# ComfyUI-Unwatermark

**ComfyUI-Unwatermark: A ComfyUI custom node to intelligently remove watermarks from images using the unwatermark.ai API.**

This custom node for ComfyUI allows you to easily remove watermarks from your images by leveraging the power of the unwatermark.ai API.

## Features

*   Integrates with the unwatermark.ai API for watermark removal.
*   Processes images individually within a batch.
*   Handles API key input securely.
*   Includes retry logic for API calls to improve reliability.
*   Returns the original image if processing fails after multiple retries.
*   Provides logging for monitoring the process.

## Installation

1.  **Clone the repository:**
    Navigate to your `ComfyUI/custom_nodes/` directory and clone this repository:
    ```bash
    git clone https://github.com/YOUR_USERNAME/ComfyUI-Unwatermark.git
    ```
    (Please replace `YOUR_USERNAME` with your GitHub username or the actual project URL)

2.  **Install dependencies:**
    This node relies on the `requests` library. If you don\'t have it installed in your ComfyUI Python environment, you might need to install it:
    ```bash
    pip install requests
    ```
    (Ensure you are using the pip associated with your ComfyUI\'s Python environment.)

3.  **Restart ComfyUI:**
    After installation, restart your ComfyUI.

## How to Use

1.  **Get an API Key:**
    *   You need an API key from [unwatermark.ai](https://unwatermark.ai/). Visit their website to sign up and obtain your key.

2.  **Add the Node in ComfyUI:**
    *   In ComfyUI, right-click on the canvas or use the "Add Node" menu.
    *   You should find the "Remove Watermark" node under the "🧼 Image Processing" category (or search for "Remove Watermark").

3.  **Connect Inputs:**
    *   **image:** Connect an image output from another node (e.g., LoadImage, VAE Decode, etc.) to the `image` input of the "Remove Watermark" node.
    *   **api\_key:** Enter your `unwatermark.ai` API key into the `api_key` field.

4.  **Get Output:**
    *   The node will output the processed image (hopefully, without the watermark). If the API call fails or an error occurs, it will attempt to return the original image.

## Configuration

*   **api\_key (String):** Your API key for `unwatermark.ai`. This is a required field.

## Troubleshooting

*   **API Key Errors:** Ensure your API key is correct and has not expired or exceeded its quota on `unwatermark.ai`.
*   **"ModuleNotFoundError: No module named \'requests\'"**: Make sure you have installed the `requests` library in the correct Python environment used by ComfyUI.
*   **Image Format:** The node expects images in a format that PIL (Pillow) can handle. Common formats like JPEG and PNG should work.
*   **Check Logs:** For detailed information or errors, check the ComfyUI console logs. The node provides logging messages about its progress and any issues encountered.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details (if you plan to add one).

## Acknowledgements

*   This node uses the [unwatermark.ai](https://unwatermark.ai/) API for watermark removal.
