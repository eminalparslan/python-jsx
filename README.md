# Python JSX
A proof-of-concept for [JSX syntax](https://react.dev/learn/writing-markup-with-jsx) in Python using "[Python's preprocessor](https://pydong.org/posts/PythonsPreprocessor/)".

There is *no* build step. Everything is done in a preprocessor stage as long as the proper `coding` is specified.

## Example

```python
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
```

## Why?
Why not :^)

## No, really. Why?
...in all seriousness, this could be useful if integrated with mypy to have type-checking for html in Python files, or creating a component-based web framework like React in Python.

## References
- https://pydong.org/posts/PythonsPreprocessor/
- https://github.com/Tsche/magic_codec
