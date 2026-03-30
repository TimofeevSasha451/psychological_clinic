from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from psyschologic_backend import settings
from structure.models import (Specialist, Portfolio, Application,
                              WorkMethods, PortfolioMethods)

User = get_user_model()


class PortfolioMethodsSerialzier(serializers.ModelSerializer):
    methods = serializers.StringRelatedField(many=True, read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Portfolio
        fields = ('methods', 'image', 'image_url')

    def get_image_url(self, obj):
        if not obj.image:
            return None

        request = self.context.get('request')  # Берем запрос из контекста
        if request:
            return request.build_absolute_uri(obj.image.url)

        return f"{settings.URL}{obj.image.url}"


class UserSerializer(serializers.ModelSerializer):
    initials = serializers.SerializerMethodField()
    is_specialist = serializers.SerializerMethodField(required=False)
    education = serializers.SerializerMethodField(required=False)
    practice = serializers.SerializerMethodField(required=False)
    link = serializers.SerializerMethodField(required=False)
    work_email = serializers.SerializerMethodField(required=False)
    work_methods = serializers.SerializerMethodField(required=False)
    description = serializers.SerializerMethodField(required=False)

    class Meta:
        model = User
        fields = ('initials', 'phone_number', 'email', 'password',
                  'education', 'practice', 'link', 'work_email',
                  'work_methods', 'description', 'is_specialist')
        read_only_fields = ('is_specialist',)
        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'read_only': True}
        }

    def get_description(self, obj):
        if Specialist.objects.filter(user=obj).exists():
            return Specialist.objects.get(user=obj).portfolio.description

    def get_is_specialist(self, object):
        return Specialist.objects.filter(user=object).exists()

    def get_initials(self, obj):
        print(obj)
        initials = f'{obj.first_name} {obj.last_name}'
        if type(obj.middle_name) is str:
            if len(obj.middle_name) != 0:
                return f'{initials} {obj.middle_name}'
        return initials

    def get_education(self, obj):
        if Specialist.objects.filter(user=obj).exists():
            return Specialist.objects.get(user=obj).portfolio.education

    def get_practice(self, obj):
        if Specialist.objects.filter(user=obj).exists():
            return Specialist.objects.get(user=obj).portfolio.practice

    def get_link(self, obj):
        if Specialist.objects.filter(user=obj).exists():
            return Specialist.objects.get(user=obj).link

    def get_work_email(self, obj):
        if Specialist.objects.filter(user=obj).exists():
            return Specialist.objects.get(user=obj).work_email

    def get_work_methods(self, obj):
        if Specialist.objects.filter(user=obj).exists():
            return PortfolioMethodsSerialzier(
                Specialist.objects.get(user=obj).portfolio
            ).data['methods']

    def to_internal_value(self, data):
        if 'initials' in data:
            initials = data.pop('initials').split(' ')
            data['first_name'] = initials[1]
            data['last_name'] = initials[0]
            if len(initials) == 3:
                data['middle_name'] = initials[2]
        return data

    def validate(self, attrs):
        if self.context['request'].method == 'PATCH':
            return attrs
        user = User(**attrs)
        password = attrs.get("password")

        validate_password(password, user)
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    collection = ['first_name', 'last_name', 'middle_name',
                  'phone_number', 'email', 'password']

    def update(self, instance, validated_data):
        if Specialist.objects.filter(user=instance).exists():
            spec = Specialist.objects.get(user=instance)
            if 'education' in validated_data:
                spec.portfolio.education = validated_data['education']
            if 'description' in validated_data:
                spec.portfolio.description = validated_data['description']
            if 'practice' in validated_data:
                spec.portfolio.practice = validated_data['practice']
            if 'work_methods' in validated_data:
                methods = validated_data['work_methods']
                spec.portfolio.methods.clear()
                for method in methods:
                    current_method, status = WorkMethods.objects.get_or_create(
                        title=method.title)
                    PortfolioMethods.objects.create(
                        portfolio=spec.portfolio,
                        method=current_method
                    )
            if 'work_email' in validated_data:
                spec.work_email = validated_data['work_email']
            if 'first_name' in validated_data:
                spec.user.first_name = validated_data['first_name']
            if 'last_name' in validated_data:
                spec.user.last_name = validated_data['last_name']
            if 'middle_name' in validated_data:
                spec.user.middle_name = validated_data['middle_name']
            spec.save()
        for key in self.collection:
            if key in validated_data:
                setattr(instance, key, validated_data[key])
        instance.save()
        return instance


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('email', 'resume_file')


class SpecialistSerializer(serializers.ModelSerializer):
    initials = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    practice = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    work_methods = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        fields = ('initials', 'education', 'practice', 'description',
                  'work_methods', 'image', 'link')
        model = Specialist

    def get_initials(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def get_education(self, obj):
        return f'{obj.portfolio.education}'

    def get_practice(self, obj):
        return f'{obj.portfolio.practice}'

    def get_description(self, obj):
        return f'{obj.portfolio.description}'

    def get_work_methods(self, obj):
        return PortfolioMethodsSerialzier(obj.portfolio).data['methods']

    def get_image(self, obj):
        return PortfolioMethodsSerialzier(obj.portfolio).data['image_url']

# class Base64ImageField(serializers.ImageField):
#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:image'):
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

#         return super().to_internal_value(data)
