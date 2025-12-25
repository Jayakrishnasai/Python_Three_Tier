import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def init_db():
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ Error: DATABASE_URL not found in .env file.")
        return

    print("🚀 Connecting to Supabase PostgreSQL...")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        # Read the schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        print("📝 Executing Production Schema (public.tasks, RLS, user_id)...")
        cur.execute(schema_sql)
        
        # Commit the changes
        conn.commit()
        
        print("✅ Database initialized successfully with production constraints!")
        
        # Close connections
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")

if __name__ == "__main__":
    init_db()
