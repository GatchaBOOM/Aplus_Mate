from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from convert import Convert
from create import CreateExam
import os
from dotenv import load_dotenv

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

    i = 0

    while i < cnt:
            
      # GPT한테 질문할 내용 만들기
      txt = con.getGPTInput()
      input_cmd = f'''
      내가 말하는 거에 대해서 시험문제를 만들어줘."대한민국의 수도는 어디인가요? [서울]"처럼 답변은 대괄호안에 넣어서 알려줘.
      "{txt}"의 내용에서 짧은 단답식 문제 1개 만들어줘.
      '''

      # GPT한테 질문 쏘기
      ans = ce.sendMessage(input_cmd)
      # 답변 정제
      filtered_qst, filtered_ans = ce.filter(ans)

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
    return FileResponse("output.pdf", filename="output.pdf")
    