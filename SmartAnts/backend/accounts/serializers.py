# backend/accounts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer

# 🐜 finlife 앱의 시리얼라이저 가져오기 (가입한 상품 보여주기용)
from finlife.serializers import DepositOptionsSerializer, SavingOptionsSerializer

User = get_user_model()

# 1. 유저 상세 정보용 (마이페이지에서 사용)
class CustomUserDetailsSerializer(UserDetailsSerializer):
    # 1. 가입한 예금/적금 가져오기 (SerializerMethodField 사용)
    joined_deposits = serializers.SerializerMethodField()
    joined_savings = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = UserDetailsSerializer.Meta.fields + (
            'nickname', 'name', 'phone_number', 'birth_date', 
            'money', 'salary', 'job', 'risk_appetite',
            'joined_deposits', 'joined_savings', # 👈 여기에 추가됨
        )
        read_only_fields = ('username', 'email', 'date_joined')

    # 🐜 예금 목록 반환 함수
    def get_joined_deposits(self, obj):
        # related_name이 'subscribed_deposits'라고 가정 (finlife models.py 확인 필요)
        # 만약 모델에 related_name 설정을 안했다면 depositoptions_set 사용
        if hasattr(obj, 'subscribed_deposits'):
            return DepositOptionsSerializer(obj.subscribed_deposits.all(), many=True).data
        return []

    # 🐜 적금 목록 반환 함수
    def get_joined_savings(self, obj):
        if hasattr(obj, 'subscribed_savings'):
            return SavingOptionsSerializer(obj.subscribed_savings.all(), many=True).data
        return []
        
# 2. 회원가입용 (변경 없음)
class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=20, required=False)
    name = serializers.CharField(max_length=30, required=False)
    birth_date = serializers.DateField(required=False)
    money = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)
    job = serializers.CharField(max_length=20, required=False)
    risk_appetite = serializers.IntegerField(required=False)

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