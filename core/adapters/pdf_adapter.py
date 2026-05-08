import os

class PDFAdapter:
    """Adaptador industrial para extracción de texto de archivos PDF."""
    
    def __init__(self):
        try:
            import fitz # PyMuPDF
            self.fitz = fitz
        except ImportError:
            self.fitz = None

    def extract_text(self, pdf_path: str) -> str:
        """Extrae el contenido textual de un PDF."""
        if not self.fitz:
            return "Error: PyMuPDF no instalado."
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF no encontrado en: {pdf_path}")
            
        doc = self.fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
