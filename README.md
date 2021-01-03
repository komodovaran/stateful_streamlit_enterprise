## What is this?
An example of how one can track state between multiple pages in *Streamlit* without reloading pages.

Inspired by https://gist.github.com/okld/0aba4869ba6fdc8d49132e6974e2e662

In addition to this, it also demonstrates Mypy type-safety with classes, decorators, inheritance, wrapping Streamlit, etc.

Instead of using `self` you'll find that all data lives in the session `sess`.

Tested on Python 3.7 and Streamlit 0.73.

## How to run this
1. Create a venv and populate it with `pip install -r requirements.txt`
2. Generate some sample data for the app `python scripts/generate_data.py`
3. Start the app with `streamlit run src/app.py`
4. Run tests (there's one, I haven't gotten to that yet) with `pytest`