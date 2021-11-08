from django.core import paginator
from django.forms.widgets import PasswordInput
from django.http import Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .models import Board
from fcuser.models import Fcuser
from .forms import BoardForm
# Create your views here.


def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)  # 함수 인자로 전달받은 pk값을 pk로 설정
    except Board.DoesNotExist:
        raise Http404('해당 게시물을 찾을 수 없습니다.')

    return render(request, 'board_detail.html', {"board": board})


def board_write(request):
    if not request.session.get('user'):
        return redirect('/fcuser/login')

    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user')
            board = Board()
            fcuser = Fcuser.objects.get(pk=user_id)
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = fcuser
            board.save()
            # writer는 기본적으로 Fcuser의 데이터베이스에서
            # 가져와야 하므로 session을 통해 가져오자.
            return redirect('/board/list')
    else:
        form = BoardForm()

    return render(request, "board_write.html", {"form": form})


def board_list(request):
    # 변수명을 all_boards(query set)로 일단 바꾸고 기존의 boards는 다른 변수로
    all_boards = Board.objects.all().order_by('-id')
    page = int(request.GET.get("p", 1))  # page번호를 p라는 값으로 받고 없으면 첫번째 페이지
    paginator = Paginator(all_boards, 2)  # 한 화면에 2개씩 나오게

    boards = paginator.get_page(page)
    return render(request, 'board_list.html', {'boards': boards})
