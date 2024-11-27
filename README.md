# Expenses app

Django application that helps you manage and analyze your expenses.

## Prerequisites  
`Python =>3.10`

## Setup  
1. Clone the repository and CD into it's directory
```
git clone https://github.com/mykhailolisovyi/testproject.git
cd testproject
```
2. Create and activate virtualenv
```
python3 -m venv .venv
source .venv/bin/activate
```
3. Install required dependencies
```
pip install -r requirements.txt
```
4. Run django migrations:
```
python3 manage.py migrate
```
5. Run tests to ensure everything is OK:
```
python3 manage.py test
```
6. Start the application:
```
python3 manage.py runserver
```

## API Documentation
- `GET /expenses/`: List all expenses for the logged-in user.  
- `POST /expenses/`: Create a new expense.  
Request template:
```
{
    "user": "<user's username>",
    "title": "<expense's title>",
    "amount": "<expense's amount>",
    "date": "<date of expense occurrence in format "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]">",
    "category": "<name of one of available categories>"
}
```
Available categories: `Food`, `Travel`, `Utilities`, `Entertainment`, `Health`, `House`, `Other`.
- `GET /expenses/<id>/`: Retrieve details of a specific expense.  
- `PUT /expenses/<id>/`: Update a specific expense.  
Request template for updating a specific expense is the same as for creating an expense.  
- `DELETE /expenses/<id>/`: Delete a specific expense.  
- `GET /expenses/date-range/?username=<user's username>&start_date=<YYYY-MM-DDThh:mm>&end_date=<YYYY-MM-DDThh:mm>`: List expenses within a date range.  
All query parameters (`username`, `start_date`, `end_date`) are optional.  
If you don't specify `username` parameter, expenses for all users will be shown.  
If you don't specify one of `*_date` parameters expenses will be showed without constraints on that parameter.  
- `GET /expenses/category-summary/?username=<user's username>&year=<YYYY>&month=<MM>`: Get total expenses per category for a given year and month.  
All query parameters (`username`, `year`, `month`) are optional.  
If you don't specify `username` parameter, expenses for all users will be shown.  
If you don't specify `year`/`month` parameters then expenses for all years/months will be used to create
category summary.  
