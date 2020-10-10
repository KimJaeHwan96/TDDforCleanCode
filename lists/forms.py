from django import forms
from .models import Item

EMPTY_LIST_ERROR = "빈 아이템을 등록할 수 없습니다"

# 모델 폼
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': '작업 아이템 입력',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }
    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

"""
일반 폼
class ItemForm(forms.Form):
    item_text = forms.CharField(
        widget=forms.fields.TextInput(attrs={
            'placeholder': '작업 아이템 입력',
            'class': 'form-control input-lg',
        })
    )
"""