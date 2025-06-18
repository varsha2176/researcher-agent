from flask import Flask, request, render_template
import wikipedia
from datetime import datetime

app = Flask(__name__)

# File path to save Q&A history
HISTORY_FILE = "qa_history.txt"

def get_wikipedia_summary(query):
    try:
        return wikipedia.summary(query, sentences=5)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {', '.join(e.options[:5])}..."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find any relevant information."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def save_to_history(question, answer):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - Q: {question}\nA: {answer}\n\n")

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        question = request.form["question"]
        answer = get_wikipedia_summary(question)
        save_to_history(question, answer)
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
