# API

**Add Foreign Exchange**
* **URL** <br/>
    `/foreignexchange/exchange/`
* **Method** <br/>
    `POST`
* **Data Params** <br/>
    * `from_currency=[integer]`
    * `to_currency=[integer]`
* **Success Response**
    * **Code:** 200 <br/>
      **Content:** `{'message': 'add exchange rate success'}`
* **Error Response**
    * **Code:** 400 <br/>
      **Content:** `{'__all__':'message for validation error'}`

**Delete Foreign Exchange**
* **URL** <br/>
    `/foreignexchange/exchange/{id}/`
* **Method** <br/>
    `DELETE`
* **URL Params** <br/>
    `id=[integer]`
* **Success Response** <br/>
    * **Code:** 200 <br/>
      **Content:** `{'message': 'delete exchange rate success'}`
* **Error Response** <br/>
    * **Code:** 400 <br/>
      **Content:** `{'__all__':'message for validation error'}`

**Add Daily Rate**
* **URL** <br/>
    `/foreignexchange/rate/`
* **Method** <br/>
    `POST`
* **Data Params** <br/>
    * `from_currency=[integer]`
    * `to_currency=[integer]`
    * `rate=[float]`
* **Success Response** <br/>
    * **Code:** 200 <br/>
      **Content:** `{'message': 'add daily rate success'}`
* **Error Response** <br/>
    * **Code:** 400 <br/>
      **Content:** `{'__all__':'message for validation error'}`

**Trace Rate**
* **URL** <br/>
    `/foreignexchange/rate-trace/`
* **Method** <br/>
    `POST`
* **Data Params** <br/>
    * `date=[date]` <br/>
    enter date format like `2018-07-20` , `07/20/2018` , `07/20/18`
* **Success Response** <br/>
    * **Code:** 200 <br/>
      **Content:** `{'result': [{'from': 'USD', 'to': 'IDR', 'rate': '14366.7', avg_rate:14296.7}]}`
* **Error Response** <br/>
    * **Code:** 400 <br/>
      **Content:** `{'__all__':'message for validation error'}`

# Database

**Currency**

```
+----+---------------+------------------------+
| id | currency_code |  Description           |
+----+---------------+------------------------+
|  1 |  IDR          | Indonesia Currency     |
|  2 |  USD          | United states Currency |
|  3 |  JPY          | Japan Currency         |
+----+---------------+------------------------+
```
The `Currency` table is used as master of table to store currency data.

**Exchange**
```
+----+---------------+--------------+
| id | from_currency |  to_currency |
+----+---------------+--------------+
|  1 |  2            |      1       |
|  2 |  2            |      3       |
+----+---------------+--------------+
```
The `Exchange` table is used to store currency exchange schema.
field `from_currency` and `to_currency` is `FOREIGN KEY` to table `Currency`

**Rate**
```
+----+----------+-----------+-----------+
| id | exchange | rate      + date      +
+----+----------+-----------+-----------+
|  1 |     1    |  14366.7  | 07/20/18  |
|  2 |     1    |  14201.2  | 07/18/18  |
|  3 |     1    |  14164.4  | 07/17/18  |
+----+----------+-----------+-----------+
```
The `Rate` table is used to store daily rate of foreign exchange.
field `exchange` is `FOREIGN KEY` to table `Exchange`


# Running the environment

You need to have Docker installed in your machine, after that, just run this command `docker-compose build && docker-compose up -d`.


# Testing

To make a testing run this command `docker-compose run web python3 manage.py test`
