import openai
import os
import convert
import re

class CreateExam:
    
    def __init__(self, key):
        
        openai.api_key = key
    
    def sendMessage(self, question):
        
        # 질문하기
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": question}])

        # 답변 가져오기
        ans = res.choices[0].message.content
        
        return ans
    
    def filter(self, gpt_ans):
        
        print(f'gpt answered: {gpt_ans}')
        question = gpt_ans.split('[')[0] # 생성된 문제
        answer = re.findall('\[([^]]+)', gpt_ans) # 괄호 안의 답변 빼오기. 리스트 형식으로 반한됨.
        
        try:
            answer_str = answer[0]
        except IndexError:
            print("list index out of range")
            print(f"type is {type(answer)}")
            print(answer)
            
        return question, answer_str 