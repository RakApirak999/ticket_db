from flask import Flask, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from supabase import create_client   # ← ย้าย import มาไว้บน

load_dotenv()

app = Flask(__name__)

# สร้าง Supabase client ครั้งเดียวตอน startup
supabase_client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5432),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME")
    )

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM concerts")
    concerts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", concerts=concerts)

@app.route("/api/concerts")
def api_concerts():
    response = supabase_client.table("concerts").select("*").execute()
    return response.data

if __name__ == "__main__":
    app.run(debug=True, port="2202")