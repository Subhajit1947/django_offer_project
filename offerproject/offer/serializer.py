from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Offermodel
class UseroutSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ["id","username"]


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model=Offermodel
        fields=['id','user','amount','offer_type','start_date','end_date','additional_info']
    def validate(self, data):
        user_id=data['user']
        start_date=data['start_date']
        end_date=data['end_date']
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        if start_date>end_date:
            raise serializers.ValidationError("Start date must be before the end date")
        overlapping_offers = Offermodel.objects.filter(
            user=user_id,
            start_date=start_date,
            end_date=end_date,
        ).exclude(id=data.get('id'))
        if overlapping_offers.exists():
            raise serializers.ValidationError("Overlapping offers for the same user and same date are not allowed.")

        return data
    def validate_offer_type(self, value):
        valid_offer_types = ['money', 'percentage', 'fixed_amount']
        if value not in valid_offer_types:
            raise serializers.ValidationError(f"Invalid offer_type. Must be one of: {valid_offer_types}")
        return value

class OfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Offermodel
        fields=['id','user','amount','offer_type','start_date','end_date','additional_info']
    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        if 'start_date'and 'end_date' in data:
            if data['start_date']>data['end_date']:
                raise serializers.ValidationError("Start date must be before the end date")
        return data
    
class OfferOutSerializer(serializers.ModelSerializer):
    user=UseroutSerializer()
    class Meta:
        model=Offermodel
        fields=['id','user','amount','offer_type','start_date','end_date','additional_info']
