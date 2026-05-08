# pdf_adapter.py - Adaptador de extraccion documental
# -------------------------------------------------------------------------
import fitz  # PyMuPDF
import re
import os

class PDFAdapter:
    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        Extrae y limpia el texto de un archivo PDF.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"El archivo no existe: {pdf_path}")
            
        text = ""
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                text += page.get_text("text") + "\n"
            doc.close()
        except Exception as e:
            return f"Error al procesar el PDF: {str(e)}"
            
        return PDFAdapter._clean_text(text)

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Limpia el ruido del texto extraido.
        """
        # Eliminar multiples saltos de linea y espacios en blanco extra
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

if __name__ == "__main__":
    # Test rapido
    print("PDFAdapter cargado correctamente.")
