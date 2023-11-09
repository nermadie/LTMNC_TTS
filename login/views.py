from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, decorators, logout


# Create your views here.
class LoginClass(View):
    def get(self, request):
        return render(request, "login/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        my_user = authenticate(username=username, password=password)
        if my_user is None:
            return HttpResponse("Invalid Login")
        login(request, my_user)
        return redirect("homepage:text")


class RegisterClass(View):
    def get(self, request):
        return render(request, "login/register.html")

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]

        # Kiểm tra xem username hoặc email đã tồn tại trong cơ sở dữ liệu
        if (
            User.objects.filter(username=username).exists()
            or User.objects.filter(email=email).exists()
        ):
            messages.error(request, "Username hoặc email đã tồn tại.")
            return redirect("login:register")
        elif password == confirm_password:
            # Tạo người dùng mới
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()
            messages.success(request, "Đăng ký thành công! Đăng nhập ngay.")
            return redirect("login:login")
        else:
            messages.error(request, "Mật khẩu và mật khẩu xác nhận không khớp.")
            return redirect("login:register")


def logout_view(request):
    logout(request)
    return redirect("login:login")
