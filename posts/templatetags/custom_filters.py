
from django import template
import io
from pdfminer.high_level import extract_text
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from pdfminer.converter import HTMLConverter

register = template.Library()

@register.filter
def endswith(value, arg):
    """
    Custom template filter to check if a string ends with a certain suffix.
    """
    return value.endswith(arg)

# custom_filters.py

register = template.Library()

@register.filter
def pdf_to_text(pdf_file):
    """
    Custom template filter to extract text from a PDF file.
    """
    text = io.StringIO()
    with open(pdf_file.path, 'rb') as f:
        extract_text(f, text)
    return text.getvalue()

@register.filter
def pdf_to_html(pdf_file):
    """
    Custom template filter to convert a PDF file to HTML.
    """
    output_string = io.StringIO()
    with open(pdf_file.path, 'rb') as f:
        extract_text_to_fp(f, output_string, laparams=LAParams(), output_type='html', codec=None)
    return output_string.getvalue()

