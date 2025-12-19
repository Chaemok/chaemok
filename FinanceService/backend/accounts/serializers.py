# backend/accounts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer

User = get_user_model()

# 1. 유저 상세 정보용 (로그인 후 유저 정보 가져올 때 및 프로필 조회/수정용)
class CustomUserDetailsSerializer(UserDetailsSerializer):
    age = serializers.ReadOnlyField() # 모델의 @property

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = UserDetailsSerializer.Meta.fields + (
            'nickname', 'name', 'phone_number', 'birth_date', 'age',
            'money', 'salary', 'job', 'risk_appetite', 'financial_products'
        )
        read_only_fields = ('username', 'name', 'date_joined')
        
# 2. 회원가입용 (가입 시 우리가 만든 추가 필드들을 DB에 저장함)
class CustomRegisterSerializer(RegisterSerializer):
    # RegisterSerializer는 기본적으로 username, email, password만 처리함
    # 추가 필드를 정의해줌
    nickname = serializers.CharField(max_length=20, required=False)
    name = serializers.CharField(max_length=30, required=False)
    birth_date = serializers.DateField(required=False)
    money = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)
    job = serializers.CharField(max_length=20, required=False)
    risk_appetite = serializers.IntegerField(required=False)

    # 실제 DB 저장은 여기서 일어남
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'nickname': self.validated_data.get('nickname', ''),
            'name': self.validated_data.get('name', ''),
            'birth_date': self.validated_data.get('birth_date', None),
            'money': self.validated_data.get('money', 0),
            'salary': self.validated_data.get('salary', 0),
            'job': self.validated_data.get('job', 'etc'),
            'risk_appetite': self.validated_data.get('risk_appetite', 3),
        })
        return data

    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get('nickname', '')
        user.name = self.validated_data.get('name', '')
        user.birth_date = self.validated_data.get('birth_date')
        user.money = self.validated_data.get('money', 0)
        user.salary = self.validated_data.get('salary', 0)
        user.job = self.validated_data.get('job', 'etc')
        user.risk_appetite = self.validated_data.get('risk_appetite', 3)
        user.save()
        return user

