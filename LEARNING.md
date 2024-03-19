# Intro 
This file is intended to be a collection of articles and videos that can help new developers get started 
    working on YACS, specifically for webscraping. These are some resources I found useful when I began
    as a developer with no experience in webscraping or any sort of backend development experience. 

As of right now, every subsection is not fully complete in regards to information for each concept. I 
    prioritized expanding on the concepts/libraries that took me longer to understand. Perhaps later,
    I can come back and add to each bulletpoint with equal amounts of information.

# Important Concepts
Python API:


RegEx:

    Regular expressions (RegEx) are employed in the code script to parse and extract specific information 
    from the raw course data obtained through web scraping. 

XML:

    The code script interacts with XML data provided by the YACS API. For instance, in the `get_current_catalog_id()` 
    function, the response from the YACS API is parsed using the `etree.parse()` method from the `lxml` library, 
    allowing the script to extract the current catalog ID from the XML response.

    XML Prolog
    - The `XML_prolog` variable in the code script stores the XML prolog, which is an optional declaration that 
    specifies the XML version and encoding used in the document. In the context of the provided code, the `XML_prolog` 
    is extracted from the XML response obtained from the YACS API. It ensures that the XML document is well-formed          
    and provides essential information about the document's encoding and version.

    Catalog Root
    - The `catalog_root` variable in the code script represents the root element of the XML response obtained from 
    the YACS API. In XML terminology, the root element is the top-level element that encloses all other elements 
    in the XML document. 

    Search Endpoint
    - The `search_endpoint` variable in the code script represents the endpoint URL for searching and retrieving 
    course information from the YACS API. This endpoint is used to search for and obtain a list of course IDs that
    match specific criteria, such as the current catalog, department, or level. 


# Important Python Packages/Libraries
BeautifulSoup:


LXML:


ElementTree:

    Once XML responses are obtained, the script constructs ElementTree objects to represent the hierarchical structure 
    of the XML documents. Each ElementTree corresponds to a parsed XML document, with elements representing nodes in 
    the XML tree and attributes representing properties of those nodes.

    XPath
    - XPath expressions can navigate through nested XML structures, allowing the script to access data at different 
    levels of hierarchy. This is particularly useful when dealing with complex XML documents containing nested 
    elements or multiple levels of nesting. For instance, in the get_all_courses() function, XPath is utilized to 
    traverse through the XML tree and extract course details from nested <field> elements within each <course> element.


# Miscellaneous 
Threading in Python:


Text Handling in HTTP Responses:

    Encoding and Decoding
    - Encoding converts a string into a sequence of bytes, while decoding converts a sequence of bytes 
    back into a string. This is essential for handling different character encodings encountered in HTTP 
    responses, ensuring that text data is correctly converted between bytes and strings.

    Cleaning UTF Characters
    - The 'clean_utf' function is utilized to normalize Unicode characters in the text data. Unicode characters 
    can have multiple representations, and normalization ensures that they are converted into a standardized 
    form. This process enhances consistency and uniformity in text data, making it easier to compare and 
    process strings.
    

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
