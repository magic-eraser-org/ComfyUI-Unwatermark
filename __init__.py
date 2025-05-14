# custom_nodes/remove_watermark_node/__init__.py

from .remove_watermark_by_unwatermark import RemoveWatermark

NODE_CLASS_MAPPINGS = {
    "Remove Watermark": RemoveWatermark,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Remove Watermark": "🧼 Remove Watermark (API)",
}
