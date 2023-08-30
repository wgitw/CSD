import subprocess
import traceback

import librosa
import librosa.display
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import struct
import json

import torch
from PIL import Image
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from matplotlib import image, transforms
from pydub import AudioSegment
from io import BytesIO


FIG_SIZE = (15, 10)
DATA_NUM = 30

matplotlib.use('Agg')

alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']
# 음성 데이터의 샘플링 레이트, 채널 수, 샘플링 포맷 등을 정의합니다.
SAMPLE_RATE = 44100
CHANNELS = 1
SAMPLE_WIDTH = 2

# byteArray -> acc -> wav -> spectrogram / -> resnetModel -> result
@csrf_exempt
def process_audio(request):
    print("process_audio")

    try:
        if request.method == 'POST':
            print("POST")
            # POST 요청에서 이미지 파일을 가져옵니다.
            # m4a_file = request.FILES['m4a']

            # POST 요청에서 byteArray 데이터를 가져옵니다.
            requestBody = json.loads(request.body)  # 안드로이드 앱에서 보낸 데이터를 가져옵니다.
            byte_data = requestBody['recordData']
            byte_array = bytes([struct.pack('b', x)[0] for x in byte_data])

            with open('my_audio_file.aac', 'wb+') as destination:
                for i in range(0, len(byte_array), 32):
                    chunk = byte_array[i:i + 32]
                    destination.write(chunk)


            # 소리 + 묵음
            # aac -> wav
            input_file = "my_audio_file.aac"
            output_file = "my_audio_file.wav"
            # Run the ffmpeg command to convert the AAC file to WAV
            subprocess.run(["ffmpeg", "-y", "-i", input_file, output_file])


            # load the audio files
            audio1 = AudioSegment.from_file("my_audio_file.wav", format="wav")
            audio2 = AudioSegment.from_file("silent.wav", format="wav")

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

            # 단순 푸리에 변환 -> Specturm
            fft = np.fft.fft(sig[startPoint:endPoint])
            # 복소공간 값 절댓갑 취해서, magnitude 구하기
            magnitude = np.abs(fft)
            # Frequency 값 만들기
            f = np.linspace(0, sr, len(magnitude))
            # 푸리에 변환을 통과한 specturm은 대칭구조로 나와서 high frequency 부분 절반을 날려고 앞쪽 절반만 사용한다.
            left_spectrum = magnitude[:int(len(magnitude) / 2)]
            left_f = f[:int(len(magnitude) / 2)]
            # STFT -> Spectrogram
            hop_length = 512  # 전체 frame 수
            n_fft = 2048  # frame 하나당 sample 수
            # calculate duration hop length and window in seconds
            hop_length_duration = float(hop_length) / sr
            n_fft_duration = float(n_fft) / sr

            # STFT
            stft = librosa.stft(sig[startPoint:endPoint], n_fft=n_fft, hop_length=hop_length)
            # 복소공간 값 절댓값 취하기
            magnitude = np.abs(stft)
            # magnitude > Decibels
            log_spectrogram = librosa.amplitude_to_db(magnitude)
            FIG_SIZE = (10, 10)
            # display spectrogram
            plt.figure(figsize=FIG_SIZE)
            librosa.display.specshow(log_spectrogram, sr=sr, hop_length=hop_length, cmap='magma')

            # matplotlib 라이브러리를 사용하여 생성된 spectrogram 이미지를 jpg 형식으로 저장
            image_path = 'static/images/' + 'test.jpg'

            # save spectrogram image
            # plt.savefig('static/images/' + file_handle[:name_end_pos] + '.jpg')
            # spectrogram 이미지 저장
            plt.savefig(image_path)

            plt.close()

            # 모델 입히기
            model = torch.load('djangoServer/resnetModel/resnet32.pth')
            # switch resnetModel to evaluation mode
            model.eval()
            # define the image transforms
            image_transforms = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])

            # 이미지 열기
            image = Image.open(image_path)
            # apply the transforms to the test image
            test_image_tensor = image_transforms(image)
            # add batch dimension to the image tensor
            test_image_tensor = test_image_tensor.unsqueeze(0)

            # get the resnetModel's prediction
            with torch.no_grad():
                prediction = model(test_image_tensor)

            # get the predicted class index
            predicted_class_index = torch.argmax(prediction).item()

            response = {'predicted_alphabet': alpha[predicted_class_index]}
            # 예측값 알파벳 출력
            print("post: ", response)
            return JsonResponse(response)


    except Exception as e:
        print(traceback.format_exc())  # 예외 발생시 traceback 메시지 출력
        return HttpResponseServerError()  # 500 Internal
