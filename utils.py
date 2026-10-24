import os
import platform
import subprocess

# Get base project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cross-version Pillow resampling filter
try:
    from PIL import Image
    try:
        LANCZOS_RESAMPLE = Image.Resampling.LANCZOS
    except AttributeError:
        try:
            LANCZOS_RESAMPLE = Image.LANCZOS
        except AttributeError:
            LANCZOS_RESAMPLE = getattr(Image, 'ANTIALIAS', 1)
except ImportError:
    Image = None
    LANCZOS_RESAMPLE = None

def get_asset_path(subpath):
    """
    Normalizes asset paths across Windows, macOS, and Linux.
    Accepts paths like 'Images_GUI\\banner.jpg' or 'banner.jpg' and returns
    an absolute path that exists.
    """
    normalized = subpath.replace('\\', os.sep).replace('/', os.sep)
    # If it's already an absolute path and exists, return it
    if os.path.isabs(normalized) and os.path.exists(normalized):
        return normalized

    # Try relative to BASE_DIR directly
    direct = os.path.join(BASE_DIR, normalized)
    if os.path.exists(direct):
        return direct

    # Try inside Image_GUI
    filename = os.path.basename(normalized)
    in_img_gui = os.path.join(BASE_DIR, "Image_GUI", filename)
    if os.path.exists(in_img_gui):
        return in_img_gui

    # Try inside Images_GUI
    in_imgs_gui = os.path.join(BASE_DIR, "Images_GUI", filename)
    if os.path.exists(in_imgs_gui):
        return in_imgs_gui

    return direct

def open_directory(path):
    """
    Cross-platform folder opening utility (replaces Windows-only os.startfile).
    """
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        os.makedirs(abs_path, exist_ok=True)

    system = platform.system()
    if system == "Windows":
        os.startfile(abs_path)
    elif system == "Darwin":
        subprocess.run(["open", abs_path], check=False)
    else:
        subprocess.run(["xdg-open", abs_path], check=False)
