# Mission-to-Mars

## Overview
Robin is a data analyst whose dream is to work for Nasa. She is passionate about space and is an afficcionado of the Mission to Mars! Because of such devotion, she wants to put together a website where she keeps all the most recent information about that planet, web-scraping from a number of websites.

## Purpose/Technical Details
The purpose of this project is to "web-scrape" or, in other words, create an automated process to acquire information in the web. The page created was simple, but there were many elements involved.

Websites scraped:
- https://redplanetscience.com: latest news acquisition
- https://spaceimages-mars.com: image from Mars
- https://galaxyfacts-mars.com: table comparing Mars and Earth
- https://marshemispheres.com: images from all four Mars hemispheres

On the technical side, a few relavant points need to be addressed:
- Use of Flask library to create a web server that will receive the requests and deliver the correct webpage;
- Use of BeautifulSoup library to parse Html in the different sites used as source;
- Use of webdriver_manager.chrome as the browser used to web-scrape;
- Use of PyMongo to store data in MongoDB.

## So how did it work?
- A webserver (flask) was created to answer client requests and it had two tasks:
  * Send to the client what was stored in the database upon request;
  * Update the data with the latest information - visiting, thus, all the websites and repeating the web-scraping process.

- A index.html file - file returned by the web server to the client whenever a request was received at localhost;

- A scraping.py with functions to scrape data from the various websites - the webserver would call one main function and this one, in its turn, would call several other functions used for the entire scraping process;

## Considerations
The webscraping process was successful: we were able to identify precisely the points where to get the information with BeautifulSoup. For that to make sense, though, we needed to automate the process - either manually, which was the case as the data was updated upon request, or automatically (in this case, the server could repeat the process from time to time by itself). Lastly, the scraped data was stored in MongoDB enabling the server to always show the latest information.

## Modifications
As part of the Challenge, we were requested to make two modifications using bootstrap. The following pictures show the before/after the changes, the changes were minor, but enough to give an idea how bootstrap works and what can be done (very easily).

![JumbotronInitial](/resources/JumbotronInitial.jpg)

![JumbotronFinal](/resources/JumbotronFinal.jpg)

![MarsHemispheresInitial](/resources/MarsHemispheresInitial.jpg)

![MarsHemispheresFinal](/resources/MarsHemispheresFinal.jpg)


