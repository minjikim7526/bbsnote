from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm


# Create your views here.
def signup(request):
    # 요청이 POST인 경우
    if request.method=='POST':
        form = UserForm(request.POST) # form에는 UserForm 받아서 request정보를 넘겨주겠다
        if form.is_valid():
            form.save() # form안에 들어가있는 데이터를 저장하겠다. commit=True가 디폴트
            username=form.cleaned_data.get('username') # username에는 form에 있는 것을 cleaned_data로 가져와라
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) # 가입 후 자동로그인 가능하도록
            login(request, user)
            return redirect('index')
    # 요청이 GET인 경우
    else:
        form=UserForm()
    return render(request, 'common/signup.html', {'form':form})