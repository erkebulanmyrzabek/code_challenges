import os

from django.shortcuts import get_object_or_404

from code_challenges import settings
from .models import Challenge, Solution

def home(request):
    challenges = Challenge.objects.all()
    return render(request, 'home.html', {'challenges': challenges})

from .utils import check_solution

from .utils import generate_certificate

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались и вошли!")
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "Вы успешно вошли!")
                return redirect('home')
            else:
                messages.error(request, "Неверные данные для входа")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


from django.http import HttpResponse

def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    if request.method == 'POST':
        solution_code = request.POST.get('code')
        test_cases = challenge.tests.all()
        is_approved = check_solution(solution_code, test_cases)
        solution = Solution.objects.create(user=request.user, challenge=challenge, code=solution_code,
                                           is_approved=is_approved)

        if is_approved:
            certificate_file = generate_certificate(request.user, challenge)
            certificate_url = f"{settings.MEDIA_URL}certificates/{os.path.basename(certificate_file)}"
            return HttpResponse(f"Решение верное! <a href='{certificate_url}'>Скачать сертификат</a>")
        else:
            return HttpResponse("Решение неверное. Попробуйте снова.")
    return render(request, 'challenge_detail.html', {'challenge': challenge})
