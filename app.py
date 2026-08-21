from datetime import date

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip().title()
        birthday_text = request.form.get("birthday", "")

        if not name or not birthday_text:
            error = "Please enter your name and date of birth."
        else:
            try:
                birthday = date.fromisoformat(birthday_text)
            except ValueError:
                error = "Please enter a valid date of birth."
            else:
                today = date.today()
                age = today.year - birthday.year - (
                    (today.month, today.day) < (birthday.month, birthday.day)
                )

                if age < 18:
                    error = "You must be 18 or older to continue."
                elif birthday > today:
                    error = "Your date of birth cannot be in the future."
                else:
                    result = {
                        "name": name,
                        "birthday": birthday.strftime("%B %d, %Y"),
                        "age": age,
                    }

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)
