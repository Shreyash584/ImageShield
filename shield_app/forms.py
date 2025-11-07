from django import forms

class EncryptForm(forms.Form):
    image = forms.ImageField(required=True)

class DecryptForm(forms.Form):
    encrypted_file = forms.FileField(required=True)
    key = forms.CharField(
        required=True, min_length=16, max_length=16,
        help_text="Enter the exact 16-character AES key used to encrypt."
    )
