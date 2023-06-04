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
            messages=[
                {"role": "system", "content": "대학교 교안을 주면 너는 시험 대비 문제를 만들어야 된다. 말이 안되거나 너가 보기에 이상한 문제는 만들면 안된다."},
                {"role": "user", "content": question},
                ])

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
        
        '''
        타입1-1-1: 1. Decision Boundaries를 표현하는 방법은?
                  답: Voronoi diagram
                  2. ...
        
        타입1-1-2: 1. "실증주의 역사"에서 역사가의 임무는 무엇인가?
                  답: 실제로 어떠했는지를 보여주는 것.
                
                  2. ...
                        
        타입1-2-2: 1. 역사의 문서로는 무엇들이 있는가? : 법령들, 조약들, 지대 대장, 보고서, 공적 통신문, 서신, 일기
                  2. ...    
                    
        타입1-2-2: 1. 과학자들은 문제해결을 위해 어떤 태도를 취하는가? : 보수적으로 기다리려 함 : 
                  2. ...
                        
                      
        타입2-1: 문제 1 : 로마의 원형 경기장은 어떤 양식의 기둥으로 만들어졌는가?
                답 : 코린트 양식의 반원 기둥
                
                문제 2 : ...
                
                <뽀나스 띄어쓰기>
                문제 1: 로마의 원형 경기장은 어떤 양식의 기둥으로 만들어졌는가?
                
        타입2-2: 문제 1 : 화학산업이 생산하는 것은 무엇인가?
                답 : 폐기물
                문제 2 : ...
        '''
        
        # 문제와 답을 저장할 리스트 초기화
        questionList = []
        answerList = []
                    
        gpt_split_1 = gpt_ans.split("\n")

        # 타입 1
        if gpt_ans[0] == '1':

            # 타입  1-1
            if gpt_split_1[1][0] == '답':

                for gs in gpt_split_1:
                    
                    # 1-1-2 거르기
                    if gs == '':
                        continue
                    if gs[0] == '답':
                        answer = gs[3:]
                        answerList.append(answer.lstrip())
                    else:
                        question = gs[3:]
                        questionList.append(question.lstrip())
                        
            # 타입 1-2
            elif gpt_split_1[1][0] == '2':
                
                for gs in gpt_split_1:
                    question = gs.split(':')[0].lstrip()
                    answer = gs.split(':')[1].lstrip()
                    
                    questionList.append(question[3:])
                    answerList.append(answer)
            else:
                print("Filtering 오류")
                return False, False
            
        # 타입 2
        elif gpt_ans[0] == '문':
            
            for gs in gpt_split_1:
                    
                # 2-1-2 거르기
                if gs == '':
                    continue
                if gs[0] == '답':
                    answer = gs.split(':')[1].lstrip()
                    answerList.append(answer)
                else:
                    question = gs.split(':')[1].lstrip()
                    questionList.append(question)
                
        else:
            print("Filtering 오류")
            return False, False
            
        # 결과 출력
        print(questionList)
        print(answerList)
            
        return questionList, answerList 
