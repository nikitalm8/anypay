import httpx
import hashlib

from .models import (
    Bill, 
    Payment, 
    Payout, 
    Rates,
)
from .exceptions import (
    AnyPayAPIError, 
    error_check, 
    error_check_async,
)


class AnyPayAPI:
    """
    AnyPay API wrapper.
    Docs: https://anypay.io/doc/api/
    """
    
    API_URL = 'https://anypay.io/api/%s/%s'
    HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'multipart/form-data',
    }


    def __init__(
        self, 
        api_id: str, 
        api_key: str, 
        project_id: int | None, 
        use_md5: bool=False,
        no_check: bool=False,
    ) -> None:
        """
        Initialize AnyPay API wrapper.
        
        :param api_id: API ID, can be found in your profile settings.
        :param api_key: API Key, can be found in your profile settings.
        :param project_id: Project ID, can be found in your project settings.
        :param use_md5: Use MD5 signature instead of SHA256 (change to MD5 in settings).
        :param no_check: Disable API ID and API Key check.

        :raises: AnyPayAPIError if API ID or API Key is invalid. 
        """

        self.api_id = api_id
        self.api_key = api_key

        self.project_id = project_id

        self.use_md5 = use_md5
        self.session = httpx.AsyncClient(
            headers=self.HEADERS,
            timeout=60,
        )

        if not no_check:

            self._make_request('balance')


    def _form_signature(self, method: str, template: str, params: dict, use_md5: bool=False) -> str:
        """
        Form signature for AnyPay API.
        """

        encryption_method = hashlib.sha256 if not use_md5 else hashlib.md5
        signature = encryption_method(
            (
                method 
                + self.api_id 
                + template % params 
                + self.api_key
            ).encode('utf-8'),
        )

        return signature.hexdigest()


    @error_check
    def _make_request(self, endpoint: str, sign_template: str='', **params) -> dict:
        """
        Make request to AnyPay API (sync).
        """

        response = httpx.get(
            self.API_URL % (
                endpoint,
                self.api_id,
            ),
            params={
                'sign': self._form_signature(
                    endpoint, sign_template, params, self.use_md5,
                ),
                **{
                    key: value
                    for key, value in params.items()
                    if value is not None
                },
            },
            headers=self.HEADERS,
            timeout=60,
        )
        
        return response.json()


    @error_check_async
    async def _make_request_async(self, endpoint: str, sign_template: str='', **params) -> dict:
        """
        Make request to AnyPay API (async).
        """

        response = await self.session.get(
            self.API_URL % (
                endpoint,
                self.api_id,
            ),
            params={
                'sign': self._form_signature(
                    endpoint, sign_template, params, self.use_md5,
                ),
                **{
                    key: value
                    for key, value in params.items()
                    if value is not None
                },
            },
        )

        return response.json()


    async def get_balance(self) -> float | int:
        """
        Get balance.
        Docs: https://anypay.io/doc/api/balance

        :return: Balance.
        :raises: AnyPayAPIError
        """

        response = await self._make_request_async('balance')

        return response['result']['balance']


    async def get_convertion_rates(self) -> Rates:
        """
        Get convertion rates.
        Docs: https://anypay.io/doc/api/rates
        
        :return: Rates object.
        :raises: AnyPayAPIError
        """

        response = await self._make_request_async('rates')

        return Rates(**response['result'])


    async def get_commissions(self, project_id: int | None=None) -> dict:
        """
        Get commissions.
        Docs: https://anypay.io/doc/api/commissions
         
        :param project_id: Project ID, can be found in your project settings.  

        :return: Commissions object.
        :raises: AnyPayAPIError
        """

        response = await self._make_request_async(
            'commissions',
            '%(project_id)s',
            project_id=project_id or self.project_id,
        )

        return response['result']


    async def create_payment(
        self, 
        pay_id: int,
        amount: float,
        email: str,
        method: str,
        project_id: int | None = None,
        currency: str='RUB',
        desc: str='',
        method_currency: str = None,
        phone: str = None,
        tail: str = None,
        success_url: str = None,
        fail_url: str = None,
        lang: str = None,
    ) -> Bill:
        """
        Create a payout.
        Docs: https://anypay.io/doc/api/create-payment
        
        :param pay_id: Payment ID.
        :param amount: Payment amount.
        :param email: User email.
        :param method: Payment method.
        :param project_id: Project ID.
        :param currency: Payment currency.
        :param desc: Payment description.
        :param method_currency: Payment method currency.
        :param phone: User phone.
        :param tail: Payment tail (for `card` payment method).
        :param success_url: Success URL.
        :param fail_url: Fail URL.
        :param lang: Bill page language.
        
        :return: Payout object.
        :raises: AnyPayAPIError
        """

        response = await self._make_request_async(
            self.API_URL,
            'create-payment',
            '%(project_id)s%(amount)s%(currency)s%(desc)s%(method)s',
            project_id=project_id or self.project_id,
            pay_id=pay_id,
            amount=amount,
            currency=currency,
            desc=desc,
            method=method,
            method_currency=method_currency,
            email=email,
            phone=phone,
            tail=tail,
            success_url=success_url,
            fail_url=fail_url,
            lang=lang,
        )

        return Bill(**response['result'])


    async def get_payments(
        self,
        project_id: int | None=None,
        transaction_id: int | None=None,
        pay_id: int | None=None,
        offset: int=0,
    ) -> list[Payment]:
        """
        Get payments.
        Docs: https://anypay.io/doc/api/payments
        
        :param project_id: Project ID, can be found in your project settings.
        :param transaction_id: Transaction ID.
        :param pay_id: Payment ID.
        :param offset: Offset (defaults to 0).

        :return: List of Payment objects.
        :raises: AnyPayAPIError
        """

        response = await self._make_request_async(
            'payments',
            '%(project_id)s',
            project_id=project_id or self.project_id,
            transaction_id=transaction_id,
            pay_id=pay_id,
            offset=offset,
        )

        return [
            Payment(**payment)
            for payment
            in response['result']['payments'].values()
        ]


    async def create_payout(
        self,
        payout_id: int,
        payout_type: str,
        amount: float,
        wallet: str,
        wallet_currency: str | None=None,
        commission_type: str | None=None,
        status_url: str | None=None,
    ) -> Payout:
        """
        Create a payout.
        Docs: https://anypay.io/doc/api/create-payout
        
        :param payout_id: Payout ID.
        :param payout_type: Payout type (qiwi, ym, ...).
        :param amount: Amount.
        :param wallet: Wallet number.
        :param wallet_currency: Wallet currency (defaults to RUB).
        :param commission_type: From where to deduct the commission (payment or balance).
        :param status_url: Status URL (Optional).
        
        :return: Payout object.
        :raises: AnyPayAPIError
        """

        response = await self._make_request_async(
            'create-payout',
            '%(payout_id)s%(payout_type)s%(amount)s%(wallet)s',
            payout_id=payout_id,
            payout_type=payout_type,
            amount=amount,
            wallet=wallet,
            wallet_currency=wallet_currency,
            commission_type=commission_type,
            status_url=status_url,
        )

        return Payout(**response['result'])


    async def get_payouts(
        self,
        transaction_id: int | None=None,
        payout_id: int | None=None,
        offset: int=0,
    ) -> list[Payout]:
        """
        Get payouts.
        Docs: https://anypay.io/doc/api/payouts
        
        :param transaction_id: Transaction ID.
        :param payout_id: Payout ID.
        :param offset: Offset (defaults to 0).

        :return: List of Payout objects.
        :raises: AnyPayAPIError
        """

        response = await self._make_request_async(
            'payouts',
            transaction_id=transaction_id,
            payout_id=payout_id,
            offset=offset,
        )

        return [
            Payout(**payout)
            for payout 
            in response['result']['payouts'].values()
        ]



    async def get_service_ip(self) -> list[str]:

        response = await self._make_request_async('ip-notification')

        return response['result']
