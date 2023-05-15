from convert import Convert
from create import CreateExam
import os
from dotenv import load_dotenv

load_dotenv()
OPEN_AI_KEY = os.environ.get("PRIVATE_KEY")

key = OPEN_AI_KEY
file = '서고강원본.pdf'
cnt = 3

ce = CreateExam(key)
con = Convert(file, cnt)

qst_list = []
ans_list = []

for i in range(cnt):
      
      # GPT한테 질문할 내용 만들기
      txt = con.getGPTInput()
      input_cmd = f'''Please make only one short answer question from the contents of "{txt}",
      For example, "Which country's capital is Seoul?[Korea]". And answer me in Korean.
      '''
      
      # GPT한테 질문 쏘기
      ans = ce.sendMessage(input_cmd)
      # 답변 정제
      filtered_qst, filtered_ans = ce.filter(ans)
      qst_list.append(f'{i+1}번. ' + filtered_qst)
      ans_list.append(f'{i+1}번. ' + filtered_ans)
      
print(f'''
      생성된 문제: {qst_list},
      생성된 답안: {ans_list}
      ''')

con.txt2pdf(qst_list, ans_list)
