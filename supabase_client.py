from supabase import create_client, Client

SUPABASE_URL = "https://faeszxdbqizoxomjaybh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZhZXN6eGRicWl6b3hvbWpheWJoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAzMzM0MjAsImV4cCI6MjA2NTkwOTQyMH0.dfpv-0_YGMhha54v60fu-jLhs04_VOnr9o_Osb8QjzI"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
