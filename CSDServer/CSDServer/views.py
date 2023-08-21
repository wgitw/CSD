from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import requests
import traceback
import os
from pydub import AudioSegment


@csrf_exempt
def process_audio(request):
    print("process_audio")

    try:
        if request.method == 'POST':
            print("POST")
            # POST 요청에서 이미지 파일을 가져옵니다.
            m4a_file = request.FILES['m4a']

            # 소리 + 묵음
            # load the audio files
            audio1 = AudioSegment.from_file(m4a_file, format="m4a")
            audio2 = AudioSegment.from_file("slient.m4a", format="m4a")

            # concatenate the audio files
            combined_audio = audio1 + audio2

            # export the concatenated audio as a new file
            file_handle = combined_audio.export("combined.wav", format="wav")
            
            # 성공적으로 파일을 받았을 때 200 OK 응답을 반환합니다.
            return HttpResponse(status=200)

    except Exception as e:
        print(traceback.format_exc())  # 예외 발생시 traceback 메시지 출력
        return HttpResponseServerError()  # 500 Internal
