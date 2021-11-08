from django.db import models

# Create your models here.

# 이 클래스를 테이블 형태로 만들어서 DB에 저장해야 한다.


class Fcuser(models.Model):  # 장고에서 제공하고 있는 models.Models
    # 를 상속받아야 한다.
    username = models.CharField(max_length=32,
                                verbose_name="사용자명")
    useremail = models.EmailField(max_length=128, verbose_name="사용자이메일")
    password = models.CharField(max_length=64, verbose_name="비밀번호")
    registered_dtt = models.DateTimeField(
        auto_now_add=True, verbose_name="등록시간")
    # dtt = datetime약자
    # 등록을 하자마자 자동으로 추가해준다. --> auto_now_add

    def __str__(self):
        return self.username

    # 데이터베이스의 table 이름 지정

    class Meta:
        db_table = "Fastcampus_fcuser"
        verbose_name = "패스트캠퍼스 사용자"
        verbose_name_plural = "패스트캠퍼스 사용자"
