from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
    return render_template('list.html')

if __name__ == "__main__":
    app.run()