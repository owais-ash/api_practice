from flask import Flask, request, render_template, jsonify
from pdfminer.high_level import extract_text
from difflib import ndiff
import os

app = Flask(__name__)

class PDFComparator:
    def __init__(self, file1_path, file2_path):
        self.file1_path = file1_path
        self.file2_path = file2_path

    def extract_text_from_pdf(self, file_path):
        return extract_text(file_path)

    def compare_texts(self, text1, text2):
        diff = ndiff(text1.splitlines(), text2.splitlines())
        changes = [line for line in diff if line.startswith('+ ') or line.startswith('- ')]
        return self.group_changes_by_paragraph(changes)

    def group_changes_by_paragraph(self, changes):
        paragraphs = []
        paragraph = []

        for line in changes:
            if line.strip() == '':
                if paragraph:
                    paragraphs.append(paragraph)
                    paragraph = []
            else:
                paragraph.append(line)

        if paragraph:
            paragraphs.append(paragraph)

        return paragraphs

    def get_changes(self):
        text1 = self.extract_text_from_pdf(self.file1_path)
        text2 = self.extract_text_from_pdf(self.file2_path)
        return self.compare_texts(text1, text2)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/compare_pdfs', methods=['POST'])
def compare_pdfs():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"error": "Please upload both PDF files"}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    file1_path = os.path.join("/tmp", file1.filename)
    file2_path = os.path.join("/tmp", file2.filename)

    file1.save(file1_path)
    file2.save(file2_path)

    comparator = PDFComparator(file1_path, file2_path)
    changes = comparator.get_changes()

    os.remove(file1_path)
    os.remove(file2_path)

    return jsonify({"changes": changes})

if __name__ == '__main__':
    app.run(debug=True)
