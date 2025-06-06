**Overview**

Indian Startup Scraper is a simple Django-based full-stack project that aims to discover the latest job openings from career pages of Indian startups and other job portals.
It currently fetches job listings from the websites: Paytm, Shopclues, and Remotive.co.

For the back end, I have developed web scrapers for all 3 websites and they collect job data, clean it up, and save it to a database. This app includes a REST API that serves these listings with a manual trigger endpoint to scrape and store data. I have also added basic deduplication logic to maintain unique job posts. I also attempted date-based filtering but wasn’t fully able to implement it.

For the front end, I developed a webpage that allows users to search for jobs by title, company name, and location. The “All Open Positions” button takes users back to the homepage and refreshes all listings. I have kept the design minimal for now.
This website is fully deployed on Render and the link is: https://indian-startup-scraper.onrender.com/


**Tech Choices:**


*Backend*: 
I used Django with Python partly because it was one of the requirements but also because it allows the structuring of the backend and frontend in one place which keeps things efficient.

*Web Scraping*: 
I used ‘requests’ to obtain HTML content from websites and BeautifulSoup to parse and extract exact listings from the raw HTML.

*Database*: 
I used SQLite during local development for simplicity but went with PostgreSQL as the production database on Render deployment.

*Frontend*: 
I used basic Django templates and Bootstrap for styling.

*API*: 
I used the Django REST Framework for building REST API to allow triggering the scrapers. 

*Live Deployment*:
I deployed the website live using Render because it works well with Django




**Architecture**

The app follows a clean and minimal Django-based architecture as follows:

*Scrapers (jobs/all_scrapers/)*

This folder contains 3 Python scripts that act as individual scrapers for each job source (Remotive, Paytm, ShopClues). Each script fetches job listings, cleans the content (most needed for job descriptions), and returns structured data.

*Views (jobs/views.py)*

The views handle both the backend API logic and the frontend rendering:

- There’s an API endpoint that triggers the scrapers and saves the job data to the database.


- There’s a frontend view that shows jobs on the homepage and handles search filters like job title, location, and company name.


*API (jobs/urls.py)*

All routes are defined here. It connects:

- /api/run-scrapers/ — triggers the scraping logic.


- /api/jobs/ — returns job data in JSON format.


- / — serves the homepage with job listings.


*Templates (jobs/templates/)*

This folder holds the HTML template for the front-end page. 

*Models & Database*

Job data is saved in  Django model called JobPost. It includes all relevant fields like title, company, location, apply link, and job description. Basic deduplication is handled during data saving to avoid duplicate listings.

*Deployment*

The entire app is deployed on Render using PostgreSQL. Static files are served with WhiteNoise, and secret keys and database credentials are managed securely using environment variables.

**Local Setup and Run Instructions**

*Prerequisites*:

Python 3.9 or later
Git installed (optional)
Web Browser to view frontend

*Setup and Run Instructions*:


Use Git to clone the project and navigate to project’s directory:

git clone https://github.com/paridnyamane/Indian_Startup_Scraper.git

cd Indian_Startup_Scraper

1. Create a Virtual Environment:
   
python -m venv env

2. Activate the virtual environment:

env\Scripts\activate		&nbsp;&nbsp;#for Windows

source env/bin/activate		&nbsp;&nbsp;#for Linux

3. Install Dependencies:
   
pip install -r requirements.txt

5. Configure Environment Variables:
   
- If current .env file throws a "SECRET_KEY not found" after migrate:

  1. Generate a new Django SECRET_KEY:
     
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

  3. Create a .env file in the project root where ‘manage.py’ is present:
     
  - *Tip*:if .env is getting saved as .env.txt, fix: save as> ".env" should work.
    
  SECRET_KEY=your-secret-key	&nbsp;&nbsp;#paste the generated secret key
  DEBUG=True
  DATABASE_URL=sqlite:///db.sqlite3


5. Setup Database and Static Files:
   
python manage.py migrate		&nbsp;&nbsp;#apply db migrations

python manage.py collectstatic --noinput	#collect static files

7. Run Development Server:
   
python manage.py runserver

9. Visit http://127.0.0.1:8000/ in your browser

Manual Trigger for Scrapers via API(Optional):

-paste in command prompt while server is running:

curl -X POST http://127.0.0.1:8000/api/run-scrapers/


**What I’d like to improve if I had more time:**

*Better Date Scraping*: 

Currently, only the Remotive scraper exposes the actual job posting date. For other sites like Paytm and Shopclues, I'm using the scraping time as a fallback. With more time, I would explore ways to fetch or estimate the actual posted date more accurately.


*Additional Scraper Testing*:

Currently, the Scrapers are tested for limited test cases but if I had more time, I would have liked to add more test cases and perform quality testing.


*Pagination & Rate Limiting Support*:

The scrapers currently handle a single page per source. I would add code for paginated or infinite scroll job boards using Selenium and respect their rate limits with retries.


*Improved Filtering*:

I currently added job title, company, and location filters. But with more time, I would like to fine-tune them. I have attempted filter by date but on the front-end which doesn't run but I would like to make it functional with more time.


*Frontend Enhancements*:

I have kept the UI simple and clean on purpose, but I’d eventually like to improve responsiveness, add better loading states, and make the UI more functional and aesthetic. I would build the frontend with React.


*Automated Scraping*:

Currently, the scraper is manually triggered via an API. I would like to set up periodic and automatic scraping using Django-Q, if I have more time.


*Authentication for API Access*:

The API is open by design for now, but I would like to add basic token or admin-based authentication to make the system more secure in production.

*LLM Integration*:

I had planned to integrate an LLM to summarize job descriptions and extract tags, but didn’t get to do this yet. I would enjoy adding this feature to the website.





