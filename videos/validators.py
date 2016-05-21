import mimetypes
from django.core.exceptions import ValidationError

from fourtyone.settings import VIDEO_MIME_TYPES


def validate_video_file(upload):
    """
    Validates uploaded file name by using mimetypes, part of Python standard
    library, to guess the mime type from the file extension.

    The file extension is not a reliable way to determine mime type. A better
    alternative is using the python-magic library, but that requires the
    libmagic library which is extra overhead, so not worth.
    """
    mime_type = mimetypes.MimeTypes().guess_type(upload.name)[0]
    if mime_type not in VIDEO_MIME_TYPES:
        raise ValidationError('File type not supported. MP4, Quicktime, or WebM recommended.')
