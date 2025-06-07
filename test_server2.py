from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Servidor Flask em execução!"

if __name__ == '__main__':
    app.run(debug=True)
