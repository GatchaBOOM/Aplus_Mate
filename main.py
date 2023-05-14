from convert import Convert
from create import CreateExam

key = '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'
file = '서고강원본.pdf'
cnt = 3

ce = CreateExam(key)
con = Convert(file, cnt)

qst_list = []
ans_list = []

for i in range(cnt):
      
      # GPT한테 질문할 내용 만들기
      txt = con.getGPTInput()
      input_cmd = f'''"{txt}"의 내용에서 짧은 단답식 문제를 1개 만들어줘, 조건은 "서울은 어느 나라의 수도인가요?[대한민국]"의 형식대로 답해야해.'''
      
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
