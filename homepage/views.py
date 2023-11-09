import concurrent.futures
import os
import time
from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from ai_handler.vietTTS.synthesizer import synthesize_text
from homepage.models import ProcessedFile

pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)


def process_file(uploaded_file, user_id, upload_time):
    try:
        upload_time_namefile = upload_time.strftime("%Y-%m-%d_%H-%M-%S")
        folder_path = os.path.join("data", "input", str(user_id))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        filename = os.path.join(folder_path, f"{upload_time_namefile}.txt")
        uploaded_file_data = uploaded_file.read()
        text = uploaded_file_data.decode("utf-8")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
        folder_path = os.path.join("input", str(user_id))
        filename = os.path.join(folder_path, f"{upload_time_namefile}.txt")
        output_folder = os.path.join("output", str(user_id))
        output_filename = os.path.join(output_folder, f"{upload_time_namefile}.wav")
        processed_file = ProcessedFile(
            user=User.objects.get(id=user_id),
            upload_time=upload_time,
            status=False,
            input_file_path=filename,
            wav_file_path=output_filename,
        )
        processed_file.save()
        output_folder = os.path.join("data", "output", str(user_id))
        output_filename = os.path.join(output_folder, f"{upload_time_namefile}.wav")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        synthesize_text(text=text, output_path=output_filename)
        processed_file.status = True
        processed_file.save()
    except Exception as e:
        print(e)


def process_text(input_text, user_id, upload_time):
    try:
        upload_time_namefile = upload_time.strftime("%Y-%m-%d_%H-%M-%S")
        folder_path = os.path.join("data", "input", str(user_id))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        filename = os.path.join(folder_path, f"{upload_time_namefile}.txt")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(input_text)
        folder_path = os.path.join("input", str(user_id))
        filename = os.path.join(folder_path, f"{upload_time_namefile}.txt")
        output_folder = os.path.join("output", str(user_id))
        output_filename = os.path.join(output_folder, f"{upload_time_namefile}.wav")
        processed_file = ProcessedFile(
            user=User.objects.get(id=user_id),
            upload_time=upload_time,
            status=False,
            input_file_path=filename,
            wav_file_path=output_filename,
        )
        processed_file.save()
        output_folder = os.path.join("data", "output", str(user_id))
        output_filename = os.path.join(output_folder, f"{upload_time_namefile}.wav")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        synthesize_text(text=input_text, output_path=output_filename)
        processed_file.status = True
        processed_file.save()
    except Exception as e:
        print(e)


# Create your views here.
class TextClass(View):
    def get(self, request):
        name = request.user.username
        return render(request, "homepage/text.html", {"name": name})

    def post(self, request):
        text = request.POST["text"]
        user_id = request.user.id
        upload_time = datetime.now()
        pool.submit(process_text, text, user_id, upload_time)
        return redirect("homepage:processing", user_id, upload_time)


class FileClass(View):
    def get(self, request):
        name = request.user.username
        return render(
            request,
            "homepage/file.html",
            {"name": name},
        )

    def post(self, request):
        if request.FILES["file"]:
            uploaded_file = request.FILES["file"]
            user_id = request.user.id  # Lấy user_id của người dùng
            upload_time = datetime.now()
            pool.submit(process_file, uploaded_file, user_id, upload_time)
            return redirect("homepage:processing", user_id, upload_time)
        else:
            return HttpResponse("Bạn chưa chọn file nào.")


class ProcessingClass(View):
    def get(self, request, user_id, upload_time):
        name = request.user.username
        return render(
            request,
            "homepage/processing.html",
            {"user_id": user_id, "upload_time": upload_time, "name": name},
        )


def is_processed(request, user_id, upload_time):
    if request.method == "GET":
        try:
            processed_file = ProcessedFile.objects.get(
                user_id=user_id, upload_time=upload_time
            )
            if not processed_file.status:
                response_data = {"status": False}
            else:
                response_data = {
                    "status": True,
                    "wav_file_path": processed_file.wav_file_path,
                }

            return JsonResponse(response_data)
        except ProcessedFile.DoesNotExist:
            return JsonResponse({"error": "Tệp xử lý không tồn tại"})


def user_history(request):
    user_id = request.user.id
    name = request.user.username
    processed_files = ProcessedFile.objects.filter(user_id=user_id)
    return render(
        request,
        "homepage/user_history.html",
        {"processed_files": processed_files, "name": name},
    )
