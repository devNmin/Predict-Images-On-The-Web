from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Predict, Comment
from django.http import JsonResponse
from .forms import  CommentForm, PredictForm
from .predict import predict_file
# Create your views here.


@require_safe
def index(request):
    predicts = Predict.objects.order_by('-pk')
    context = {
        'predicts': predicts,
    }
    return render(request, 'predicts/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = PredictForm(request.POST,request.FILES)
        print("**************")
        path = f"./media/images/{request.FILES['poster_url']}"
        values = predict_file(path)
        # print(values)
        # form.predict_name = values
        print("**************")
        if form.is_valid():
            predict = form.save(commit=False)
            predict.user = request.user
            predict.predict_name=values
            predict.save()
            print("asdasdasdasd",predict.predict_name)
            return redirect('predicts:detail', predict.pk)
    else:
        form = PredictForm()
    context = {
        'form': form,
    }
    return render(request, 'predicts/create.html', context)



@require_safe
def detail(request, pk):
    predict = get_object_or_404(Predict, pk=pk)
    comment_form = CommentForm()
    comments = predict.comment_set.all()



    context = {
        'predict': predict,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'predicts/detail.html', context)


@require_POST
def delete(request, pk):
    predict = get_object_or_404(Predict, pk=pk)
    if request.user.is_authenticated:
        if request.user == predict.user:
            predict.delete()
    return redirect('predicts:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    predict = get_object_or_404(Predict, pk=pk)
    if request.user == predict.user:
        if request.method == 'POST':
            form = PredictForm(request.POST, request.FILES, instance=predict)
            if form.is_valid():
                predict = form.save()
                return redirect('predicts:detail', predict.pk)
        else:
            form = PredictForm(instance=predict)
    else:
        return redirect('predicts:index')
    context = {
        'predict': predict,
        'form': form,
    }
    return render(request, 'predicts/update.html', context)


@require_POST
def comment_create(request, pk):
    if request.user.is_authenticated:
        predict = get_object_or_404(Predict, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.predict = predict
            comment.user = request.user
            comment.save()
        return redirect('predicts:detail', predict.pk)
    return redirect('accounts:login')


@require_POST
def comment_delete(request, predict_pk ,comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('predicts:detail', predict_pk)

@require_POST
def likes(request, predict_pk):
    predict = get_object_or_404(Predict, pk=predict_pk)

    # 게시물 좋아요 누른 사람들 목록 => 있으면
    if predict.like_users.filter(pk=request.user.pk).exists():
        # 목록에서 빼겠다
        predict.like_users.remove(request.user)
        # 현재 상태
        liked = False
    else:
        # 없으면 목록에 추가하겠다
        predict.like_users.add(request.user)
        # 현재 상태
        liked = True

    context = {
        'liked': liked,
        'count': predict.like_users.count()
    }
    # JSON을 반환
    return JsonResponse(context)