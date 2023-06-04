from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from convert import Convert
from create import CreateExam
import os
from dotenv import load_dotenv
import warnings
import time
warnings.filterwarnings("ignore")

app = FastAPI()

load_dotenv()
OPEN_AI_KEY = os.environ.get("PRIVATE_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(pdf: UploadFile = File(...)):
    key = OPEN_AI_KEY
    contents = await pdf.read()
    filename = pdf.filename
    cnt = 5
    try:
        # 파일의 저장 경로와 이름 결정
        file_path = os.path.join(filename)

        # 파일을 기록합니다.
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        print("error")
    ce = CreateExam(key)
    con = Convert(filename, cnt)
    
    qst_list = []
    ans_list = []

    ############ 버전 1 ############
    # i = 0

    # while i < cnt:
            
    #   # GPT한테 질문할 내용 만들기
    #   txt = con.getGPTInput()
    #   input_cmd = f'''
    #   내가 말하는 거에 대해서 시험문제를 만들어줘."대한민국의 수도는 어디인가요? [서울]"처럼 답변은 대괄호안에 넣어서 알려줘.
    #   "{txt}"의 내용에서 짧은 단답식 문제 1개 만들어줘.
    #   '''

    #   # GPT한테 질문 쏘기
    #   ans = ce.sendMessage(input_cmd)
    #   # 답변 정제
    #   filtered_qst, filtered_ans = ce.filter(ans)

    #   if filtered_qst is False:
    #         print("답변 형식 오류로 인한 재생성")
    #         continue

    #   qst_list.append(f'{i+1}번. ' + filtered_qst)
    #   ans_list.append(f'{i+1}번. ' + filtered_ans + f' / {con.page} ~ {con.page+1}페이지')

    #   i += 1
            

    ############ 버전 2 ############
    txt_list = ''
    for i in range(cnt):
        txt = con.getGPTInput()
        txt_list += txt
        
    input_cmd = f'''"Sentence"를 가지고 단답형 문제 5개와 그에 따른 각각의 답을 만들어줘. 또한 아래의 지시사항을 따라야해.

    1. 모든 문제는 주어진 "Sentence" 와 관련되어야 한다.
    2. 답변 형식은 항상 문제와 답을 ":" 로 구분해야한다. 즉, "문제 : 답 : " 형식이어야 한다. 아래의 두 예시를 참고하면 된다.
    <예시 1>
    문제 1 : 대한민국의 수도는?
    답 : 서울
    <예시 2>
    문제 2 : 1+1은?
    답 : 2
    3. 문제를 생성할 "Sentence"는 아래와 같다.
    Sentence : "{txt_list}"
    4. 한글로 작성해야한다.

    '''
    input_bantanggo = f'''내가 아래에 <내용>이라고 적은 뒷부분의 내용으로 단답형 문제 5개와 그에 따른 각각의 답을 만들어줘. 또한 아래의 지시사항을 따라야해.

    - 답변 형식은 항상 문제와 답을 ":" 로 구분해야한다. 즉, "문제 : 답 : " 형식이어야 한다. 아래의 두 예시를 참고하면 된다.
    <예시 1>
    문제 1 : 대한민국의 수도는?
    답 : 서울
    <예시 2>
    문제 2 : 1+1은?
    답 : 2
    - 한글로 작성해야한다.

    <내용>
    "{txt_list}"
    '''

    # GPT한테 질문 쏘기
    import time
    st = time.time()
    ans = ce.sendMessage(input_cmd)

    # 답변에 Sentence 있으면 반창고 질문으로 재질문
    if ans.find('Sentence') != -1:
        ans = ce.sendMessage(input_bantanggo)
        
    et = time.time()
    tt = et - st
    print(f'걸린 시간 : {tt}')

        
    # 답변 정제
    filtered_qst_list, filtered_ans_list = ce.filter2(ans)

    # 필터링 오류 시 한번만 다시 질문 더 해보기
    if filtered_qst_list is False:
        ans = ce.sendMessage(input_bantanggo)
        filtered_qst_list, filtered_ans_list = ce.filter2(ans)
        
    for i in range(len(filtered_qst_list)):
        qst_list.append(f'{i+1}번. ' + filtered_qst_list[i])
    for i in range(len(filtered_ans_list)):
        ans_list.append(f'{i+1}번. ' + filtered_ans_list[i])


    for q, a in zip(qst_list, ans_list):
        print(f'생성 문제 {q}')
        print(f'생성 답안 {a}')

    con.txt2pdf(qst_list, ans_list)
    return FileResponse("output.pdf", filename="output.pdf")
    