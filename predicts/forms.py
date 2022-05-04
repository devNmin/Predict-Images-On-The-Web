from django import forms
from .models import Predict, Comment

class PredictForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'maxlength': 10,
                'placeholder': '제목을 작성해주세요.',
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': '내용을 작성해주세요.',
            }
        )
    )
    poster_url = forms.ImageField(
        label='포스터',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    class Meta:
        model = Predict
        exclude = ('user','like_users','predict_name',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='댓글',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '댓글을 작성해주세요.',
                'maxlength': 100,
            }
        )
    )
    class Meta:
        model = Comment
        fields = ('content',)