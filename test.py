from flask_bootstrap import Bootstrap
from flask import Flask, render_template
#...

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('test.html')


if __name__=="__main__":
    app.run(debug=True)
