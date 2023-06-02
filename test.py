from convert import Convert
from create import CreateExam
import os
from dotenv import load_dotenv
load_dotenv()
GPT_KEY1 = os.environ.get("GPT_KEY1")
GPT_KEY2 = os.environ.get("GPT_KEY2")
GPT_KEY3 = os.environ.get("GPT_KEY3")

key1 = GPT_KEY1
key2 = GPT_KEY2
key3 = GPT_KEY3

file = '서고강원본.pdf'
cnt = 10

gpt1 = CreateExam(key1)
gpt2 = CreateExam(key2)
gpt3 = CreateExam(key3)

con = Convert(file, cnt)
qst_list = []
ans_list = []
i = 0

while i < cnt:
            
      # GPT한테 질문할 내용 만들기
      txt = con.getGPTInput()
      input_cmd = f'''
      내가 말하는 거에 대해서 시험문제를 만들어줘."대한민국의 수도는 어디인가요? [서울]"처럼 답변은 대괄호안에 넣어서 알려줘.
      "{txt}"의 내용에서 짧은 단답식 문제 1개 만들어줘.
      '''

      # GPT한테 질문 쏘기
      ans = gpt1.sendMessage(input_cmd)
      # 답변 정제
      filtered_qst, filtered_ans = gpt1.filter(ans)

      if filtered_qst is False:
            print("답변 형식 오류로 인한 재생성")
            continue

      qst_list.append(f'{i+1}번. ' + filtered_qst)
      ans_list.append(f'{i+1}번. ' + filtered_ans + f' / {con.page} ~ {con.page+1}페이지')

      i += 1

            
      print(f'''
            생성된 문제: {qst_list},
            생성된 답안: {ans_list}
            ''')

      con.txt2pdf(qst_list, ans_list)