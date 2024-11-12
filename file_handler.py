import os
from PyPDF2 import PdfReader
from docx import Document
import markdown2


class FileHandler:
    def read_file_contents(self, file_path):
        """Read the contents of a file based on its extension."""
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()

        try:
            if extension == ".pdf":
                return self._read_pdf(file_path)
            elif extension == ".txt":
                return self._read_text(file_path)
            elif extension in [".doc", ".docx"]:
                return self._read_doc(file_path)
            elif extension == ".md":
                return self._read_markdown(file_path)
            else:
                raise ValueError(f"Unsupported file type: {extension}")
        except Exception as e:
            raise RuntimeError(f"Error reading file: {str(e)}")

    def _read_pdf(self, file_path):
        pdf_reader = PdfReader(file_path)
        return "".join([page.extract_text() for page in pdf_reader.pages])

    def _read_text(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def _read_doc(self, file_path):
        document = Document(file_path)
        return "\n".join([paragraph.text for paragraph in document.paragraphs])

    def _read_markdown(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return markdown2.markdown(file.read())