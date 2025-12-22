# Import required libraries with auto-installation
import subprocess
import sys
import os

def install_package(package):
    """Silently install a package if not already installed"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])

# Check and install required packages
required_packages = {
    'pdfplumber': 'pdfplumber',
    'gtts': 'gTTS'
}

for import_name, package_name in required_packages.items():
    try:
        __import__(import_name)
    except ImportError:
        print(f"Installing {package_name}...")
        install_package(package_name)

# Now import the libraries
import pdfplumber
from gtts import gTTS

# Check if file path is provided as command-line argument
if len(sys.argv) < 2:
    print("Usage: python text2speech.py <path_to_pdf_file>")
    sys.exit(1)

# Get file path from command-line argument
file_path = sys.argv[1]

# Check if file exists
if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' not found.")
    sys.exit(1)

# Check if file is a PDF
if not file_path.lower().endswith('.pdf'):
    print("Error: File must be a PDF.")
    sys.exit(1)

# Extract PDF text
print(f"Extracting text from '{file_path}'...")
text = ""

try:
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
except Exception as e:
    print(f"Error extracting text from PDF: {e}")
    sys.exit(1)

# Print text length to verify extraction
print(f"Extracted text length: {len(text)} characters")

# Generate output filename based on input filename
output_file = os.path.splitext(os.path.basename(file_path))[0] + ".mp3"

# Convert text to .mp3
print(f"Converting text to speech...")
try:
    tts = gTTS(text, lang='en')
    tts.save(output_file)
    print(f"Audio file saved as '{output_file}'")
except Exception as e:
    print(f"Error converting to speech: {e}")
    sys.exit(1)