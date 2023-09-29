from .models import Profile, Skill
from django.forms import ModelForm


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']
        labels = {
            'name': 'Навык:',
            'description': 'Описание:'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'bio', 'short_info', 'profile_image',
                  'social_inst', 'social_vk', 'social_web']
        labels = {
            'name': 'Введите ФИО',
            'email': 'Введите почту',
            'username': 'Введите имя пользователя',
            'bio': 'Информация',
            'short_info': 'Краткая информация',
            'profile_image': 'Фото',
            'social_inst': 'Инст',
            'social_vk': 'Вконтаке',
            'social_web': 'Веб сайт',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
