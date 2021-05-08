# Extract reviews from Daraz.pk

With these scripts you can scrap reviews of any category you choose from Daraz.pk which is Pakistan's largest ecommerce platform. You can use them for NLP, research or just for fun.

## System Requirements
The scripts need the following to be installed in your system:
- [Chrome](https://www.google.com/intl/en_pk/chrome/)
- [Python 3.6](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [virtualenv](https://pypi.org/project/virtualenv/)

## Usage
This is a two step process. And there are two scripts involved. `1_extract_products.py` and `2_extract_reviews.py`. Follow the instructions (Run in commandline):

1. Clone the repository in your system. `git clone https://github.com/sfsultan/daraz_review_data_scraping.git`
2. Change the working directory : `cd daraz_review_data_scraping`
2. Create a virtual enviornemnt: `virutalenv env`
    - If you have multiple python installations, provide the suitable one as the argument.
3. Activate the virutalenv:
    - Linux : `source env/bin/activate`
    - Windows : `env\Scripts\activate`
4. Install all the dependencies:
    - `pip install -r requirements.txt`
1. Run `1_extract_products.py` to extract the product urls for a particular category. Script excepts two arguments.
    - `category name` : The name of the category.
    - `total pages` : Total number of pages that category has.
    - example : `python 1_extract_products.py "smartphones" 56`
The above command will result in a `csv` file containing all the urls for the products of the provided category.
2. Run `2_extract_reviews.py` to extract all the reviews from the urls present in the `csv` file generated in the first step. This script only has one argument: `category name`:
    - example : `python 2_extract_reviews.py "smartphones"`


## How it works
The scripts leverage two python libraries `selenium` and `beautifulsoup` for the data extraction.

## Contacts
[sfsultan](mailto:sfsultan@gmail.com)

## Bibtex

```text
@misc{daraz-review-data-scraping-2021,
  name        = {Fahd Sultan},
  author      = {sfsultan},
  title       = {Extract reviews from Daraz.pk},
  version     = {1},
  date        = {2021-05-08},
  type        = {electronic resource}
}

```
