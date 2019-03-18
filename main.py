from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from translate import Translator

app = Flask(__name__)
db = SQLAlchemy(app)

# models
class TranslateText(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    text = db.Column(db.String(1000), unique=False, nullable=True)
    from_lang = db.Column(db.String(25), unique=False, nullable=False)
    to_lang = db.Column(db.String(25), unique=False, nullable=False)

class TranslateHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    text = db.Column(db.String(1000), unique=False, nullable=True)
    t_text = db.Column(db.String(1000), unique=False, nullable=True)
    from_lang = db.Column(db.String(25), unique=False, nullable=False)
    to_lang = db.Column(db.String(25), unique=False, nullable=False)


with open("langs.txt") as f:
    langs = f.readlines()

@app.route("/", methods=["POST", "GET"])
def translator():
    return render_template("home.html", langs=langs)

@app.route("/translate", methods=["POST"])
def translate():
    user_text = request.form["text"]
    from_lang = request.form["from"]
    to_lang = request.form["to"]

    text = TranslateText(text=user_text, from_lang=from_lang, to_lang=to_lang)

    db.create_all()
    db.session.add(text)
    db.session.commit()
    
    text_t = TranslateText.query.filter_by(id=text.id).first()
    
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    translation = translator.translate(text_t.text)

    t_his = TranslateHistory(text=user_text, t_text=translation, from_lang=from_lang, to_lang=to_lang)

    db.create_all()
    db.session.add(t_his)
    db.session.commit()

    return jsonify(result=translation)

@app.route("/history")
def history():
    try:
        history = TranslateHistory.query.all()
    except:
        return "There is no translation history!"
    return render_template("history.html", history=history)

@app.route("/save")
def save():
    history = TranslateHistory.query.all()
    file = open("trans_history.txt", 'a')
    for h in history:
        file.write(str(h.text))
        file.write("\n")
        #file.write(str(h.t_text))
        file.write("\n")
        file.write(str(h.from_lang))
        file.write("\n")
        file.write(str(h.to_lang))
        file.write("\n")
        file.write("\n")
    file.close()
    return "File has been created!"


if __name__ == "__main__":
    app.run(debug=True)
