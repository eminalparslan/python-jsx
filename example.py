# coding: jsx
# ^^^^^^^^^^^ this enables the magic

from flask import Flask

app = Flask(__name__)

def hello(object: str) -> str:
    return <p>Hello, {object}!</p>

def greetings() -> str:
    return (
        <div>
            <hello object="World" />
            <hello object="Galaxy" />
            <hello object="Universe" />
        </div>
    )

@app.route("/")
def route():
    return <greetings />

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
