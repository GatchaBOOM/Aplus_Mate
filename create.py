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
        
        # 문제를 한개가 아니라 여러개 만들어 내면 다시 
        if (gpt_ans.count('?') > 1) or (gpt_ans.count('[') > 3):
            print("여러 문제 생성 탐지")
            return False, False
        
        # GPT의 답변 형식에 따라 구분
        if '[' == gpt_ans[0]: # [문제] [답변] 형식
            print('1번 대답 형식')
            question = re.findall('\[([^]]+)', gpt_ans)[0]
            answer = re.findall('\[([^]]+)', gpt_ans)[1]
        
        elif ' - ' in gpt_ans: # 문제 - 답변 형식
            print('3번 대답 형식')
            question = gpt_ans.split(' - ')[0]
            answer = gpt_ans.split(' - ')[1]
            
        elif '[' in gpt_ans: # 문제 [답변] 형식
            print('2번 대답 형식')
            question = gpt_ans.split('[')[0] # 생성된 문제
            answer = re.findall('\[([^]]+)', gpt_ans)[-1] # 괄호 안의 답변 빼오기. 리스트 형식으로 반한됨.
            
        else:
            print('이상하게 말해서 다시 함미다잉')
            return False, False
            

        # 답변에 가끔 따옴표 같이 보내줌
        question = question.replace('"','')
        answer = answer.replace('"','')
        
        if ('대한민국의' in question) or ('수도' in question) or ('서울' in answer):
            print('그 놈의 대한민국 수도')
            return False, False
            
            
        return question, answer 

    

    # 버전 2 필터임
    def filter2(self, gpt_ans):
        print("filter2 시작")
        print(f'gpt answered: {gpt_ans}')
        
        # 문제와 답을 저장할 리스트 초기화
        questionList = []
        answerList = []
        gpt_split = gpt_ans.split("\n\n")

        for gs in gpt_split:
            question, answer = gs.split("\n")
            questionList.append(question[6:])
            answerList.append(answer[3:])

        # 결과 출력
        print(questionList)
        print(answerList)
            
        return questionList, answerList 