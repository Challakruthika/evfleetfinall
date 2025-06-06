from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from ev_fleet_management.supabase_utils import get_supabase_client

User = get_user_model()

class SupabaseAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Authenticate with Supabase
            supabase = get_supabase_client()
            response = supabase.auth.sign_in_with_password({
                "email": username,
                "password": password
            })
            
            if response.user:
                # Get or create Django user
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': username,
                        'is_active': True
                    }
                )
                return user
        except Exception as e:
            print(f"Authentication error: {e}")
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None 