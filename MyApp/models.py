from datetime import date
from django.db import models

# Create your models here.

class Mentor:
    fname : str
    lname : str
    exp : int
    domain_name : str
    current_company : str
    email : str
    linkedin : str
    rating : int


class Startup:
    company_name : str
    age : int
    domain : str
    emps : int
    descp :str
    poc : str
    poc_email : str
    email : str
    linkedin : str
    website : str

class Queries:
    query_id : int
    company_name : str
    email : str
    query_date : date

class Suggestion:
    query_id : int
    suggestion : str

class Goals:
    email : str
    goals : str    



