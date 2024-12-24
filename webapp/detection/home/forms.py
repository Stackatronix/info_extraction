from django import forms

class MyFileForm(forms.Form):    
    # file=forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control', 
            # 'multiple': True
        }),
        required=True
    )