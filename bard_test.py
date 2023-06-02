import bardapi
import os
from convert import Convert
from create import CreateExam

key = 'WQjTY3VdBwsaRDd9fxFCNZzMbGKnbi3Eca4gGUBsppK_XfoOvWcNrF6FT5v2SCW1XGHAxQ.'
os.environ['_BARD_API_KEY'] = key

file = '7.Discriminant analysis.pdf'
cnt = 10
con = Convert(file, cnt)
txt = con.getGPTInput()
input_cmd = f'''
내가 말하는 거에 대해서 시험문제를 만들어줘."대한민국의 수도는 어디인가요? [서울]"처럼 답변은 대괄호안에 넣어서 알려줘.
"{txt}"의 내용에서 짧은 단답식 문제 1개 만들어줘. 한국어로 답해줘.
'''
import time
st = time.time()
res = bardapi.core.Bard().get_answer(input_cmd)
et = time.time()
print(et - st)
print(res['content'])