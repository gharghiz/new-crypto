from flask import Flask, render_template
from db.database import init_db, get_news, get_stats

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    news = get_news(100)
    stats = get_stats()
    return render_template("index.html", news=news, stats=stats)

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
