from django import forms
from .models import Art, User_Info, User_Credentials, Art_Tags, Tag_List, User_Social


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'rectangle-4'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'rectangle-3'}))


class ArtForm(forms.ModelForm):   
    class Meta:
        model = Art
        fields = ['title', 'Description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control w-100', 'placeholder': 'Escribe un título'}),
            'Description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe una descripción', 'style': 'resize: none;'}),
            'image': forms.FileInput(attrs={'class': 'form-control w-100'}),
        }
    #Campos Adicionales para Art_Tags
    Tag1=forms.ModelChoiceField(Tag_List.objects.all(),label='Selecciona Etiqueta 1')
    Tag2 =forms.ModelChoiceField(Tag_List.objects.all(),label='Selecciona Etiqueta 2')
    Tag3 =forms.ModelChoiceField(Tag_List.objects.all(),label='Selecciona Etiqueta 3')

    def save(self,commit=True, user=None):
        art = super().save(commit=False)
        art.Owner_ID = user
        art.save()

        art_tags = Art_Tags.objects.create(
            Tag1=self.cleaned_data['Tag1'],
            Tag2=self.cleaned_data['Tag2'],
            Tag3=self.cleaned_data['Tag3'],
            arts_id=art
        )

        return art
    


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User_Info
        fields = ['First_Name', 'Last_Name', 'About_Me']
        widgets = {
            'First_Name': forms.TextInput(attrs={'class': 'rectangle-8'}),
            'Last_Name': forms.TextInput(attrs={'class': 'rectangle-7'}),
            'About_Me': forms.TextInput(attrs={'class': 'rectangle-4'}),
        }

    #Campos Adicionales Basados en User_Credentials
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'rectangle-8'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'rectangle-7'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'rectangle-11'}))

    def save(self, commit=True):
        #Guardo la Instancia de las Credenciales para Obtener el ID
        user_credentials = User_Credentials.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']
        )

        #Guardo la Instancia de User_Info basandome en el ID de la Instancia de User_Credentials
        user_info = User_Info.objects.create(
            First_Name=self.cleaned_data['First_Name'],
            Last_Name=self.cleaned_data['Last_Name'],
            About_Me=self.cleaned_data['About_Me'],
            User_ID=user_credentials
        )

class Tag_Search(forms.Form):
    Tag1=forms.ModelChoiceField(Tag_List.objects.all(), required=False)
    Tag2 =forms.ModelChoiceField(Tag_List.objects.all(), required=False)
    Tag3 =forms.ModelChoiceField(Tag_List.objects.all(), required=False)



# Forms to Update Info
class UserCredentialsForm(forms.ModelForm):
    class Meta:
        model = User_Credentials
        fields = ['username', 'password', 'email']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User_Info
        fields = ['First_Name', 'Last_Name', 'About_Me']

class UserSocialForm(forms.ModelForm):
    class Meta:
        model = User_Social
        fields = ['Whatsapp', 'Facebook', 'Instagram']