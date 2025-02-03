# Web Scraping and Academic Data Management Project

## Overview
This project is focused on developing a web-based system that allows users to scrape academic data from Google Scholar, store the data in a **MongoDB** database, and display the data through an interactive web interface. The project also explores the integration of **Elasticsearch** for advanced query functionalities, although technical issues prevented its implementation.

## Table of Contents
- [Overview](#overview)
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Database Design](#database-design)
- [Web Scraping Process](#web-scraping-process)
- [Web Interface](#web-interface)
- [Experimental Results](#experimental-results)
- [Screenshots](#screenshots)
- [References](#references)

## Introduction
This project involves:
1. Scraping academic publication data from **Google Scholar** using web scraping techniques.
2. Storing the scraped data in a **MongoDB** database.
3. Developing a user-friendly web interface for searching, filtering, and viewing the data.
4. Attempting to use **Elasticsearch** for querying but encountering challenges.

The primary goals of this project include:
- Learning web scraping techniques.
- Understanding NoSQL databases such as MongoDB.
- Gaining experience with Python-based web frameworks like Flask.
- Building an intuitive web interface for data management and visualization.

## Technologies Used
- **Programming Language:** Python
- **Database:** MongoDB (NoSQL)
- **Web Framework:** Flask
- **Web Scraping Library:** BeautifulSoup
- **Frontend Technologies:** HTML, CSS, JavaScript

## Features
1. **Web Scraping:**
   - Extract publication data from Google Scholar based on user-defined keywords.
   - Store scraped data into MongoDB collections.
2. **Data Storage and Management:**
   - Save publication details (e.g., title, authors, publication date) in a structured format.
   - Organize PDF files into designated folders.
3. **Web Interface:**
   - Display publications in a user-friendly format.
   - Allow keyword-based search and dynamic filtering.
   - Enable users to view publication details and navigate to source URLs.
4. **Dynamic Data Management:**
   - CRUD operations for managing stored data.
   - Synchronous updates using AJAX.

## Database Design
The database consists of the following collections:

1. **Publications:**
   - Fields: `title`, `authors`, `publication_date`, `type`, `url`, `keywords`
   - Indexed for efficient search and retrieval.

2. **Users:**
   - Fields: `username`, `password`, `role`
   - For managing access control (admin/user roles).

3. **Logs:**
   - Tracks scraping and user actions for debugging and analytics.

## Web Scraping Process
1. **Keyword Input:**
   - Users input keywords into a web interface.

2. **HTTP Request:**
   - Python sends HTTP GET requests to Google Scholar.

3. **HTML Parsing:**
   - BeautifulSoup extracts relevant information (title, authors, etc.).

4. **Data Cleaning:**
   - Unstructured data is formatted into MongoDB-compatible JSON.

5. **Data Storage:**
   - Cleaned data is inserted into the MongoDB database.

6. **File Handling:**
   - PDFs associated with publications are downloaded to a designated folder.

## Web Interface
1. **Framework:** Flask
2. **Functionalities:**
   - Search publications by keywords.
   - View details of each publication.
   - Navigate to external URLs for more information.
   - Dynamic filtering and sorting options.

3. **Pages:**
   - **[Search Page](images/web_interface_search.png):**
     - Input keywords to retrieve publication data.
   - **[Results Page](images/web_interface_results.png):**
     - View retrieved data in a table format.
   - **[Details Page](images/web_interface_details.png):**
     - Display comprehensive details about a publication.

## Experimental Results
1. Successfully implemented basic web scraping using Python and BeautifulSoup.
2. Developed a robust database structure in MongoDB.
3. Integrated scraped data with a functional Flask-based web interface.
4. Overcame challenges related to dynamic web scraping and data storage.
5. Encountered issues with Elasticsearch integration due to service errors, leading to the use of MongoDB for all database functionalities.

## Screenshots
### Database View
#### MongoDB Collections
![Database Screenshot 1](images/database_view_1.png)

#### Indexed Data Example
![Database Screenshot 2](images/database_view_2.png)

### Web Interface
#### Search and Results Page
![Web Interface 1](images/interface_search_results.png)


![Web Interface 2](images/interface_publication_details.png)


## References
1. [Stack Overflow](https://stackoverflow.com)
2. [Codes Cracker](https://codescracker.com)
3. [Coding Alpha](https://codingalpha.com)
4. [YouTube](https://youtube.com)
5. [GitHub](https://github.com)
6. School Friends
7. *C/C++ Programming Book*
