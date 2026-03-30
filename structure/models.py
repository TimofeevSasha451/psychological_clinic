from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    CHOICES_ROLES = [
        ('user', 'Пользовтаель'),
        ('admin', 'Администратор')
    ]
    middle_name = models.CharField('Отчество', max_length=150, blank=True,
                                   null=True)
    first_name = models.CharField('Имя', max_length=150, blank=False,
                                  null=False)
    last_name = models.CharField('Фамилия', max_length=150, blank=False,
                                 null=False)
    email = models.EmailField('Почта', blank=True, null=True)
    phone_number = PhoneNumberField(unique=True)
    username = models.CharField(unique=True, blank=True, null=True)
    role = models.CharField(
        'Роль пользователя',
        choices=CHOICES_ROLES,
        default='user',
        max_length=157
    )
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']


    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('last_name',)

    def __str__(self):
        initials = self.last_name + ' ' + self.first_name
        if type(self.middle_name) is str:
            if len(self.middle_name) != 0:
                return initials + ' ' + self.middle_name
        return self.last_name + ' ' + self.last_name


class Application(models.Model):
    email = models.EmailField('Электронная почта')
    resume_file = models.FileField(
        upload_to='resumes/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'docx'])
        ],
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.email


class WorkMethods(models.Model):
    title = models.CharField('Название метода', max_length=30)

    class Meta:
        verbose_name = 'Метод работ'
        verbose_name_plural = 'Методы работы'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Portfolio(models.Model):
    education = models.CharField('Образование', max_length=255)
    practice = models.TextField('Опыт работы')
    description = models.TextField('Описание')
    methods = models.ManyToManyField(
        WorkMethods,
        verbose_name='Методы работы',
        related_name='portfolio',
        through='PortfolioMethods',
    )
    image = models.ImageField('Фотография', upload_to='specialists/photos',
                              blank=True, null=True)

    class Meta:
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'
        ordering = ('description',)

    def __str__(self):
        return self.description[:20]


class Specialist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Психолог'
    )
    portfolio = models.OneToOneField(
        Portfolio,
        on_delete=models.SET_NULL,
        verbose_name='Портфолио специалиста',
        null=True
    )
    link = models.CharField('Ссылка для консультации')
    work_email = models.EmailField('Корпоративная почта')

    class Meta:
        verbose_name = 'Психилог'
        verbose_name_plural = 'Психологи'

    def __str__(self):
        return f'{self.user.last_name} {self.user.last_name} является специалистом'


class PortfolioMethods(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE,
                                  related_name='work_methods')
    method = models.ForeignKey(WorkMethods, on_delete=models.CASCADE,
                               related_name='portfolios')

    class Meta:
        verbose_name = 'Метод в работе'
        verbose_name_plural = 'Методы в работе'

    def __str__(self):
        return f'метод {self.method} используется в {self.portfolio}'