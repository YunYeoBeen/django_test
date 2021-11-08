from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import Fcuser
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .forms import LoginForm
# Create your views here.


def home(request):
    user_id = request.session.get('user')
    if user_id:  # session에서 user의 정보를 가져온다. 만약 있다면?
        fcuser = Fcuser.objects.get(pk=user_id)  # pk는 기본키 즉 user_id를 기본으로
    #     return HttpResponse(fcuser.username)  # 로그인이 되었다면 유저 이름을 출력하는 방식
    # return HttpResponse('Home!')  # 로그인이 안됐다면 home! 텍스트만 출력
    return render(request, "home.html")


def logout(request):
    if request.session.get('user'):  # user의 정보가 있다면
        del(request.session['user'])  # 로그아웃
    return redirect('/')


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
    # if request.method == "GET":
    #     return render(request, "login.html")
    # elif request.method == "POST":
    #     username = request.POST.get("username", None)
    #     password = request.POST.get("password", None)
    #     res_data = {}
    #     if not(username):
    #         res_data["error"] = "아이디를 입력하세요"
    #     elif not(password):
    #         res_data["error"] = "비밀번호를 입력하세요"
    #     else:
    #         # 자 우리가 register에서는 Fcuser라는 fc_community의 models에 저장되어있는
    #         # 클래스를 이용했다. 이제 그 register안에 있는 정보를 로그인에 써야하니 Fcuser를
    #         # 가져온다. Fcuser 안에 username를 이용하여 일치하는지 불일치하는지를 파악

    #         # objects 안에 get이라는 함수가 있는데
    #         fcuser = Fcuser.objects.get(username=username)
    #         # 조건은 username이 username인가?
    #         # 앞의 username은 register, 뒤에는 login username
    #         if check_password(password, fcuser.password):  # 새로운 모듈인 check_password 선언
    #             # login의 password가 fcuser.password와 일치하는지
    #             # 이제 로그인 됐을 시 홈화면으로 가는 redirect를 추가
    #             # return redirect('http://naver.com') --> 이런 식으로 naver화면으로 이동
    #             request.session['user'] = fcuser.id  # session을 딕셔너리 형태로!!
    #             # # 방금 로그인한 fcuser.id를 session의 value값으로 저장

    #             return redirect('/')  # '/' 만 입력해도 현재 제작하는 홈페이지로 이동

    #         else:
    #             res_data["error"] = "비밀번호를 틀렸습니다."
    # return render(request, 'login.html', res_data)


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        # get함수를 사용해줘서 기본값을 None으로 지정
        username = request.POST.get("username", None)
        # 즉 비밀번호 확인칸을 작성하지 않으면 None값이 기본으로 지정
        # 따라서 None이 오게 되면 밑에 if not() 부분에서 걸리게 된다. 따라서 모든 것을 작성해줘야 한다.
        password = request.POST.get("password", None)
        re_password = request.POST.get("re-password", None)
        useremail = request.POST.get("useremail", None)
        # 원래는 re_password=request.POST["re-password"] 주의! ()가 아닌 []다
        # 장고관련.txt의 9월 3일 자 12번 때문에 ()로 바꿔준다.

        res_data = {}  # 이전까지는 그냥 비밀번호가 다릅니다 라고 웹페이지 왼쪽 상단에 나타나서 볼품없었다.
        # 하지만 딕셔너리 변수를 만들어 준 후 error일 시 비밀번호가 다릅니다 라는 원소를 추가
        # 그리고 (else)같을 시에는 회원가입이 되는 로직으로 구성
        # 마지막에 render(request, "register.html",res_data) res_data를 랜더링(html코드로 전달)할 수 있다.
        # html코드를 변경시켜줘야 한다. --> html로 고고

        if not(username and password and re_password and useremail):  # 모든 값을 작성해주지 않았다면 error발생
            res_data["error"] = "모든 값을 입력해야 합니다."
        elif password != re_password:
            res_data["error"] = "비밀번호가 다릅니다."
        else:
            fcuser = Fcuser(
                username=username,
                password=make_password(password),  # 암호화한 password를 저장
                useremail=useremail
            )

            fcuser.save()

        return render(request, "register.html", res_data)
    # request를 같이 전달하고 내가 반환할 html파일을 보내줘야 한다.
    # 이 html파일의 위치를 명시해줘야 한다. 지금은 fcuser안의 templates에 있으니 이렇게 표현
    # 아니면 foledr이름/folder이름/ 이렇게 해줘야 한다.

    # 회원가입 동작을 구현하기 위해서 html에서 name으로 명시해줬던 값이 전달된다.
    # fcuser class를 사용하기 위해 models 안에 있는 Fcuser사용
    # 입력받은 값으로 fcuser라는 객체가 생성되고 실제로 데이터베이스에 저장이 된다.
