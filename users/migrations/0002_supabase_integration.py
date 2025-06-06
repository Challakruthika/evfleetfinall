from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            # Create Supabase RLS (Row Level Security) policies
            """
            -- Enable RLS on user_registration_details
            ALTER TABLE user_registration_details ENABLE ROW LEVEL SECURITY;

            -- Create policy for authenticated users to read all users
            CREATE POLICY "Users can view all users"
                ON user_registration_details
                FOR SELECT
                USING (auth.role() = 'authenticated');

            -- Create policy for users to update their own records
            CREATE POLICY "Users can update own record"
                ON user_registration_details
                FOR UPDATE
                USING (auth.uid() = id)
                WITH CHECK (auth.uid() = id);

            -- Create policy for admin users to manage all records
            CREATE POLICY "Admins can manage all users"
                ON user_registration_details
                FOR ALL
                USING (auth.role() = 'service_role');
            """,
            # Rollback SQL
            """
            ALTER TABLE user_registration_details DISABLE ROW LEVEL SECURITY;
            DROP POLICY IF EXISTS "Users can view all users" ON user_registration_details;
            DROP POLICY IF EXISTS "Users can update own record" ON user_registration_details;
            DROP POLICY IF EXISTS "Admins can manage all users" ON user_registration_details;
            """
        ),
    ] 