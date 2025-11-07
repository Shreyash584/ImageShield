import io
import uuid
from pathlib import Path
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.contrib import messages
from PIL import Image, UnidentifiedImageError

from .forms import EncryptForm, DecryptForm
from .utils import generate_key_16chars, aes_encrypt_with_hash, aes_decrypt_verify

ENCRYPTED_DIR = Path(settings.MEDIA_ROOT) / "encrypted"
UPLOADS_DIR = Path(settings.MEDIA_ROOT) / "uploads"
ENCRYPTED_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

def index(request):
    return render(request, "shield_app/index.html", {
        "encrypt_form": EncryptForm(),
        "decrypt_form": DecryptForm(),
    })

def encrypt_image(request):
    if request.method != "POST":
        return render(request, "shield_app/index.html", {
            "encrypt_form": EncryptForm(),
            "decrypt_form": DecryptForm(),
        })

    form = EncryptForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, "Please provide a valid image.")
        return render(request, "shield_app/index.html", {
            "encrypt_form": form,
            "decrypt_form": DecryptForm(),
        })

    img_file = form.cleaned_data['image']
    data = img_file.read()

    # Optional: sanity-check it’s an image
    try:
        Image.open(io.BytesIO(data)).verify()
    except UnidentifiedImageError:
        messages.error(request, "Uploaded file is not a valid image.")
        return render(request, "shield_app/index.html", {
            "encrypt_form": form,
            "decrypt_form": DecryptForm(),
        })

    key = generate_key_16chars()
    blob = aes_encrypt_with_hash(data, key)

    # Save encrypted as <uuid>__<orig_name>.bin
    enc_name = f"{uuid.uuid4().hex}__{Path(img_file.name).name}.bin"
    enc_path = ENCRYPTED_DIR / enc_name
    enc_path.write_bytes(blob)

    messages.success(request, "Image encrypted successfully.")
    return render(request, "shield_app/index.html", {
        "encrypt_form": EncryptForm(),
        "decrypt_form": DecryptForm(),
        "generated_key": key,
        "encrypted_relpath": f"{settings.MEDIA_URL}encrypted/{enc_name}",
        "encrypted_filename": enc_name,
    })

def decrypt_image(request):
    if request.method != "POST":
        return render(request, "shield_app/index.html", {
            "encrypt_form": EncryptForm(),
            "decrypt_form": DecryptForm(),
        })

    form = DecryptForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, "Provide the encrypted file and the 16-char key.")
        return render(request, "shield_app/index.html", {
            "encrypt_form": EncryptForm(),
            "decrypt_form": form,
        })

    enc_file = form.cleaned_data['encrypted_file']
    key = form.cleaned_data['key']

    blob = enc_file.read()
    try:
        data = aes_decrypt_verify(blob, key)
    except ValueError as e:
        messages.error(request, str(e))
        return render(request, "shield_app/index.html", {
            "encrypt_form": EncryptForm(),
            "decrypt_form": form,
        })

    # Try to guess image format and add extension
    img_ext = "png"
    try:
        img = Image.open(io.BytesIO(data))
        fmt = (img.format or "PNG").lower()
        # Common normalization
        ext_map = {"jpeg": "jpg", "jpg": "jpg", "png": "png", "webp": "webp", "bmp": "bmp", "gif": "gif", "tiff":"tif"}
        img_ext = ext_map.get(fmt, "png")
    except UnidentifiedImageError:
        # If it’s not a valid image, still save bytes for debugging
        messages.warning(request, "Decrypted bytes were not recognized as an image; saving raw data.")
        img_ext = "bin"

    out_name = f"decrypted_{uuid.uuid4().hex}.{img_ext}"
    out_path = UPLOADS_DIR / out_name
    out_path.write_bytes(data)

    messages.success(request, "File decrypted and verified successfully.")
    return render(request, "shield_app/index.html", {
        "encrypt_form": EncryptForm(),
        "decrypt_form": DecryptForm(),
        "decrypted_relpath": f"{settings.MEDIA_URL}uploads/{out_name}",
        "decrypted_filename": out_name,
    })
