<div align="left">
    <h1>AnyPayAPI <img src="https://anypay.io/template/img/main/logo-start.svg" width=30 height=30></h1>
    <p align="left" >
        <a href="https://pypi.org/project/anypay/">
            <img src="https://img.shields.io/pypi/v/anypay?style=flat-square" alt="PyPI">
        </a>
        <a href="https://pypi.org/project/anypay/">
            <img src="https://img.shields.io/pypi/dm/anypay?style=flat-square" alt="PyPI">
        </a>
    </p>
</div>

A simple, yet powerful library for AnyPay [API](https://anypay.io/doc/api/)


## Usage

With ``AnyPayAPI`` you can easily create and retrieve payment and payout info, get informaition about your account's balance and commissions, etc.

## Documentation

Official docs can be found on the [API's webpage](https://anypay.io/doc/api/)

## Installation

```bash
pip install anypay
```

## Requirements

 - ``Python 3.9+``
 - ``httpx``
 - ``pydantic``

## Features

 - ``Asynchronous``
 - ``Exception handling``
 - ``Pydantic return model``
 - ``LightWeight``

## Basic example

```python
import asyncio

from anypay import AnyPayAPI, AnyPayAPIError


api = AnyPayAPI(
    'api_id', 'api_key', no_check=True # you can disable credentials check
) 


async def main():

    try:

        await api.get_balance()

    except AnyPayAPIError as exc:

        print(exc)

    payments = await api.get_payments(project_id=1) # project_id can be provided in __init__
    print(payments[0].id, payments[0].status)

    bill = await api.create_payment(
        pay_id=1234,
        project_id=1,
        method='qiwi',
        email='test@mail.ru',
        amount=100, 
        currency='RUB', 
        description='Test payment', 
    )
    print(bill.id, bill.url)

    bill = await api.create_bill( # easier way to create payment via SCI
        pay_id=1234,
        amount=100,
        project_id=1,
        project_secret='abcd',
    )
    print(bill.id, bill.url)


asyncio.run(main())
```

Developed by Nikita Minaev (c) 2023
