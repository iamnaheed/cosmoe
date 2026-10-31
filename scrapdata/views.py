from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import json
import os
from django.core.paginator import Paginator
from .models import ProductRecord  
from django.shortcuts import render
from django.shortcuts import render
from .models import ProductRecord
import base64
from transformers import BertTokenizer, BertModel
from django.shortcuts import render
from django.http import JsonResponse
from .utils import search_products
from django.shortcuts import render, get_object_or_404

from .utils import recommend_products, filter_and_sort_products, product_data

def search_results(request):
    if request.method == 'POST':
        query = request.POST.get('queryInput', '')
        recommended_products = recommend_products(query, product_data)
        sorted_products = filter_and_sort_products(recommended_products, product_data)
        return render(request, 'search.html', {'sorted_products': sorted_products})
    else:
        return render(request, 'search.html', {'sorted_products': None})
    
def index(request):
    top_rated_products = ProductRecord.objects.order_by('-rating')
    paginator = Paginator(top_rated_products, 20)  # Show 20 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, "index.html", context)
# ____________________________aboutus_____________
def aboutus(request):
   return render(request, "about-us.html")


def contactus(request):
   return render(request, "contact-us.html")
# __________________________________formal query_____________

def formalsearch(request):
    query = request.GET.get('query', '')
    search_results = search_products(query)
    return render(request, 'formlsearch.html', {'search_results': search_results})

# ______________________________________________________________________________________
# _____________________________category______________________________
def category_view(request, category):
    products = ProductRecord.objects.filter(title__icontains=category)
    
    paginator = Paginator(products, 20)  # Show 20 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'category.html', context)


# ___________________________________________________________________-
def scrape(request):
    driver_path = ChromeDriverManager().install()
    urls = [
        "https://www.etsy.com/search/handmade?q=Home+Decor&explicit=1&locationQuery=1168579&item_type=handmade&ship_to=PK",
    ]
    with webdriver.Chrome(service=Service(driver_path)) as driver:
        for url in urls:
            for page_num in range(1,3):  # Scraping three pages
                driver.get(url + f"&page={page_num}")
                time.sleep(3)  # Add a delay to ensure the page is fully loaded
                
                # Get the HTML content of the page
                html_content = driver.page_source
                
                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                
                if "daraz.pk" in url:
                    # Daraz HTML structure
                    all_divs = soup.find_all('div', class_='gridItem--Yd0sa')
                    
                    for div in all_divs:
                        try:
                            # Extracting title
                            title_elem = div.find('div', class_='title-wrapper--IaQ0m')
                            exttitle = title_elem.text.strip() if title_elem else "N/A"

                            # Extracting rating
                            rating_elem = div.find('span', class_='ratig-num--KNake')
                            rating = rating_elem.text.strip() if rating_elem else "N/A"

                            # Extracting review count
                            review_elem = div.find('span', class_='rating__review--ygkUy')
                            review_count = review_elem.text.strip('()') if review_elem else "N/A"

                            # Extracting sold count
                            rating_div = div.find('div', id='id-rating')
                            if rating_div:
                                div_elements = rating_div.find_all('div')
                                sold_count = div_elements[-1].text.strip() if div_elements else "N/A"
                            else:
                                sold_count = "N/A"

                            # Extracting price
                            price_elem = div.find('span', class_='currency--GVKjl')
                            price = price_elem.text.strip() if price_elem else "N/A"

                            # Extracting href link
                            href_elem = div.find('a', id='id-a-link')
                            href = href_elem['href'] if href_elem else "N/A"
                            if href.startswith("//"):
                                href = "https:" + href

                            # Extracting image source
                            image_div = div.find('div', class_='image-wrapper--ydch1')
                            image_elem = image_div.find('img') if image_div else None
                            image_src = image_elem['src'] if image_elem else "N/A"

                            # If image source is in base64 format, decode it and store the URL
                            if image_src.startswith('data:image'):
                                driver.get(href)
                                time.sleep(3)  # Add a delay to ensure the page is fully loaded
                                html_content = driver.page_source
                                soup = BeautifulSoup(html_content, 'html.parser')
                                image_src = soup.find('img', class_='gallery-preview-panel__image')['src']

                            # Save data to the database
                            service = ProductRecord(title=exttitle, rating=rating, review_count=review_count, sold_count=sold_count, price=price, image_src=image_src, addtocart_href=href)
                            service.save()
                        except Exception as e:
                            print(f"Error occurred: {e}. Skipping this item.")
                elif "etsy.com" in url:
    # Etsy HTML structure
                    # Etsy HTML structure
                    all_li = soup.find_all('li', class_='wt-list-unstyled')

                    for li in all_li:
    # Extracting title
                        # title_elem = li.find('h3', class_='v2-listing-card__title wt-text-caption v2-listing-card__title')
                        # title = title_elem.text.strip() if title_elem else "N/A"
                        # print("Title:", title)
                        # Updated code
                      # Updated code
                        # Updated code
                        title_elem = soup.find('h3', class_='wt-text-caption v2-listing-card__title wt-text-truncate')
                        title = title_elem.get_text(strip=True) if title_elem else "N/A"
                        print("Title:", title)
                        

                        

    # Extracting price
                        price_elem = li.find('span', class_='currency-value')
                        price = price_elem.text.strip() if price_elem else "N/A"
                        print("Price:", price)

    # Extracting sold count
                        sold_count_elem = li.find('span', class_='wt-text-body-01')
                        sold_count = sold_count_elem.text.strip('()') if sold_count_elem else "N/A"
                        print("Sold Count:", sold_count)

    # Extracting image source
                        image_elem = li.find('img', class_='wt-width-full')
                        image_src = image_elem['src'] if image_elem else "N/A"
                        print("Image Source:", image_src)
                    
    # Extracting href link
                        href_elem = li.find('a', class_='listing-link')
                        href = href_elem['href'] if href_elem else "N/A"
                        print("Href Link:", href)

    # Extracting review count
                        rating_elem = li.find('div', {'role': 'img'})
                        rating_text = rating_elem['aria-label'] if rating_elem else "N/A"
                        rating, _, reviews = rating_text.partition(' with ')
                        rating = rating.split()[0] if rating else "N/A"  # Extract rating value
                        reviews = reviews.split()[0] if reviews else "N/A"  # Extract review count

                        print("Rating:", rating)
                        print("Review Count:", reviews)


    # Extracting rating
                        review_elem = li.find('span', class_='wt-text-body-01')
                        review_count = review_elem.text.strip('()') if review_elem else "N/A"
                        print("Review Count:", review_count)

    # Save data to the database
                        service = ProductRecord(title=title, rating=rating, review_count=reviews, sold_count=reviews, price=price, image_src=image_src, addtocart_href=href)
                        service.save()

# Move the return statement outside of the loop
            return HttpResponse('Scraping completed successfully!')
                    
