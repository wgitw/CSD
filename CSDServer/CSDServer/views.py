from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import requests
import traceback
import os
from pydub import AudioSegment
import librosa, librosa.display


# m4a -> wav -> spectrogram
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

            # paths.append(file_path)
            sig, sr = librosa.load(file_handle, sr=22050)

            # 에너지 평균 구하기
            sum = 0
            for i in range(0, sig.shape[0]):
                sum += sig[i] ** 2
            mean = sum / sig.shape[0]

            # 피크인덱스 찾기
            for i in range(0, sig.shape[0]):
                if (sig[i] ** 2 >= mean):
                    peekIndex = i
                    break

            START_LEN = 1102
            END_LEN = 20948
            if peekIndex > 1102:
                print(peekIndex)
                startPoint = peekIndex - START_LEN
                endPoint = peekIndex + 22050
            else:
                print(peekIndex)
                startPoint = peekIndex
                endPoint = peekIndex + END_LEN



            # 성공적으로 파일을 받았을 때 200 OK 응답을 반환합니다.
            return HttpResponse(status=200)

    except Exception as e:
        print(traceback.format_exc())  # 예외 발생시 traceback 메시지 출력
        return HttpResponseServerError()  # 500 Internal
