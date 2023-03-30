from django import forms
from bbsnote.models import Board, Comment

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['subject','content']
        # widgets={
        #     'subject' : forms.TextInput(attrs={'class':'form-control'}), # forms의 TextInput에 attribute를 추가시킬게
        #     'content' : forms.Textarea(attrs ={'class':'form-control', 'rows':10})
        # }
        # labels={
        #     'subject' : '제목',
        #     'content' : '내용',
        # }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']
        labels={
            'content' : '댓글내용'

        }
