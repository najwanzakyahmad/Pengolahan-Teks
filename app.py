from flask import Flask, render_template, request

app = Flask(__name__)

ARTICLE_TEXT = """
TULIS / PASTE ARTIKEL DI SINI...
"""  


def count_word(text: str, word: str) -> int:
    import re
    tokens = re.findall(r"\w+", text.lower())
    target = word.lower()
    return sum(1 for t in tokens if t == target)


@app.route("/", methods=["GET", "POST"])
def index():
    text = ARTICLE_TEXT
    result = None
    info = None

    selected_action = "search"
    search_word = ""
    old_word = ""
    new_word = ""

    if request.method == "POST":
        text = request.form.get("text", ARTICLE_TEXT)
        selected_action = request.form.get("action", "search")

        if selected_action == "search":
            search_word = request.form.get("search_word", "").strip()
            if not search_word:
                info = "Masukkan kata yang ingin dicari."
            else:
                total = count_word(text, search_word)
                info = f"Kata '{search_word}' ditemukan {total} kali dalam artikel."

        elif selected_action == "replace":
            old_word = request.form.get("old_word", "").strip()
            new_word = request.form.get("new_word", "").strip()

            if not old_word or not new_word:
                info = "Kata lama dan kata baru wajib diisi."
            else:
                replaced_text = text.replace(old_word, new_word)
                result = replaced_text
                info = f"Semua '{old_word}' telah diganti menjadi '{new_word}'."

        elif selected_action == "sort":
            import re
            tokens = re.findall(r"\w+", text.lower()) 

            total_words = len(tokens)  

            from collections import Counter
            counts = Counter(tokens)

            sorted_unique_words = sorted(counts.items(), key=lambda x: x[0])

            result_lines = [f"Total kata dalam teks: {total_words} kata\n"]
            
            for word, count in sorted_unique_words:
                result_lines.append(f"{word} ({count} kali)")

            result = "\n".join(result_lines)
            info = "Kata unik telah diurutkan berdasarkan abjad beserta jumlah kemunculannya dan total kata keseluruhan."

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
