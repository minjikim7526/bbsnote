from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Board, Comment
from django.utils import timezone
from .forms import BoardForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def index(request):
    # 입력인자 추가
    # 페이지정보 값이 따라다님
    # 요청된 정보로부터 GET방식으로 넘어오는 데이터중에 page라는 값을 가져오고, 없으면 1로 초기화(주소에 page값 입력하지 않으면 1페이지를 기본으로 보여줘라)
    page = request.GET.get('page',1)
    # 조회
    board_list = Board.objects.order_by('-create_date')
    # 페이징처리
    # paginator라는 변수에 boad_list에 있는 데이터를 5개씩 쪼개 담는다(한 page에 글 5개씩 보여주기 위함)
    paginator = Paginator(board_list, 5)
    # 위에서 정의한 page변수를 넘겨받아서 그 page에 해당하는 정보를 page_obj에 저장하고 board_list로 넘겨준다
    page_obj=paginator.get_page(page)
    context={'board_list' : page_obj} # 사전형

    # return HttpResponse("bbsnote에 오신 것을 환영합니다")
    return render(request, 'bbsnote/board_list.html', context)

def detail(request, board_id): # 주소에서 board_id 넘겨받음
    board = Board.objects.get(id=board_id) # board_id=5일때의 데이터 묶음이 board에 할당됨(id, subject, comment,...)
    context = {'board':board}
    return render(request, 'bbsnote/board_detail.html', context)

@login_required(login_url='common:login')
def comment_create(request, board_id):
    if request.method =='POST':
        board = Board.objects.get(id=board_id)
        # comment = Comment(board=board, content=request.POST.get('content'), create_date=timezone.now())
        # comment.save()

        # Board와 Comment가 foreignKey로 연결되어있는 종속관계의 경우에는 위의 두 문장을 이렇게 한 줄로 쓸 수도 있다
        board.comment_set.create(content=request.POST.get('content'),create_date=timezone.now(), author=request.user)
    return redirect('bbsnote:detail', board_id=board_id)
        
    
@login_required(login_url='common:login')
def board_create(request):
    if request.method =='POST': # 요청된 정보가 POST로 왔으면 BoardForm이라는 클래스를 참조해서 요청된 정보롤 form이라는 변수에 담아라
        form = BoardForm(request.POST)
        if form.is_valid(): # 만약에 그 폼의 값이 있으면 그 값을 board에 저장하되, commit은 하지마라(mysql은 오토커밋이니까 오토커밋하지말라는 뜻)
            board = form.save(commit=False)
            board.author=request.user
            # board.create_date = timezone.now() #models.py에 자동으로 시간 저장되도록 이미 설정해두었기 때문에 없어도 되는 부분!
            board.save()  # create_date에 시간 할당하고나서 save해라(커밋해라)
            return redirect('bbsnote:index')#  저장까지 다 했으면 bbsnote의 index로 가라
    else: # POST로 요청이 오지 않았으면
        form = BoardForm()
    return render(request, 'bbsnote/board_form.html', {'form':form}) # 'form'이라는 키를 가진 애한테 form의 정보를 넘겨줘라


@login_required(login_url='common:login')
def board_modify(request, board_id):
    board = get_object_or_404(Board, pk=board_id) # 오류가 나면 오류 대신 404가 나오도록 처리
    if request.user != board.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('bbsnote:detail', board_id=board.id)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user
            board.save()
            return redirect('bbsnote:detail', board_id=board.id)
    else:
        form=BoardForm(instance=board)
    context={'form' : form}
    return render(request, 'bbsnote/board_form.html', context)

@login_required(login_url='common:login')
def board_delete(request, board_id):
    board=get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('bbsnote:detail', board_id=board.id)
    board.delete()
    return redirect('bbsnote:index')

@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    # 작성자가 아닌 경우 예외처리
    if request.user != comment.author:
        messages.error(request, "수정 권한이 없습니다!")
        # bbsnote의 detail에 board_id를 넘겨주는데, board_id가 현재 comment가 종속된 board의 id인 곳으로 가라
        return redirect('bbsnote:detail', board_id=comment.board.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author=request.user
            comment.save()
            return redirect('bbsnote:detail', board_id=comment.board.id)
    else:
        form = CommentForm(instance=comment)
    context={'comment':comment, 'form':form}
    return render(request, 'bbsnote/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "삭제 권한이 없습니다!")
        return redirect('bbsnote:detail', board_id=comment.board.id)
    comment.delete()
    return redirect('bbsnote:detail', board_id=comment.board.id)