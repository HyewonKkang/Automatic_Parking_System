from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework import status
from .models import User, Cars, ParkingSlot, Reservation
from .serializers import UserSerializer, CarsSerializer, ParkingSlotSerializer, ReservationSerializer

# 현재 로그인 중인 유저의 정보를 담는 클래스(일종의 세션 역할)
global current_user

class UserInfo():
    id = ''
    pw = ''
    name = ''
    
    def __init__(self, id, pw, name):
        self.id = id
        self.pw = pw
        self.name = name   

current_user = UserInfo('', '', '')
        
# Create your views here.
# 그냥 이것저것 테스트용 class. 무시해도 됨
class Test(generics.ListAPIView):  
    id = 'aaa'
    pw = 'aa'
    
    # 유효성 검증
    queryset = User.objects.filter(user_id=id)  # user_id에 위에서 얻어온 id값이 들어가야 함
    if queryset:
        values = queryset.values()[0]
        # id 존재, 그러나 pw 불일치
        if values.get('password') == pw: 
            # 로그인 성공 시, 받아온 정보를 담은 current_user에 저장
            global current_user
            current_user.id = id
            current_user.id = pw
            current_user.name = values.get('name')
        else:
            queryset = User.objects.none()    # valid하지 않으면 empty queryset 반환하는 것으로 valid 여부 판단  
    # id 존재하지 않음
    else:
        queryset = User.objects.none()
        
    serializer_class = UserSerializer 
   
    
# ----------------------------------------------------------------------------
# 로그인 화면에서 id, pw 받아와 유효성 검증
class CheckValidation(generics.ListAPIView):
    # 데이터 받아오기 파트 
    id = ''
    pw = ''
    
    # -------------------------------------

    # 유효성 검증
    queryset = User.objects.filter(user_id=id)  # user_id에 위에서 얻어온 id값이 들어가야 함
    if queryset:
        values = queryset.values()[0]
        # id 존재, 그러나 pw 불일치
        if values.get('password') == pw: 
            # 로그인 성공 시, 받아온 정보를 담은 UserInfo 클래스 인스턴스 생성
            global current_user
            current_user = UserInfo('ddd', 'ddd', 'ddd') 
        else:
            queryset = User.objects.none()    # valid하지 않으면 empty queryset 반환하는 것으로 valid 여부 판단  
    # id 존재하지 않음
    else:
        queryset = User.objects.none()
        
    serializer_class = UserSerializer  
    
# 회원가입 시, 새로운 아이디 중복체크 (*테스트 가능) 
class CheckDuplication(generics.ListAPIView):
    # 데이터 받아오기 파트 
    id = ''
    pw = ''
    
    # -------------------------------------
    
    # 중복 체크 (반환된 queryset이 있으면 중복)
    queryset = User.objects.filter(user_id=id)
    serializer_class = UserSerializer  

# 회원가입 정보를 받아와 신규 회원 추가 
def CheckDuplication(request):
     # 데이터 받아오기 파트 
     if request.method == 'POST':
        user = User()
        car = Cars()
        user.user_id = request.POST['Id']
        user.password = request.POST['Password']
        # birthday input 형식 frontend에서 정해지면 수정
        birthday_year = request.POST['year']
        birthday_monthDate = request.POST['monthDate']
        print("birthday_year"+birthday_year)
        print("birthday_monthDate"+birthday_monthDate)
        #birthday
        #post.birthday = birthday_year
        user.phone_number = request.POST['phone']
        user.point = 0
        user.total_fee = 0
        car.car_number = request.POST['Car Number']
        car.user_id = user.user_id
        car.car_type = request.POST['Car Type']
        user.save()
        return redirect('signup')
    

# 새로운 예약 등록
class CreateResv(generics.CreateAPIView):
    queryset = ''
    
# 개인 예약 내역 조회 (*테스트 가능)
class GetUserResv(generics.RetrieveAPIView):
    global current_user
    queryset = Reservation.objects.filter(user_id=current_user.id)
    serializer_class = ReservationSerializer
    
# 예약 취소
class DeleteResv(generics.UpdateAPIView):
    queryset = ''
    
# 개인 정보 조회 
class GetUserInfo(generics.RetrieveAPIView):
    queryset = ''
    
# 개인 정보 수정
class UpdateUserInfo(generics.RetrieveUpdateAPIView):
    queryset = ''

# 개인 보유 포인트 조회 ?   
class GetUserPoint(generics.RetrieveAPIView):
    queryset = ''

# 포인트 충전
class ChargeUserPoint(generics.RetrieveUpdateAPIView):
    queryset = ''




    
    