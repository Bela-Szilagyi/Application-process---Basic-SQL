'''
TODO
    mogrify
    html include
'''

import sys
from flask import Flask, render_template, request, redirect
import psycopg2
import data_manager
from part1_routes import part1_routes
from part2_routes import part2_routes


app = Flask(__name__)
app.register_blueprint(part1_routes)
app.register_blueprint(part2_routes)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=e), 404


@app.errorhandler(500)
def internal_server(e):
    return render_template('error.html', error=e), 500


if __name__ == '__main__':
    app.run(debug=False)
