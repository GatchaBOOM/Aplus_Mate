import openai
import os
import convert

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
        # GPT가 만든 문제와 답 리스트
        question = []
        answer = []
        
        ans_splt = gpt_ans.split('\n')
        print('-------------------')
        for one_ans in ans_splt:
            print(one_ans)
            one_ans_splt = one_ans.split(' - ')
            print(one_ans_splt)
            if len(one_ans_splt) > 1:
                question.append(one_ans_splt[0])
                answer.append(one_ans_splt[1])
        
        return question, answer