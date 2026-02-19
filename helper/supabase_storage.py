import os
import uuid
import streamlit as st
from supabase import create_client


# -------------------------------------
# GET SUPABASE CREDENTIALS
# -------------------------------------
def get_supabase_credentials():
    """
    Works both locally (.env) and on Streamlit Cloud (st.secrets)
    """

    # 1️⃣ Streamlit Cloud
    if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
        return st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"]

    # 2️⃣ Local environment (.env or system env)
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if url and key:
        return url, key

    raise ValueError("Supabase credentials not found.")


SUPABASE_URL, SUPABASE_KEY = get_supabase_credentials()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "missing-person-images"


# -------------------------------------
# UPLOAD IMAGE FUNCTION
# -------------------------------------
def upload_image(file_or_bytes, original_filename=None):
    """
    Flexible upload function.
    Works with:
    1) upload_image(file_object)
    2) upload_image(file_bytes, filename)
    """

    try:
        # Case 1: Streamlit file uploader object
        if original_filename is None:
            file_obj = file_or_bytes
            file_bytes = file_obj.getvalue()
            original_filename = file_obj.name
            content_type = file_obj.type
        else:
            # Case 2: bytes + filename
            file_bytes = file_or_bytes
            content_type = "image/jpeg"

        # Extract extension safely
        file_ext = original_filename.split(".")[-1].lower()

        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}.{file_ext}"

        # Upload to Supabase storage
        supabase.storage.from_(BUCKET_NAME).upload(
            unique_filename,
            file_bytes,
            {"content-type": content_type},
        )

        # Get public URL
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(
            unique_filename
        )

        return public_url

    except Exception as e:
        print("Upload error:", e)
        return None
