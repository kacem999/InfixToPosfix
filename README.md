# Infix to Postfix Converter

This project is a web application that converts logical phrases infix to postfix. It's built with Django and Python.
## Features

- Converts logical phrases into postfix.
- make a tree of the logical expression.
- evaluate the logical expression.

## Installation
1. Clone the repository: git clone https://github.com/kacem999/InfixToPosfix.git
2. Install the requirements: pip install -r requirements.txt
3. Run the Django server: python manage.py runserver
4. Run the Django server: python manage.py runserver
5. Open your web browser and navigate to `http://localhost:8000`.

## Usage
1. Enter a logical expression in the input field.
2. Click the "Convert" button to convert the expression into postfix.
3. gives the truth value to each variable to evaluate the expression.
4. click the "evaluate" button to evaluate the expression.

- The logical expression must be in propositional logic.
- The logical operators supported are: 
    - `!` for negation.
    - `&` for conjunction.
    - `|` for disjunction.
    - `>` for implication.
    - `=` for equivalence.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Note
You must have the following installed on your machine:
- Python 3.8 or higher : https://www.python.org/downloads/

## Authors
- Kacem Cherifi

## License
[MIT](https://choosealicense.com/licenses/mit/)