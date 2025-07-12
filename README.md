# ChefDeck Python API

## Overview

This is an API created with FastAPI that provides some functionality to the ChefDeck application, specifically fetching recipes from the web and merging ingredients into a grocery list. These tasks are well-suited to python and so were abstracted into a separate API.

## Requirements

- Python 3.10+ (not tested on earlier versions)

## Installation

1. Clone the repository:

  ```sh
  git clone https://github.com/yourusername/yourproject.git
  cd yourproject
  ```
2. Create a virtual environment:
  ```sh
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```

3. Install the required packages:
  ```sh
  pip install -r requirements.txt
  ```

## Usage

To run the application, use the following command:

```sh
fastapi dev src/main.py
```

Once the server is running, you can access the API documentation at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

This will show you the available endpoints and how to use them.

## API Key
Make sure to define an allowed API key using the `ALLOWED_API_KEY` environment variable. You'll then need to include it in the `X-API-Key` header of each request.

## Testing

To run the tests, use:

```sh
pytest
```

Make sure to have `pytest` installed in your environment.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. Note that third party libraries are bundled with the final project, and remain under their respective licenses - see [third_party_licenses](third_party_licenses) for details. 

Ingredient merging uses WordNet, a registered trademark of Princeton University.
Princeton University "About WordNet." WordNet. Princeton University. 2010. 