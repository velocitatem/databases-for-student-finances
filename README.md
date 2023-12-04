# University Finance Data Generator

## Overview

This project combines web scraping using the Hugging Face AI model for named entity recognition and data generation with the Faker library to create financial data for university users. The generated data is then stored in a MongoDB database through a Django application.

After the Database is created with the scraped names and fake fill data we can start using it. We setup 2 views of the data:

1. One that list all the transactions for the user.
2. The other one that get the average budget for a certain age range.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- Django
- MongoDB
- Other dependencies specified in `requirements.txt`

## Installation & Requirement

1. Clone the repository


2. Install dependencies & requirements


3. Set up Django migrations


4. Run the Django development server

5. makes sure mongo is running

6. make sure directory perms are 777

7. docker mong:

```bash
docker run --name some-mongo -d -p 27017:27017 mongo:latest
```



## Usage

### Web Scraping

1. Obtain the Hugging Face API key.
2. Set your API key as an environment variable:
3. Run the web scraping script:


### Data Generation

1. Generate financial data using Faker:


### Database Population

1. Populate the MongoDB database with the generated data:


## Data Models

The Django application defines the following data models:

- User
- Budget
- SubscriptionType
- Subscription
- ExpenseType
- Expense
- Transaction

MongoDB is used for storing transaction data.

## Acknowledgments

- [Hugging Face](https://huggingface.co/) for the named entity recognition model.
- [Faker](https://faker.readthedocs.io/) for data generation.





