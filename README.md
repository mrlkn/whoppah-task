# Whoppah Second Hand Market 


## Table of Contents ->

1. [Installation and Setup](#installation-and-setup)
2. [Models](#Models)
3. [Serializers](#serializers)
4. [Views](#views)
5. [Transition Logic](#transition-logic)
6. [Tasks and Signals](#tasks-and-signals)
7. [Testing](#testing)
8. [Coding style and guide](#Coding-Style-Guide)

## Installation and setup

Create `.env` from the `.env-example`

Example `.env` file

```text
POSTGRES_USER=db
POSTGRES_PASSWORD=db
POSTGRES_DB=db
POSTGRES_HOST=whoppah_db
POSTGRES_PORT=5432
```
Then
```shell
docker-compose up --build
```
should do it.

## Models

- **AuditModel**
  - The `Base` model is an abstract base class that includes common fields like `created_by` and `last_updated_by`. Other models inherit from this base model.
- **Category Model** 
  - The `Category` model represents product categories. It contains a name and slug field. The slug field is automatically generated from the category name and is used in URLs. 
- **Product Model** 
  - The `Product` model represents products. It has fields for the title, category, and state. The state field represents the current state of the product (e.g. draft, new, rejected, banned, accepted). Products are also associated with categories through a ForeignKey relationship.

## Serializers

- **Base Serializer** 
  - This serializer adds `created_by` and `last_updated_by` fields to the serialized representation and is inherited by other serializers.
- **Category Serializer** 
  - Used for serializing Category instances. 
- **Product Serializer**
  - Used for serializing Product instances, including validation for state transitions.

## Views

- **Category View**
  - This view allows you to perform CRUD operations on categories. Only users with admin permissions can create, update, or delete categories. All users have read-only access. 
- **Product View**
  - This view allows you to perform CRUD operations on products. It also includes an additional endpoint for updating the state of a product. The state transition logic is applied during updates.

### OpenAPI specs and Redoc documentation

- `OpenAPI` specs can be found in here http://0.0.0.0:8000/swagger/

- `Redoc` specs can be found in here http://0.0.0.0:8000/redoc/

## Transition Logic

Products have different states and not all transitions between states are valid.

The `is_valid_transition` function in `utils.py` validates if a state transition is valid based on the user’s role (admin/creator) and the current state of the product. Currently, storing it as a basic dictionary which I would say not ideal but at this scale it solves it all.

I have implemented `State Machine` in order to handle transition better yet in this scale instead of helping, it created more complexity. On a real world application it can be more applicable.

## Tasks and Signals

### Tasks

The `send_email_task` is an asynchronous task that sends an email notification when the state of a product changes. It is executed by Celery and automatically retries in case of failure.

Again, on real world application I would implement a Notification Service that handles these emails but for single email requirement, I didn't even bother to get `from_who` from environment variable.

*To connect to Celery*
```shell
celery -A whoppah worker --loglevel=debug
```

### Signals

A signal is used to execute the `send_email_task` every time a product is saved. It checks if the state of the product has changed and if so, triggers the task to send an email notification to the product creator.

## Testing

Tests are located in the `tests` directory. They cover different aspects of the application including models, serializers, views, transition logic, and tasks.

In order to run the tests

```shell
./manage.py test product.tests 
```

*To be honest they are not that comprehensive.* 


**Coverage report** 
```text

Name                                   Stmts   Miss  Cover
----------------------------------------------------------
manage.py                                 12      2    83%
product/__init__.py                        0      0   100%
product/admin.py                           1      0   100%
product/apps.py                            6      0   100%
product/choices.py                         8      0   100%
product/custom_pagination.py               5      0   100%
product/migrations/0001_initial.py         8      0   100%
product/migrations/__init__.py             0      0   100%
product/models.py                         33      2    94%
product/permissions.py                     6      0   100%
product/serializers.py                    53      0   100%
product/signals.py                        12      0   100%
product/tasks.py                           7      2    71%
product/tests/__init__.py                  0      0   100%
product/tests/test_category_model.py      25      0   100%
product/tests/test_product_model.py       32      0   100%
product/tests/test_serializers.py         21      0   100%
product/tests/test_utils.py               31      0   100%
product/tests/test_views.py              104      0   100%
product/urls.py                            7      0   100%
product/utils.py                          21      0   100%
product/views.py                          31      2    94%
whoppah/__init__.py                        3      0   100%
whoppah/celery.py                          7      0   100%
whoppah/settings.py                       24      0   100%
whoppah/urls.py                            8      0   100%
----------------------------------------------------------
TOTAL                                    465      8    98%

```

## Coding Style Guide
List of the tools that has been used in the code.

- [Black](https://pypi.org/project/black/) as a linter.
- [isort](https://pycqa.github.io/isort/) for import optimization.
-  [mypy](https://mypy-lang.org/) for type hinting.


