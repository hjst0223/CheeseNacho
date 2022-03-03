from django import forms
from entmt_info.models import Movies, Series


class MoviesDetailForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = '__all__'

        labels = {
            'mc_movie': '작성한 영화 제목',
            'mc_star': '별점',
            'mc_member': '댓글 작성자',
            'mc_content': '댓글 내용',
            'mc_date': '댓글 작성 시간'
        }

        widgets = {
            'mc_movie': forms.TextInput(
                attrs={
                    'class': 'form-control w-50'
                }
            ),
            'mc_star': forms.TextInput(
                attrs={
                    'class': 'form-control w-15'
                }
            ),
            'mc_member': forms.TextInput(
                attrs={
                    'class': 'form-control w-25'
                }
            ),
            'mc_content': forms.TextInput(
                attrs={
                    'class': 'form-control w-75'
                }
            ),
            'mc_date': forms.TextInput(
                attrs={
                    'class': 'form-control w-25'
                }
            )
        }


class SeriesDetailForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = '__all__'

        labels = {
            'sc_movie': '작성한 영화 제목',
            'sc_star': '별점',
            'sc_member': '댓글 작성자',
            'sc_content': '댓글 내용',
            'sc_date': '댓글 작성 시간'
        }

        widgets = {
            'sc_movie': forms.TextInput(
                attrs={
                    'class': 'form-control w-50'
                }
            ),
            'sc_star': forms.TextInput(
                attrs={
                    'class': 'form-control w-15'
                }
            ),
            'sc_member': forms.TextInput(
                attrs={
                    'class': 'form-control w-25'
                }
            ),
            'sc_content': forms.TextInput(
                attrs={
                    'class': 'form-control w-75'
                }
            ),
            'sc_date': forms.TextInput(
                attrs={
                    'class': 'form-control w-25'
                }
            )
        }

