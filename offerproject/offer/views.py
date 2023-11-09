from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializer import UseroutSerializer,OfferSerializer,OfferOutSerializer,OfferUpdateSerializer
from .models import Offermodel
from rest_framework.decorators import api_view,permission_classes

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer


class UserDetailAPI(APIView):
    def post(self, request):
        data=request.data
        if not data["email"]:
            return Response({'message':'invalid email'},status=status.HTTP_403_FORBIDDEN)
        use1=User.objects.filter(username=data["email"]).first()
        if use1:
           return Response({'message':'email already exist'},status=status.HTTP_208_ALREADY_REPORTED)
        if not len(data["password"])>7:
            return Response({'message':'password is too sort'},status=status.HTTP_403_FORBIDDEN)
        u=User.objects.create(username=data['email'],password=make_password(data['password']))
        
        u.save()
        serializer = UseroutSerializer(u)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Offer(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,off_id=None):
        if not off_id:
            offer_type=request.query_params.get('offertype')
            u1=request.query_params.get('user')
            s_date=request.query_params.get('start_date')
            e_date=request.query_params.get('end_date')
            amount=request.query_params.get('amount')
            
            o=Offermodel.objects.all()
            if offer_type:
                o=Offermodel.objects.filter(offer_type=offer_type).all()
            if u1:
               o=Offermodel.objects.filter(user=u1).all() 
            if s_date:
                o=Offermodel.objects.filter(start_date=s_date).all()
            if e_date:
                o=Offermodel.objects.filter(end_date=e_date).all()
            if amount:
                o=Offermodel.objects.filter(amount__lt=amount).all()
            s=OfferOutSerializer(o,many=True)
            return Response(s.data,status=status.HTTP_200_OK)
        try:
            off=Offermodel.objects.get(id=off_id)
            if off:
                serializer=OfferOutSerializer(off)
                return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({'message':'invalid id'})
    
    def post(self,request):
        offer_data=request.data
        u=request.user
        if not offer_data['amount']:
            return Response({'message':'invalid amount'},status=status.HTTP_403_FORBIDDEN)
        if not offer_data['offer_type']:
            return Response({'message':'invalid offer_type'},status=status.HTTP_403_FORBIDDEN)
        offer_data['user']=u.id
        print(offer_data)
        of_serializer=OfferSerializer(data=offer_data)
        if of_serializer.is_valid():
            of_serializer.save()
            return Response(of_serializer.data,status=status.HTTP_201_CREATED)
        return Response(of_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,off_id):
        if not id:
            return Response({'messege':'id is not valid'},status=status.HTTP_404_NOT_FOUND)
        try:
            off=Offermodel.objects.get(id=off_id)
            u=request.user.id
            if off:
                if u==off.user.id:
                    off_serializer=OfferUpdateSerializer(off,data=request.data,partial=True)
                    if off_serializer.is_valid():
                        off_serializer.save()
                        return Response(off_serializer.data,status=status.HTTP_200_OK)
                    return Response({'message':'somthing went to wrong'})
                return Response({'message':'you are not athorize to do this'})
        except:
            return Response({'message':'id not found'},status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,request,off_id):
        if not id:
            return Response({'messege':'id is not valid'},status=status.HTTP_404_NOT_FOUND)
        try:
            off=Offermodel.objects.get(id=off_id)
            u=request.user.id
            if off:
                if u==off.user.id:
                    off.delete()
                    return Response({'message':'delete successfuly'},status=status.HTTP_204_NO_CONTENT)
                return Response({'message':'you are not athorize to do this'})
            return Response({'message':'invalid offer'})
        except:
            return Response({'message':'id not found'},status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Myoffer(request):
    try:
        o=Offermodel.objects.filter(user=request.user.id).all()
        if not o:
            return Response({'message':'no offer'},status=status.HTTP_204_NO_CONTENT)
        s=OfferOutSerializer(o,many=True)
        return Response(s.data,status=status.HTTP_200_OK)
    except:
         return Response({'message':'somthing went to wrong'},status=status.HTTP_400_BAD_REQUEST)
    

