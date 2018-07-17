# API

|Method|URI|URL Params|Data Params|
|------|---|-----------|-----------|
| `POST` | /exchange/ |  | `{'currency_from': 'IDR' }` |
| `DELETE` | /exchange/{id}/ | `id=[integer]` |  |
| `POST` | /rate/ |  |  |
| `POST` | /rate-trace/ |  |  |


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
