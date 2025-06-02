import PyPDF2
import sys

try:
    with open('Reference.pdf', 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        print(text[:10000])  # Print first 10000 characters
except ImportError:
    print("PyPDF2 not available, trying pdfplumber")
    try:
        import pdfplumber
        with pdfplumber.open('Reference.pdf') as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''
            print(text[:10000])
    except ImportError:
        print("No PDF libraries available")
except Exception as e:
    print(f"Error: {e}")