# -*- coding: utf-8 -*-
from os import path
from io import BytesIO
from logging import getLogger, FileHandler

from flask import Flask
from flask import render_template
from flask import abort, send_file, Response
from flask import redirect, url_for

from waitress import serve
from paste.translogger import TransLogger


BASE_DIR = path.dirname(__file__)


def create_app():
    app = Flask(__name__)

    @app.route("/favicon.ico")
    def favicon():
        return send_file(
            filename_or_fp=BytesIO(globals().get("favicon.ico")),
            mimetype="image/x-icon"
        )

    @app.route("/src/<string:img>")
    def src(img: str):
        if img not in ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png", "icon192.png"]:
            abort(404)

        return send_file(
            filename_or_fp=BytesIO(globals().get(img)),
            mimetype="image/png"
        )

    @app.route("/")
    def game():
        return render_template(
            "game.html"
        )

    @app.route("/style.min.css")
    def style():
        return Response(
            mimetype="text/css",
            response="html{color:#dcddde;background-color:#36393f;text-align:center}"
                     ".btn{display:inline-block;border:#dcddde 1px solid;border-radius:.3rem;padding:10px;"
                     "font-size:16px;background-color:#36393f;color:#dcddde}"
                     ".btn:hover{background-color:#dcddde;color:#36393f}"
        )

    @app.route("/robots.txt")
    def robots():
        return Response(
            mimetype="text/plain",
            response="\n".join([
                "User-agent: *",
                "Allow: /$",
                "Allow: /static",
                "Disallow: /",
            ])
        )

    for status in [400, 403, 404, 405]:
        app.register_error_handler(
            status, lambda error: redirect(url_for(".game"))
        )

    return app


if __name__ == "__main__":
    try:
        port = open(path.join(BASE_DIR, "port.txt"), "r").read()
    except (FileNotFoundError, Exception):
        port = 5000

    logger = getLogger("wsgi")
    logger.addHandler(FileHandler(path.join(BASE_DIR, "wsgi.log")))

    globals().update({
        "1.png": open(path.join(BASE_DIR, "src", "1.png"), "rb").read(),
        "2.png": open(path.join(BASE_DIR, "src", "2.png"), "rb").read(),
        "3.png": open(path.join(BASE_DIR, "src", "3.png"), "rb").read(),
        "4.png": open(path.join(BASE_DIR, "src", "4.png"), "rb").read(),
        "5.png": open(path.join(BASE_DIR, "src", "5.png"), "rb").read(),
        "6.png": open(path.join(BASE_DIR, "src", "6.png"), "rb").read(),

        "favicon.ico": open(path.join(BASE_DIR, "src", "favicon.ico"), "rb").read(),
        "icon192.png": open(path.join(BASE_DIR, "src", "icon192.png"), "rb").read(),
    })

    serve(
        app=TransLogger(
            application=create_app(),
            setup_console_handler=True
        ),
        port=port
    )
