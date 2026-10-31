# CosmoE: An AI-Powered Product Search and Recommendation System for Home Decor E-Commerce

> An academic project that combines web scraping, Natural Language Processing (NLP) and transformer-based semantic search to help users discover home decor, kitchen and wooden products across multiple online marketplaces.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [Scope of the Project](#4-scope-of-the-project)
5. [System Architecture](#5-system-architecture)
6. [Methodology](#6-methodology)
7. [Key Features](#7-key-features)
8. [Technology Stack](#8-technology-stack)
9. [Dataset](#9-dataset)
10. [Database Design](#10-database-design)
11. [Project Structure](#11-project-structure)
12. [Installation and Setup](#12-installation-and-setup)
13. [Application Routes](#13-application-routes)
14. [Limitations](#14-limitations)
15. [Future Work](#15-future-work)
16. [Learning Outcomes](#16-learning-outcomes)
17. [Author](#17-author)
18. [License](#18-license)

---

## 1. Project Overview

**CosmoE** is a full-stack web application built with the Django framework. It collects product listings from popular e-commerce platforms, namely **Daraz.pk** and **Etsy**, and gives users one place to browse and search them.

The project's main contribution is its **intelligent search engine**. Traditional e-commerce search relies on exact keyword matching, which often fails when a user describes a product in different words from the seller. CosmoE addresses this with two search strategies:

- **Semantic search (Smart Search):** uses **BERT** (Bidirectional Encoder Representations from Transformers) to understand the *meaning* of a query and match it with similar product titles, even when they share no exact words.
- **Keyword search (Formal Search):** uses the **spaCy** NLP library to pull the important keywords out of a query and rank products by how relevant those keywords are.

The project shows a practical use of Machine Learning and NLP in information retrieval and recommender systems, applied to a real e-commerce dataset.

---

## 2. Problem Statement

Online shoppers looking for home decor and handmade products face several challenges:

1. **Scattered information:** Products are spread across many marketplaces, so users have to visit and compare several websites by hand.
2. **Limited keyword search:** Most platforms use literal keyword matching. A search for *"wooden wall art"* may miss a product titled *"laser cut wall hanging for living room"*, even though both describe the same kind of item.
3. **Information overload:** Product titles are often long and stuffed with keywords, which makes it hard for users to find the most relevant, best-rated items quickly.

This project asks: **can transformer-based language models improve product discovery by understanding the meaning behind a user's query rather than only its exact words?**

---

## 3. Objectives

The main objectives of the project are:

1. To design and build an **automated web scraper** that collects product data (title, price, rating, reviews, sales and images) from multiple e-commerce websites.
2. To store and manage the collected data in a **structured relational database**.
3. To build a **semantic search engine** using pre-trained BERT embeddings and cosine similarity.
4. To build a **keyword search engine** using spaCy's NLP pipeline for stop-word removal and keyword extraction.
5. To **rank search results** by product quality signals such as rating, units sold and review count.
6. To develop a **user-friendly web interface** for browsing products by category and searching for them.

---

## 4. Scope of the Project

- **Domain:** Home decor, kitchen and wooden handcrafted products.
- **Data sources:** Daraz.pk (Pakistan's largest online marketplace) and Etsy (a global marketplace for handmade goods).
- **Users:** Online shoppers who want to discover and compare products, and administrators who manage product data.
- **Out of scope:** Payments, user accounts, order management and real-time price tracking.

---

## 5. System Architecture

The system follows Django's **Model-View-Template (MVT)** architecture and is organised into four layers:

```
+--------------------------------------------------------------+
|                     Presentation Layer                       |
|        HTML Templates · CSS · jQuery · Font Awesome          |
+------------------------------+-------------------------------+
                               |
+------------------------------v-------------------------------+
|                    Application Layer (Django)                |
|   Views: Home · Category · Smart Search · Formal Search ·    |
|          Scraper · About · Contact · Admin Panel             |
+-------+-----------------------+----------------------+-------+
        |                       |                      |
+-------v--------+   +----------v---------+   +--------v-------+
| Data Collection|   | Intelligence Layer |   |   Data Layer   |
| Selenium +     |   | BERT embeddings    |   | MySQL DB       |
| BeautifulSoup  |   | Cosine similarity  |   | CSV dataset    |
| (Daraz, Etsy)  |   | spaCy NLP pipeline |   | Pickle files   |
+----------------+   +--------------------+   +----------------+
```

---

## 6. Methodology

The project was developed in five stages:

### 6.1 Data Collection (Web Scraping)

- **Selenium WebDriver** loads product listing pages automatically, including content that is rendered by JavaScript.
- **BeautifulSoup** parses the HTML and extracts each product's title, price, rating, review count, sales count, image URL and product link.
- The scraper handles each website's different HTML structure separately and deals with edge cases. For example, when Daraz shows a placeholder base64 image, the scraper opens the product page to get the real image URL.

### 6.2 Data Storage and Preprocessing

- Scraped records are saved to a **MySQL** database through the Django ORM.
- The data is exported to CSV so it can be used for model processing.
- Product titles are **tokenized** with the BERT tokenizer and saved for reuse.

### 6.3 Semantic Search Using BERT

1. **Embedding generation:** Each product title is passed through the pre-trained `bert-base-uncased` model. The output vector of the **[CLS] token** (768 dimensions) is used as the title's embedding.
2. **Precomputation:** Embeddings for every product are computed once and stored in a pickle file (`product_embeddings.pkl`). This avoids running the model on every product for each search.
3. **Query encoding:** At search time, the user's query is turned into an embedding with the same model.
4. **Similarity matching:** **Cosine similarity** is calculated between the query embedding and every product embedding:

   ```
   similarity(q, p) = (q · p) / (‖q‖ × ‖p‖)
   ```

5. **Ranking:** The 20 most similar products are re-ranked by **rating**, **sold count** and **review count**, so the results are both relevant and good quality.

### 6.4 Keyword Search Using spaCy

1. The query is processed with spaCy's `en_core_web_lg` language model.
2. **Stop words** (such as "the", "for" and "with") and **punctuation** are removed, leaving the meaningful keywords.
3. Each product title is scored by how many of these keywords it contains.
4. Products are sorted by keyword score, and the top 30 are returned.

### 6.5 Web Application Development

- The backend is built with **Django 4.2**, using its ORM, URL routing and template engine.
- **Pagination** shows 20 products per page.
- The **Django admin panel** is customised with search, filter and list-display options for managing products.

---

## 7. Key Features

| Feature | Description |
|---------|-------------|
| **Multi-source web scraper** | Collects product data from Daraz.pk and Etsy automatically |
| **Smart semantic search** | BERT-based search that understands what the user means |
| **Keyword search** | spaCy-based search with stop-word removal and keyword scoring |
| **Quality-based ranking** | Results are ranked by rating, sales and reviews |
| **Category browsing** | Separate pages for Home Decor, Kitchen and Wooden products |
| **Top-rated home page** | Products sorted by rating, 20 per page |
| **Admin dashboard** | Manage, search and filter product records |
| **Informational pages** | About Us and Contact Us pages |

---

## 8. Technology Stack

| Category | Technologies |
|----------|--------------|
| **Programming language** | Python 3.11 |
| **Web framework** | Django 4.2 |
| **Database** | MySQL |
| **Web scraping** | Selenium, WebDriver Manager, BeautifulSoup4 |
| **Deep learning / NLP** | Hugging Face Transformers (BERT), PyTorch, spaCy |
| **Machine learning and data** | scikit-learn, NumPy, pandas |
| **Frontend** | HTML5, CSS3, jQuery, Font Awesome, Animate.css |
| **Tools** | Google Chrome, Visual Studio Code, Git |

---

## 9. Dataset

The dataset was collected by the project's own scraper and contains **1,375 product records**:

| Source | Number of products |
|--------|--------------------|
| Etsy | 868 |
| Daraz.pk | 409 |
| Other / unlinked | 98 |
| **Total** | **1,375** |

Each record contains the following attributes:

| Attribute | Description |
|-----------|-------------|
| `title` | Product name or description |
| `rating` | Customer rating |
| `review_count` | Number of customer reviews |
| `sold_count` | Number of units sold |
| `price` | Product price |
| `image_src` | URL of the product image |
| `addtocart_href` | Link to the original product page |
| `created_at` | Date and time the record was collected |

The dataset is available at `csv_files/scrapdata_productrecord.csv`.

---

## 10. Database Design

The system uses a single main table, defined by the `ProductRecord` model:

```python
class ProductRecord(models.Model):
    title          = models.CharField(max_length=255)
    rating         = models.CharField(max_length=50)
    review_count   = models.CharField(max_length=50)
    sold_count     = models.CharField(max_length=50)
    price          = models.CharField(max_length=50)
    image_src      = models.CharField(max_length=255)
    addtocart_href = models.TextField(max_length=500)
    created_at     = models.DateTimeField(auto_now_add=True)
```

---

## 11. Project Structure

```
cosmoe/
├── manage.py                     # Django command-line utility
├── cosmoe/                       # Project configuration
│   ├── settings.py               # Settings (database, apps, static files)
│   ├── urls.py                   # Root URL configuration
│   ├── wsgi.py / asgi.py         # Server entry points
├── scrapdata/                    # Main application
│   ├── models.py                 # ProductRecord data model
│   ├── views.py                  # Page views and web scraper
│   ├── utils.py                  # BERT and spaCy search engines
│   ├── urls.py                   # Application routes
│   ├── admin.py                  # Admin panel configuration
│   └── model_files/              # Precomputed ML artefacts
│       ├── product_embeddings.pkl
│       ├── preprocessed_titles.pkl
│       └── scrapdata_productrecord.csv
├── csv_files/                    # Exported dataset
├── templates/                    # HTML templates
└── static/                       # CSS, JavaScript and images
```

---

## 12. Installation and Setup

### 12.1 Prerequisites

- Python 3.11
- MySQL Server
- Google Chrome (needed only to run the scraper)

### 12.2 Clone the repository

```bash
git clone https://github.com/<your-username>/cosmoe.git
cd cosmoe
```

### 12.3 Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# macOS / Linux
source venv/bin/activate
```

### 12.4 Install dependencies

```bash
pip install django==4.2.5 mysqlclient algoliasearch-django selenium webdriver-manager beautifulsoup4 transformers torch spacy scikit-learn pandas numpy
python -m spacy download en_core_web_lg
```

The BERT model (`bert-base-uncased`) downloads automatically the first time the application starts.

### 12.5 Configure environment variables

For local development, set the Django environment variables before running the application:

```powershell
# Windows PowerShell
$env:DJANGO_DEBUG = "True"
$env:DJANGO_SECRET_KEY = "local-development-key"
```

```bash
# macOS / Linux
export DJANGO_DEBUG=True
export DJANGO_SECRET_KEY=local-development-key
```

For production, configure `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS` in the hosting provider's environment settings, and leave `DJANGO_DEBUG` unset or set to `False`. Configure `ALGOLIA_APPLICATION_ID` and `ALGOLIA_API_KEY` there only if Algolia is enabled.

### 12.6 Configure the database

Create the MySQL database:

```sql
CREATE DATABASE cosmoe CHARACTER SET utf8mb4;
```

If your MySQL credentials are different, update the `DATABASES` section in `cosmoe/settings.py`. Then apply the migrations:

```bash
python manage.py migrate
python manage.py createsuperuser   # optional, for admin access
```

### 12.7 Load the product data

Choose one of the following:

- **Import the dataset:** import `csv_files/scrapdata_productrecord.csv` into the `scrapdata_productrecord` table (for example with MySQL Workbench or phpMyAdmin).
- **Run the scraper:** start the server and visit `http://127.0.0.1:8000/scrap/`.

### 12.8 Run the application

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your web browser.

---

## 13. Application Routes

| URL | Purpose |
|-----|---------|
| `/` | Home page showing top-rated products |
| `/search/` | Smart semantic search (BERT) |
| `/formalsearch/?query=<text>` | Keyword search (spaCy) |
| `/category/<name>/` | Products filtered by category |
| `/scrap/` | Starts the web scraper |
| `/about-us/` | About page |
| `/contact-us/` | Contact page |
| `/admin/` | Django administration panel |

---

## 14. Limitations

- **Static embeddings:** Product embeddings are precomputed, so newly scraped products only appear in smart search after the embeddings are regenerated.
- **Website changes:** The scraper depends on each website's current HTML structure and needs updating if a site changes its layout.
- **Text-only matching:** Search uses only product titles. Images and full product descriptions are not used.
- **General-purpose model:** `bert-base-uncased` was trained on general English text and was not fine-tuned on e-commerce data.
- **Data types:** Numeric fields such as price and rating are stored as text, which limits numeric sorting and filtering.

---

## 15. Future Work

1. **Fine-tune BERT, or use Sentence-BERT (SBERT),** on e-commerce product data to produce more accurate embeddings.
2. Use a **vector database** (such as FAISS) for fast similarity search over large product catalogues.
3. Add **multimodal search** that combines text and product images (for example with CLIP).
4. Build **personalised recommendations** based on user behaviour and preferences.
5. Add **scheduled scraping** with automatic embedding updates.
6. Add **price comparison and filtering**, with properly typed numeric fields.
7. **Evaluate search quality** with standard information-retrieval metrics such as Precision@K, Recall@K and NDCG.
8. **Deploy** the application to a cloud platform with production-grade security settings.

---

## 16. Learning Outcomes

Through this project, I gained practical experience in:

- Building full-stack web applications with **Django** and the MVT architecture
- Designing and running **web scrapers** for dynamic, JavaScript-rendered websites
- Applying **transformer-based deep learning models** (BERT) to real-world problems
- Using **NLP techniques** such as tokenization, stop-word removal and keyword extraction
- Implementing **vector similarity search** with cosine similarity
- Designing **relational databases** and working with an ORM
- Covering the full process from **data collection** to a working, user-facing application

---

## 17. Author

**[Your Full Name]**
[Degree Program], [University Name]
Email: [your.email@example.com]
LinkedIn: [linkedin.com/in/your-profile]
GitHub: [github.com/your-username]

**Supervisor:** [Supervisor Name], [Department]

---

## 18. License

This project was developed for **educational and academic purposes**. Product data belongs to the original marketplaces (Daraz.pk and Etsy) and was collected only for research and demonstration.
