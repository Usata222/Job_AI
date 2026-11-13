import os
import zipfile

from django.conf import settings
from rest_framework import serializers

ALLOWED_EXTENSIONS = ('.pdf', '.docx')

PDF_MAGIC = b'%PDF-'
ZIP_MAGIC = b'PK\x03\x04'  # .docx files are zip archives

MAX_UNZIPPED_BYTES = 50 * 1024 * 1024
MAX_ZIP_ENTRIES = 2000


def _looks_like_docx(upload):
    """A real .docx is a zip holding word/document.xml. Also refuses zip bombs."""
    try:
        with zipfile.ZipFile(upload) as archive:
            entries = archive.infolist()
            if len(entries) > MAX_ZIP_ENTRIES:
                return False
            if sum(entry.file_size for entry in entries) > MAX_UNZIPPED_BYTES:
                return False
            names = {entry.filename for entry in entries}
            return '[Content_Types].xml' in names and 'word/document.xml' in names
    except zipfile.BadZipFile:
        return False
    finally:
        upload.seek(0)


def validate_resume_file(upload):
    extension = os.path.splitext((upload.name or '').lower())[1]
    if extension not in ALLOWED_EXTENSIONS:
        raise serializers.ValidationError('Only PDF and DOCX files are allowed.')

    if upload.size > settings.RESUME_MAX_UPLOAD_BYTES:
        limit_mb = settings.RESUME_MAX_UPLOAD_BYTES // (1024 * 1024)
        raise serializers.ValidationError(f'The file is too large. The limit is {limit_mb} MB.')

    # Check what the file really is. The extension and the content-type header
    # are both supplied by the user, so neither is trusted.
    head = upload.read(8)
    upload.seek(0)
    if extension == '.pdf':
        genuine = head.startswith(PDF_MAGIC)
    else:
        genuine = head.startswith(ZIP_MAGIC) and _looks_like_docx(upload)

    if not genuine:
        raise serializers.ValidationError(
            "The file's contents do not match its extension, or the file is damaged."
        )