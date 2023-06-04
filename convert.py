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
        self.num = 0
        self.page = 0
        
        self.doc = fitz.open(self.pdf_file)
        self.page_list = []
        
    def getGPTInput(self):
        print("getGPTInput")
        page = self.pickPages()
        text = self.pdf2txt(page)
        
        return text
    
    def checkToken(self, text):
        # 문장 너무 길면 쪼개기
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        num_tokens = len(encoding.encode(text))
        
        if num_tokens > 500:
            ratio = num_tokens//500    
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
        self.num = self.doc.page_count
        print("pickPages")
        '''
        처음 몇 장은 제목, 개요 이런 내용이라 생각해서 제외
        나머지 페이지 중에서 cnt 개수만큼 랜덤으로 페이지 번호 추출
        '''
        
        if self.num < 5:
            self.page = random.randint(1, self.num)
        else:
            while True:
                self.page = random.randint(1, self.num)
                if self.page not in self.page_list:
                    break
            
        self.page_list.append(self.page)
        print(f"{self.page} 페이지에서 추출")
        
        return self.page
        
    def pdf2txt(self, page_num):
        print("pdf2txt")
        '''
        page: pickPage()에서 랜덤으로 뽑은 난수 페이지 번호
        ppnum: pnum과 다음페이지까지 두장의 내용을 추출해서 한 문제 생성
        '''
        text = ''
        if self.num == page_num:
            page = self.doc.load_page(page_num-1)
            text += page.get_text()
            
        else:
            for ppnum in range(page_num, page_num+1):
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
        pdf.add_font('Basic', '', './fonts/Arial_Unicode.ttf', uni=True)
        # 제목
        pdf.set_font('Bold', '', 25)
        name = self.pdf_file.split('.')[-2]
        pdf.cell(200, 10, txt = f'Question',ln = 1, align = 'C')
        pdf.write(15, '\n')
        pdf.set_font('Medium', '', 10)
        pdf.cell(200, 0, txt = '에이플메이트',ln = 1, align = 'C')
        pdf.write(15, '\n\n')
        
        # 문제
        pdf.set_font('Basic', '', 14)
        for q in qst:
            pdf.write(8, q+'\n\n')
        
        
        # 답안
        pdf.add_page()
        pdf.set_font('Bold', '', 25)
        name = self.pdf_file.split('.')[-2]
        pdf.cell(200, 10, txt = f'Answer',ln = 1, align = 'C')
        pdf.write(15, '\n')
        pdf.set_font('Medium', '', 10)
        pdf.cell(200, 0, txt = '에이플메이트',ln = 1, align = 'C')
        pdf.write(15, '\n\n')
        
        pdf.set_font('Basic', '', 14)
        for a in ans:
            pdf.write(8, a+'\n\n')
        
        
        pdf.output("output.pdf", 'F')