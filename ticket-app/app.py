from flask import Flask, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()  # โหลดค่าจากไฟล์ .envp

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5432),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME")   # ← psycopg2 ใช้ "dbname" ไม่ใช่ "database"
    )

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)  # ← ต่างจาก MySQL ตรงนี้
    cursor.execute("SELECT * FROM concerts")
    concerts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", concerts=concerts)

if __name__ == "__main__":
    app.run(debug=True,port = "2202")