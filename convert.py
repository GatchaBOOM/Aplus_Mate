# -*- coding: utf8 -*-
import fitz
from fpdf import FPDF
import random
import tiktoken
import logging

class Convert:
    
    def __init__(self, pdf_file, cnt):
        '''
        pdf_file: pdf 파일 경로
        cnt: 문제 생성할 횟수
        ''' 
        
        self.pdf_file = pdf_file
        self.cnt = cnt
        
        self.doc = fitz.open(self.pdf_file)
        self.page_list = []
        
        
    def getGPTInput(self):
        
        self.pickPages()
        text = self.pdf2txt()
        
        return text
    
    def checkToken(self, text):
        # 문장 너무 길면 쪼개기
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        num_tokens = len(encoding.encode(text))
        
        if num_tokens > 2000:
            ratio = num_tokens//2000    
            length = len(text)//ratio
            num_tokens = num_tokens // ratio//2
            devided_txt = text[0:length//2]
            print(f'modified num_token: {num_tokens}')
            return devided_txt
        
        else:
            print(f'pure num_token: {num_tokens}')
            return text
    
    def pickPages(self,):
        # PDF 페이지 수
        num = self.doc.page_count
        
        for i in range(self.cnt):
            '''
            처음 몇 장은 제목, 개요 이런 내용이라 생각해서 제외
            나머지 페이지 중에서 cnt 개수만큼 랜덤으로 페이지 번호 추출
            '''
            
            p = random.randint(3, num-3)
            self.page_list.append(p)
            
    def pdf2txt(self):
        
        '''
        pnum: pickPage()에서 랜덤으로 뽑은 난수 페이지 번호
        ppnum: pnum과 다음페이지까지 두장의 내용을 추출해서 한 문제 생성
        '''
        text = ''
        for pnum in self.page_list:
            for ppnum in range(pnum, pnum+1):
                page = self.doc.load_page(ppnum)
                text += page.get_text()
        
        text = self.checkToken(text)
        
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
        for a in ans:
            pdf.write(8, a+'\n\n')
        
        
        pdf.output("output.pdf", 'F')
