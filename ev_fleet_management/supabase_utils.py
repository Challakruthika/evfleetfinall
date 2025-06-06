from django.conf import settings
from supabase import Client

def get_supabase_client() -> Client:
    """
    Get the Supabase client instance from Django settings.
    """
    return settings.supabase

def get_user_by_id(user_id: str):
    """
    Get a user from Supabase by their ID.
    """
    supabase = get_supabase_client()
    return supabase.table('user_registration_details').select('*').eq('id', user_id).execute()

def create_user(user_data: dict):
    """
    Create a new user in Supabase.
    """
    supabase = get_supabase_client()
    return supabase.table('user_registration_details').insert(user_data).execute()

def update_user(user_id: str, user_data: dict):
    """
    Update a user in Supabase.
    """
    supabase = get_supabase_client()
    return supabase.table('user_registration_details').update(user_data).eq('id', user_id).execute()

def delete_user(user_id: str):
    """
    Delete a user from Supabase.
    """
    supabase = get_supabase_client()
    return supabase.table('user_registration_details').delete().eq('id', user_id).execute()

def get_all_users():
    """
    Get all users from Supabase.
    """
    supabase = get_supabase_client()
    return supabase.table('user_registration_details').select('*').execute() 