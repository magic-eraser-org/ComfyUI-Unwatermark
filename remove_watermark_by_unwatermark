import requests
import base64
from PIL import Image
from io import BytesIO
import torch
import torchvision.transforms as T
import logging
import numpy as np
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RemoveWatermark:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "remove_watermark"
    CATEGORY = "🧼 Image Processing"

    def remove_watermark(self, image, api_key):
        try:
            logger.info("Starting image processing...")
            logger.info(f"Input tensor shape: {image.shape}")
            
            # Check if API key is provided
            if not api_key:
                logger.error("API key not provided")
                raise ValueError("Please provide a valid API key")
            
            # Save original batch size for later restoration
            batch_size = image.shape[0]
            
            # ComfyUI usually uses BHWC format, we need to process each image in the batch
            processed_images = []
            
            for i in range(batch_size):
                # Extract single image
                single_image = image[i]
                logger.info(f"Processing batch {i+1}/{batch_size}, shape: {single_image.shape}")
                
                # Ensure pixel values are between 0-1
                if single_image.max() > 1.0:
                    single_image = single_image / 255.0
                
                # ComfyUI usually uses HWC format, PIL needs CHW
                pil_image_converted = None # To ensure pil_image is visible outside the retry loop
                if single_image.shape[-1] in [3, 4]:  # If it's HWC format
                    temp_single_image = single_image
                    # If it's RGBA, convert to RGB
                    if single_image.shape[-1] == 4:
                        temp_single_image = single_image[..., :3]
                    pil_image_converted = T.ToPILImage()(temp_single_image.permute(2, 0, 1))
                else:
                    # Already CHW format
                    pil_image_converted = T.ToPILImage()(single_image)
                
                logger.info(f"PIL image mode: {pil_image_converted.mode}, size: {pil_image_converted.size}")
                
                # Convert PIL image to byte stream
                img_byte_arr = BytesIO()
                pil_image_converted.save(img_byte_arr, format='JPEG')
                img_byte_arr_value = img_byte_arr.getvalue()
                logger.info(f"Image byte size: {len(img_byte_arr_value)} bytes")

                max_retries = 3
                current_retry = 0
                image_processed_successfully = False

                while current_retry < max_retries:
                    logger.info(f"Image {i+1}/{batch_size} - Attempt {current_retry + 1}/{max_retries}")
                    try:
                        logger.info("Calling unwatermark API...")
                        response = requests.post(
                            'https://api.unwatermark.ai/api/unwatermark/api/v1/auto-unWaterMark',
                            headers={'ZF-API-KEY': api_key},
                            files={'original_image_file': ('image.jpg', img_byte_arr_value, 'image/jpeg')},
                            timeout=60
                        )
                        logger.info(f"API response status code: {response.status_code}")
                        
                        if response.status_code == 200:
                            result = response.json()
                            logger.info(f"API response content: {result}")

                            api_code = result.get('code')
                            if api_code == 100000:
                                logger.info("API call successful (code 100000), processing returned results...")
                                output_image_info = result.get('result')
                                processed_image_url = None
                                if output_image_info:
                                    processed_image_url = output_image_info.get('output_image_url')
                                
                                if processed_image_url:
                                    logger.info(f"Successfully retrieved processed image URL: {processed_image_url}")
                                    image_response = requests.get(processed_image_url, timeout=60)
                                    if image_response.status_code == 200:
                                        img_bytes = image_response.content
                                        processed_pil = Image.open(BytesIO(img_bytes)).convert("RGB")
                                        logger.info(f"Processed PIL image mode: {processed_pil.mode}, size: {processed_pil.size}")
                                        
                                        tensor = T.ToTensor()(processed_pil)
                                        tensor = tensor.permute(1, 2, 0)
                                        logger.info(f"Final tensor shape: {tensor.shape}")
                                        
                                        processed_images.append(tensor)
                                        image_processed_successfully = True
                                        break # Successfully processed, break the retry loop
                                    else:
                                        logger.error(f"Failed to download processed image, status code: {image_response.status_code}")
                                else:
                                    logger.error("No output_image_url in API response (code 100000 but missing URL)")
                            else:
                                logger.error(f"API call successful but business logic failed, code: {api_code}, message: {result.get('message')}")
                        else:
                            logger.error(f"API call failed: {response.text}")

                    except requests.exceptions.Timeout:
                        logger.error("API request timed out")
                    except requests.exceptions.RequestException as e:
                        logger.error(f"An exception occurred during API request: {str(e)}")
                    except Exception as e_inner: # Catch exceptions in internal processing logic
                        logger.error(f"Internal error while processing API response: {str(e_inner)}", exc_info=True)
                    
                    # Prepare for retry if not successfully processed
                    if not image_processed_successfully:
                        current_retry += 1
                        if current_retry < max_retries:
                            logger.info(f"Image {i+1}/{batch_size} - Retrying in 3 seconds... (Attempt {current_retry + 1}/{max_retries})")
                            time.sleep(3)
                        else:
                            logger.error(f"Image {i+1}/{batch_size} - All {max_retries} retries failed.")
                    else: # If image_processed_successfully is True, break the loop
                        break 
                
                if not image_processed_successfully:
                    logger.warning(f"Image {i+1}/{batch_size} could not be processed successfully, using original image.")
                    processed_images.append(single_image)
            
            # If at least one image was successfully processed
            if processed_images:
                # Stack all processed images into a batch
                result_tensor = torch.stack(processed_images, dim=0)
                logger.info(f"Final output batch shape: {result_tensor.shape}")
                return (result_tensor,)
            else:
                # If no image was successfully processed, return a blank image
                logger.error("No image was successfully processed")
                return (torch.zeros((batch_size, 64, 64, 3)),)
                
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}", exc_info=True)
            # Return a blank image
            return (torch.zeros((1, 64, 64, 3)),)
