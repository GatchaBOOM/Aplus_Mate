# -*- coding: utf8 -*-
import fitz
from fpdf import FPDF

class Convert:
    
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        
    def pdf2txt(self):
        
        doc = fitz.open(self.pdf_file)
        text = ''
        for page in doc:
            text += page.get_text()
        return text
        
        
    def txt2pdf(self, qst, ans):
        
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('Light', '', './fonts/GmarketSansTTFLight.ttf', uni=True)
        pdf.add_font('Medium', '', './fonts/GmarketSansTTFMedium.ttf', uni=True)
        pdf.add_font('Bold', '', './fonts/GmarketSansTTFBold.ttf', uni=True)
        
        # 제목
        pdf.set_font('Bold', '', 25)
        name = self.pdf_file.split('.')[-2]
        pdf.cell(200, 10, txt = f'{name}의 생성 문제',ln = 1, align = 'C')
        pdf.write(15, '\n\n')
        
        # 문제
        pdf.set_font('Medium', '', 14)
        for q in qst:
            pdf.write(8, q+'\n\n')
        
        
        # 답안
        pdf.add_page()
        pdf.set_font('Bold', '', 25)
        name = self.pdf_file.split('.')[-2]
        pdf.cell(200, 10, txt = f'{name}의 생성 문제 답안',ln = 1, align = 'C')
        pdf.write(15, '\n\n')
        
        pdf.set_font('Medium', '', 14)
        for i, a in enumerate(ans):
            pdf.write(8, f'{i}. '+a+'\n\n')
        
        
        pdf.output("output.pdf", 'F')
