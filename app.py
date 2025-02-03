import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect

import db

load_dotenv()

app = Flask(__name__)
csrf = CSRFProtect()
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
csrf.init_app(app)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            db.insert_item(name)
            flash(f"{name} added to the list.", "success")
        return redirect(url_for(home.__name__))
    items = db.select_all_items()
    context = {"items": items}
    return render_template("home.html", **context)


@app.post("/toggle/<int:item_id>")
def toggle_item(item_id: int):
    db.update_item_toggle_checked(item_id)
    return redirect(url_for(home.__name__))


@app.post("/delete/<int:item_id>")
def delete_item(item_id: int):
    db.delete_item(item_id)
    flash(f"Item {item_id} deleted", "success")
    return redirect(url_for(home.__name__))
