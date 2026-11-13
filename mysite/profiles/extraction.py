import logging
import os
import re

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from pypdf import PdfReader

from .models import Resume

logger = logging.getLogger(__name__)

MAX_PDF_PAGES = 25
MAX_TEXT_CHARS = 100_000

_CONTROL_CHARS = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')


class ExtractionError(Exception):
    """The file is genuine, but its text cannot be read (e.g. a password-protected PDF)."""


def _pdf_text(stored):
    reader = PdfReader(stored)
    if reader.is_encrypted:
        raise ExtractionError('The PDF is password protected.')
    pages = reader.pages[:MAX_PDF_PAGES]
    return '\n\n'.join((page.extract_text() or '') for page in pages)


def _docx_text(stored):
    document = Document(stored)
    lines = []
    # Walk the body in order so paragraphs and tables stay in their original sequence.
    for child in document.element.body.iterchildren():
        if child.tag.endswith('}p'):
            lines.append(Paragraph(child, document).text)
        elif child.tag.endswith('}tbl'):
            for row in Table(child, document).rows:
                cells = []
                for cell in row.cells:
                    text = cell.text.strip()
                    if text and text not in cells:  # merged cells repeat
                        cells.append(text)
                lines.append(' | '.join(cells))
    return '\n'.join(lines)


def _clean(text):
    text = _CONTROL_CHARS.sub('', text)
    text = '\n'.join(line.strip() for line in text.splitlines())
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()[:MAX_TEXT_CHARS]


def extract_text(stored, extension):
    if extension == '.pdf':
        return _clean(_pdf_text(stored))
    if extension == '.docx':
        return _clean(_docx_text(stored))
    raise ExtractionError('Unsupported file type.')


def extract_resume_text(resume):
    """Read the resume's text into the database and record how it went."""
    extension = os.path.splitext(resume.file.name)[1].lower()
    try:
        with resume.file.open('rb') as stored:
            text = extract_text(stored, extension)
        resume.extracted_text = text
        resume.text_status = (
            Resume.TextStatus.EXTRACTED if text else Resume.TextStatus.NO_TEXT
        )
    except Exception as error:
        # Never log the resume's content, only what kind of error happened.
        logger.warning(
            'Resume text extraction failed for user %s: %s',
            resume.user_id,
            type(error).__name__,
        )
        resume.extracted_text = ''
        resume.text_status = Resume.TextStatus.FAILED
    resume.save(update_fields=['extracted_text', 'text_status'])