# Skincare Products Recommendation System

![](https://i.imgur.com/TZqYxAH.png)


### I. Introduction:
#### Dataset: Sephora
* Product's name
* Description 
* Brand 
* Ingredients
* Category
* Average rating 
* Number of recommendation
* Start's count.

#### Progress: 
*Prediction on product ratings and recommendation based on product's profiles, product description, ingredients.*
1. Scraping data from Sephora's website.
2. Using Sentiment Analysis - to process review's score and recommends products with the top 5 highest cosine similarity score. (reviews for face products)
3. Dataset is collected by Scrapy, dataprocessing.
4. Build the recommendation system.


![](https://i.imgur.com/csht248.jpg)


### II. Scraping data:
*Implement a recommendation system based on review contents from different skincare's products.*
* Parsing Sephora's HTML using the BeautifulSoup Module
* Find all categories in SHOP then scrape all products in Skincare category as well as information in reviews 

### III. Sentiment Analysis:
* Counts the number of stars (user's rating) to analyse the quality of the products.

![](https://i.imgur.com/rDvivHj.png)


### IV. Build a recommendation system:
1. Skin type (Oily, Dry, Sensitive, Combination, Normal)
2. Skin tone (Light, Dark, Porcelain ...)
3. Age range (18-22, 30-40,...)

<img src="https://i.imgur.com/qa88RSg.png" alt="drawing" width="450"/>

<img src="https://i.imgur.com/IGWRHgq.png" alt="drawing" width="450"/>

<img src="https://i.imgur.com/NrdH6zs.png" alt="drawing" width="450"/>

* The recommendation system calculates a cosine similarity score then comparing items with cosine similarity. 
* Finally, the system regulates the top 5 products with highest cosine similarity.


