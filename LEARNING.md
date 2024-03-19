# Intro 
This file is intended to be a collection of articles and videos that can help new developers get started 
    working on YACS, specifically for webscraping. These are some resources I found useful when I began
    as a developer with no experience in webscraping or any sort of backend development experience. 

As of right now, under each subsection there is not much information regarding each concept/library as 
    there are links in the bibliography that refer to each item with its necessary information. But as the 
    semester progresses, I can add information for each bulletpoint and expand on what to look
    out for specifically when beginning to understand and use each concept/library in YACS 
    development for the purposes of webscraping.

# Important Concepts
Python API:


RegEx:


XML:

    The code script interacts with XML data provided by the YACS API. For instance, in the `get_current_catalog_id()` 
    function, the response from the YACS API is parsed using the `etree.parse()` method from the `lxml` library, 
    allowing the script to extract the current catalog ID from the XML response.

    # XML Prolog
    - The `XML_prolog` variable in the code script stores the XML prolog, which is an optional declaration that specifies the XML version and encoding used in the document.        In the context of the provided code, the `XML_prolog` is extracted from the XML response obtained from the YACS API. It ensures that the XML document is well-formed          and provides essential information about the document's encoding and version.

    # Catalog Root
    - The `catalog_root` variable in the code script represents the root element of the XML response obtained from the YACS API. In XML terminology, the root element is the 
      top-level element that encloses all other elements in the XML document. In the provided code, `catalog_root` encapsulates all the course-related information retrieved        from the YACS API, including course details such as name, description, prerequisites, etc.

    # Catalog Detail Endpoint
    - The `catalog_detail_endpoint` variable in the code script represents the endpoint URL for retrieving detailed catalog information from the YACS API. This endpoint is 
      used to fetch data about the available catalogs, including the current catalog ID, which is necessary for further API requests. In the `get_current_catalog_id()` 
      function, an HTTP GET request is made to this endpoint to obtain information about the current catalog, such as its ID.


# Important Python Packages/Libraries
BeautifulSoup:


LXML:


ElementTree:


# Miscellaneous 
Threading in Python:




# Annotated Bibliography
“Beautiful Soup Documentation¶.” Beautiful Soup Documentation - Beautiful Soup 4.12.0 Documentation, 
        www.crummy.com/software/BeautifulSoup/bs4/doc/. Accessed 14 Mar. 2024. 
        
Grupman, Celeste. “Python API Tutorial: Getting Started with Apis.” Dataquest, 9 Apr. 2023, 
        www.dataquest.io/blog/python-api-tutorial/. 

Howson, Steph. “Python XML Tutorial: Element Tree Parse & Read.” DataCamp, DataCamp, 6 Mar. 2018, 
        www.datacamp.com/tutorial/python-xml-elementtree. 
        
“An Intro to Threading in Python.” Real Python, Real Python, 22 May 2022, 
        realpython.com/intro-to-python-threading/. 
        
“An Introduction to Selenium with Python.” Simplilearn.Com, Simplilearn, 28 Feb. 2023, 
        www.simplilearn.com/tutorials/python-tutorial/selenium-with-python. 

“Universal Lxml Tutorial for Beginners and Pros.” Universal Lxml Tutorial for Beginners and Pros, 
        oxylabs.io/blog/lxml-tutorial. Accessed 18 Mar. 2024. 

“Web Scraping with Regex.” Web Scraping with RegEx, oxylabs.io/blog/regex-web-scraping. Accessed 18 
        Mar. 2024. 
        
“What Is an Application Programming Interface (API)?” IBM, www.ibm.com/topics/api. Accessed 14 Mar. 2024. 

“What Is XML | XML Beginner Tutorial | Learn XML with Demo in 10 Min.” YouTube, YouTube, 17 Nov. 2020, 
        www.youtube.com/watch?v=1JblVElt5K0&pp=ygUEeG1sIA%3D%3D. 
        
“Xml.Etree.ElementTree - The Elementtree XML API.” Python Documentation, 
        docs.python.org/3/library/xml.etree.elementtree.html. Accessed 14 Mar. 2024. 
