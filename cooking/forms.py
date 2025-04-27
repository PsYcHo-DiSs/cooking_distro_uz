from django import forms
from .models import Post


class PostAddForm(forms.ModelForm):
    """Форма для добавления новой статьи от пользователя"""

    class Meta:
        """Мета класс, указывающий поведенческий характер, чертёж для класса"""
        model = Post
        fields = ['title', 'content', 'photo', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
