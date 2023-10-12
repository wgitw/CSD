## 🔥 Title
CSDServer

<br><br>
## :raised_hands: Introduction
**[ENG]**
CSD Server receives the sound as a request and converts it into a spectrogram image to run the model and output the result value.

<br>

**[KOR]**
소리를 요청으로 받고 스펙트로그램 이미지로 변환해 모델을 돌리고 결과값을 출력해주는 CSDServer 입니다. 

<br><br>

## 💪 Major Function
**[ENG]**
Take byte Array from the client, convert it to an ac file, and convert it to a wav file.
Use the liborasa library to convert the wave file into a spectrogram image in the form of a time-frequency graph.
Apply the converted image to the CSD-Model to extract the alphabetic result value and send a POST response to the client.

<br>

**[KOR]**
client로부터 byteArray를 받아 이를 acc 파일로 변환을 한뒤 wav 파일로 변환을 합니다. 
wav 파일을 liborasa 라이브러리를 사용하여 시간-주파수 그래프 형태의 스펙트로그램 이미지로 변환합니다. 
변환된 이미지를 CSD-Model에 적용시켜 알파벳 결과값을 추출하여 client에게 POST 응답을 보냅니다.

<br><br>

## ⭐️ Install and Run

1. clone [github 리포지토리 주소]
2. 가상환경 생성
    1. python -m venv venv 또는 python3 -m venv venv
3. 가상환경 실행
    1. Windows
        1. venv\Scripts\activate
    2. macOS 및 Linux
        1. source venv/bin/activate
4. 패키지 설치
    1. pip install -r requirements.txt
    2. pip3 install -r requirements.txt
4-1. 패키지 설치2
    1. pip install matplotlib torch pydub
    2. pip3 install matplotlib torch pydub
5. cd CSDServer
6. migration
    1. python manage.py makemigrations
    2. python manage.py migrate
    
    또는
    
    1. python manage.py makemigrations
    2. python manage.py migrate
7. 로컬 실행
    1. python manage.py runserver 또는 python3 manage.py runserver

<br><br>

## 👏 API ENDPOINT

process_audio

: byteArray 받아서 모델돌리고 숫자 예측값 변환

- URL
    
    /process_audio/
    
- Method
    
    `POST`
    

- URL Params
    
    None
    
- Data Params
    
    
    | key | value |
    | --- | --- |
    | ‘recordData’ | byteArray |
    |  |  |
    
- Success Response:
    
    code : 200
    
    content : 
    
    ```json
    [
    	{
    		"predicted_alphabet": String,
    	}
    ]
    ```
    
<br><br>

## 🔗 Project Structure
  ```bash
Back-Server
├── CSDServer
│   ├── CSDServer
│   │   ├── init.py
│   │   ├── asgi.py
│   │   ├── resnetModel
│   │   │   └── resnet34.pth
│   │   ├── base.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── wsgi.py
│   ├── combined.wav
│   ├── manage.py
│   ├── silent.wav
│   └── static
│       └── images
│           └── test.jpg
├── README.md
└── base.txt

```
