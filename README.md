# submition_pemda

├── tests
    └── test_extract.py
    └── test_transform.py
    └── test_load.py
├── utils
    └── extract.py
    └── transform.py
    └── load.py
├── main.py
├── requirements.txt
├── submission.txt
├── products.csv
├── google-sheets-api.json

## Menjalankan skrip
python3 main.py

## Menjalankan unit test pada folder tests
python3 -m pytest tests

## Menjalankan test coverage pada folder tests
coverage run -m pytest tests
