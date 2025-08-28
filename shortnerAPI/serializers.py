from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

import qrcode
import io
import base64

from .models import ShortedURL
from .utils import convert_to_base62


class UserSerializer(serializers.ModelSerializer):
    """
        User class serializer
    """
    class Meta:
        model = get_user_model()
        fields = ('username')


class ShortedURLSerializer(serializers.ModelSerializer):
    """
        Serializer for ShortedURL class 
    """
    original_url = serializers.URLField(
        error_messages={
            'invalid': 'Please enter a valid URL (e.g., https://example.com)',
            'required': 'URL is required',
            'blank': 'URL cannot be empty'
        }
    )
    shorted_url = serializers.SerializerMethodField()
    creation_date = serializers.DateField(read_only=True)
    click_count = serializers.IntegerField(read_only=True)
    expiration_date = serializers.DateField(read_only=True)
    days_alive = serializers.IntegerField(required=False)
    qr_code = serializers.SerializerMethodField()
    # user = UserSerializer()
    
    class Meta:
        model = ShortedURL
        fields = (
            'original_url',
            'shorted_url',
            'creation_date',
            'expiration_date',
            'click_count',
            'days_alive',
            'qr_code'
        )

    def get_qr_code(self, obj):
        """
            Returns qr code for shortened URL as base64 string
        """
        
        if not obj.shorted_url:
            return None
        
        request = self.context.get('request', None)
        if request is not None:
            full_url = f"http://{request.get_host()}/api/{obj.shorted_url}"
                
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(full_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        result = f"data:image/png;base64,{img_str}"
        
        return result
    
    def get_shorted_url(self, obj):
        """Return the full URL format for the shortened URL"""
        if obj.shorted_url:
            request = self.context.get('request', None)
            if request is not None:
                return f"http://{request.get_host()}/api/{obj.shorted_url}"
        return None
    
    def validate_days_alive(self, val):
        if val < 1 or val > 30:
            raise serializers.ValidationError("URL should stay alive less then 30 day")
        return val 
        
    def create(self, validated_data: dict):
        shorted_instance: ShortedURL = super().create({'original_url': validated_data['original_url']})
        # Creating short url vie converting id into base62
        shorted_url = convert_to_base62(shorted_instance.id)
        shorted_instance.shorted_url = shorted_url

        days_alive = validated_data.get('days_alive', None)
        # Only set default expiration if not provided in request
        if days_alive is None:
            days_alive = 7
        expiration_date = shorted_instance.creation_date + timedelta(days=days_alive)
        shorted_instance.expiration_date = expiration_date

        shorted_instance.save(update_fields=('shorted_url', 'expiration_date'))
        return shorted_instance