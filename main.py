from convert import Convert
from create import CreateExam

key = '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'
file = '서고강.pdf'
ce = CreateExam(key)

con = Convert(file)
text = con.pdf2txt()

length = int(len(text))
devided_txt = text[0:length]
print(devided_txt)
input_cmd = f'{devided_txt}의 내용에서 단답형 문제 10개랑 답까지 만들어줘'

ans = ce.sendMessage(input_cmd)
print(ans)
filtered_qst, filtered_ans = ce.filter(ans)
print(f'''
      생성된 문제: {filtered_qst},
      생성된 답안: {filtered_ans}
      ''')

con.txt2pdf(filtered_qst, filtered_ans)
