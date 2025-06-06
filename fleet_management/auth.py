from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.conf import settings
from supabase import Client, create_client

User = get_user_model()

class SupabaseAuthBackend(BaseBackend):
    def __init__(self):
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    def authenticate(self, request, token=None, **kwargs):
        if not token:
            return None

        try:
            # Verify the JWT token with Supabase
            user_data = self.supabase.auth.get_user(token)
            if not user_data:
                return None

            # Get or create the user in Django's database
            user, created = User.objects.get_or_create(
                username=user_data.user.email,
                defaults={
                    'email': user_data.user.email,
                    'is_active': True
                }
            )

            return user
        except Exception as e:
            print(f"Supabase authentication error: {str(e)}")
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None 