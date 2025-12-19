from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    회원 정보 조회(GET) 및 수정(PUT)용 Serializer
    - 로그인 후 내 정보를 받아볼 때 사용됩니다.
    """
    # age는 DB에 저장된 필드가 아니라 모델의 @property로 계산하므로 ReadOnlyField 사용
    age = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'name', 'nickname', 
            'profile_image', 'phone_number', 'birth_date', 
            'money', 'salary', 'job', 'date_joined'
        ]
        # 👇 핵심: 아이디와 이름은 수정 못하게 막음
        read_only_fields = ('username', 'name', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    """
    회원가입용 Serializer
    - 비밀번호 확인 로직 포함
    - 입력받을 모든 필드 정의
    """
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True) # 비밀번호 확인용

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'nickname', 'phone_number', 'birth_date',
            'money', 'salary', 'job'
        ]

    def validate(self, attrs):
        # 비밀번호 일치 검사
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return attrs

    def create(self, validated_data):
        # 1. 패스워드 필드들은 User 모델 생성에 직접 필요 없으니 제거
        validated_data.pop('password2')
        password = validated_data.pop('password')

        # 2. 나머지 데이터(username, email, job, salary 등)를 한 번에 넣어서 유저 생성
        user = User(**validated_data)
        
        # 3. 비밀번호 암호화 저장
        user.set_password(password)
        user.save()
        
        return user