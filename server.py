from flask import Flask, render_template, request, redirect
import data_logic


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    return render_template('list.html', dict=data_logic.get_all_questions())


if __name__ == "__main__":
    app.run()
