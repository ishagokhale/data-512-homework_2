# data-512-homework_2

# Goal 
The goal of this assingment was to explore bias in datasets using Wikipedia articles through API requests. It was also important to consider how our own biases and judgement may affect the way we view data and conclusions. Additionally, we wanted to anlayze the countries and regions with the most and lest articles per capita and high quality articles per capita. 

# Data Sources and Licensing
The list of article titles was crawled from this Wikipedia page detailing politicians by country: https://en.wikipedia.org/wiki/Category:Politicians_by_nationality
 - This data was already crawled and given to us in the `politicians_by_country_AUG.2024.csv` file. 

The population data came from the world population datasheet by the Population Reference Bureau: https://www.prb.org/international/indicator/population/table/
 - This data was already given to us in the `population_by_country_AUG.2024.csv` file. 

I was able to access the wikipedia page information, particularly the last revision ID, through the wikimedia API, with documentation noted here: https://www.mediawiki.org/wiki/API:Info

Additionally, I accessed the article quality prediction through the ORES API, documentation linked here: https://www.mediawiki.org/wiki/ORES

I also used sample code in my notebook from Dr. David McDonald which is licensed through CC-BY, linked here:
https://creativecommons.org/licenses/by/4.0/

# Intermediate Files
`rev_id.csv`: File with article quality and last revision ID. It is an output file from a function in my notebook.  
`quality_pred.csv`: File with article quality and article quality prediction. It is an output file from `get_data.py`.  
`get_data.py`: Function to get the article quality prediction for each politician.  


# Output Files
`wp_politicians_by_country.csv`: Output CSV file with `article_title, region, country, population (in millions), quality prediction, and last revision ID` as columns.  
`wp_countries-no_match.txt`: Output txt file with countries do not have a match between the population data and article information data. The file lists the country names.  

# Research Implications

I have learned how to access the Wikimedia API, ORES API, and how to create my own API access token. Additionally, which countries and regions had the most articles per person. I was surprised that smaller countries (by size and population), such as Antigua and Barbuda and the Federated States of Micronesia had the two highest articles per capita ratio. In hindsight, given that they are smaller in population might make it easier for them to achieve a higher ratio as they would need fewer articles published than the larger countries, such as China or India. Thus, there might have been bias in my own preconceived notions that smaller countries (by population and size) would have less articles about their politicians.

1. Some biases I expected to find in the data before my analysis was that more affluent countries would have higher quality articles per capita. I presumed the more well developed countries would have more literate and higher educated writers, increasing the supply of high quality articles for that country. However, Montenegro, Luxembourg, and Albania were the countries I found with the top 3 high quality articles per capita. While Luxembourg is a pretty well developed country, I was surprised to see Montenegro and Albania there as they are still developing, highlighting my own biases I had before analyzing the data.

3. English Wikipedia as a source is very likely to be biased towards including only well known figures from English speaking countries. There might also be a preference to highlight figures more closely associated with western culture and not enough attention to the sciences or academia. Also, the contributors of English Wikipedia are going to be predominantly white, English speaking people. Therefore, their background may provide a westernized perspective of international political figures. 

7. A researcher might attempt to correct this by noting the background of the contributors for articles written about international figures and validate the cultural context. They could also take some time to cross reference articles to make sure the information is reliable, in addition to using the ORES quality prediction. Also, they could gather article data from non English wikipedia to diversify the sources to get a wider perspective on political figures and topics. 




