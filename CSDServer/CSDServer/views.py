from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import requests
import traceback
import os


@csrf_exempt
def process_audio(request):
    print("process_audio")

    try:
        if request.method == 'POST':
            print("POST")
            # POST 요청에서 이미지 파일을 가져옵니다.
            m4a_file = request.FILES['m4a']

            # 성공적으로 파일을 받았을 때 200 OK 응답을 반환합니다.
            return HttpResponse(status=200)

    except Exception as e:
        print(traceback.format_exc())  # 예외 발생시 traceback 메시지 출력
        return HttpResponseServerError()  # 500 Internal
