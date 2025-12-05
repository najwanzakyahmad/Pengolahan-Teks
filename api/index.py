from flask import Flask, render_template, request
from collections import Counter
import re

app = Flask(__name__, template_folder="../templates")

@app.route("/", methods=["GET", "POST"])
def index():
    text = request.form.get("text", "")
    result = None
    info = None

    selected_action = request.form.get("action", "search")
    search_word = request.form.get("search_word", "")
    old_word = request.form.get("old_word", "")
    new_word = request.form.get("new_word", "")

    if request.method == "POST":
        if selected_action == "search":
            if search_word.strip():
                tokens = re.findall(r"\w+", text.lower())
                total = tokens.count(search_word.lower())
                info = f"Kata '{search_word}' ditemukan {total} kali."
            else:
                info = "Masukkan kata yang ingin dicari."

        elif selected_action == "replace":
            if old_word and new_word:
                result = text.replace(old_word, new_word)
                info = f"Semua '{old_word}' telah diganti menjadi '{new_word}'."
            else:
                info = "Kata lama dan kata baru wajib diisi."

        elif selected_action == "sort":
            tokens = re.findall(r"\w+", text.lower())
            total_words = len(tokens)
            counts = Counter(tokens)
            sorted_unique = sorted(counts.items(), key=lambda x: x[0])

            output = [f"Total kata dalam teks: {total_words} kata\n"]
            for w, c in sorted_unique:
                output.append(f"{w} ({c} kali)")
            result = "\n".join(output)
            info = "Kata unik telah diurutkan berdasarkan abjad."

    return render_template(
        "index.html",
        text=text,
        result=result,
        info=info,
        selected_action=selected_action,
        search_word=search_word,
        old_word=old_word,
        new_word=new_word,
    )

if __name__ == "__main__":
    app.run(debug=True)