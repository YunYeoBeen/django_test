from types import CellType
from django import forms
from .models import Fcuser
from django.contrib.auth.hashers import check_password


class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages={
            'required': "아이디를 입력해주세요",
        }, max_length=32, label="사용자 이름")
    password = forms.CharField(
        error_messages={
            'required': "비밀번호를 입력해주세요",
        },
        widget=forms.PasswordInput, label="비밀번호")

    def clean(self):
        cleaned_data = super().clean()  # 내가 입력한 값들이 cleaned_data에 들어간다.
        # username에 적었던 데이터는 username이라는 변수에
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:  # 각 값이 들어있을 때
            try:  # 이제 예외처리
                fcuser = Fcuser.objects.get(username=username)
            # session처리를 따로 하지 않을거기때문에 not을 붙여준다.
            except Fcuser.DoesNotExist:
                self.add_error('username","해당 아이디가 없습니다.')
                return
            if not check_password(password, fcuser.password):
                self.add_error('password', "비밀번호를 틀렸습니다.")
            else:  # 맞을 시
                self.user_id = fcuser.id
