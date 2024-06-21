# Bookommender - Backend

## Endpoints

You can find the Spec with all endpoint of the Bookommender backend in [./spec/bookommender.yml](./spec/bookommender.yml).

Endpoint Swagger UI: http://localhost:8055/docs

### Endpoint /recommendItems

Provide either:

- **userId**: uses the FM recommend method
- **itemId**: uses the FM similiarItems method
- **age (>=5, <=100) and locationCountry**: uses similar users and FM recommendations
- **fallback**: returns items from our most and least popular baseline

Supported Users: all users ids from the `./app/books/BX-Book-Ratings-cleaned.csv` are supported.

## Search

For the search we use ElasticSearch with a Fuzzy Search on

- Book Title with weight 5
- Excerpt with weight 3
- Author with weight 1

and a Fuziness of 2.0.

## Get Started

- `pip install -r requirements.txt` → Install dependencies
- or manually install packages: `pip install fastapi` & `pip install "uvicorn[standard]"`
- `uvicorn app.main:app --reload` → Start development server

## Docker

- `docker build -t bookommender-b .`
- `docker run -d -p 80:80 bookommender-b`
