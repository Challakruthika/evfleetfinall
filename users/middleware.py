from django.contrib.auth import get_user_model
from ev_fleet_management.supabase_utils import get_supabase_client

User = get_user_model()

class SupabaseAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the Supabase token from the request header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Verify token with Supabase
                supabase = get_supabase_client()
                user = supabase.auth.get_user(token)
                if user:
                    # Get or create Django user
                    django_user, created = User.objects.get_or_create(
                        email=user.email,
                        defaults={
                            'username': user.email,
                            'is_active': True
                        }
                    )
                    request.user = django_user
            except Exception as e:
                print(f"Token verification error: {e}")

        response = self.get_response(request)
        return response 