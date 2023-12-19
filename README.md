# Project Readme

Hi, I'm Tobi, and welcome to the Doo-Hickey repository.

This project was created in response to a technical interview task assigned to me by CJID. The total build time for this project was 12 hours and 31 minutes. For a demonstration, you can check out this [demo video](https://vimeo.com/896159556/3ace706210).

The primary goal behind Doo-Hickey was to develop a platform capable of extracting text from documents, particularly newspapers. The extracted text is stored in a database, categorized by title and content. This extracted data serves as a resource for training a machine learning model. The aim is to create human-like conversations with the data, allowing users to query the model in natural language and receive human-based responses, utilizing Natural Language Understanding (NLU) and Natural Language Processing (NLP).

Now, let's dive into setting up Doo-Hickey on your machine.


But before that, you'd need to install tesseract on your machine. You can follow this tutorial [here](https://tesseract-ocr.github.io/tessdoc/Installation.html) to do so. 


And also setup pytesseract [here](https://pypi.org/project/pytesseract/)

## Setup Instructions

### Step one:

Clone this repository by entering the following command in your terminal:

```bash
git clone https://github.com/Tobitheprof/cjid.git
```

### Step two:

Navigate into the project directory after cloning the repository:

```bash
cd cjid
```

### Step three:

Install project requirements using the command:

- On windows:
 ```bash
    pip install -r requirements.txt
 ```

 - On Linux:
 ```bash
    pip3 install -r requirements.txt
 ```

### Step four:

Navigate into the project backend by executing the following commands consecutively:

```bash
cd backend
cd cjid_archive

```

### Step five:

Run the Python web server:

- On windows

```bash
python manage.py runserver
```

### Step six:
Run the Celery worker. Ensure you have Redis installed on your computer. You can follow this [tutorial](https://redis.io/docs/install/install-redis/) for installing Redis. 

Run Celery using the following commands:

- On windows:
 ```bash
    celery -A cjid_archive worker -l info --pool=solo
 ```

 - On Linux:
 ```bash
    celery -A cjid_archive worker --loglevel=info
 ```
