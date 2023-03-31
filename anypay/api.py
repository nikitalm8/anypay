import httpx
import hashlib

from .models import (
    Bill, 
    Payment, 
    Payout, 
    Rates,
)
from .exceptions import AnyPayAPIError

from typing import Union, Optional, List


class AnyPayAPI(object):
    """
    AnyPay API wrapper.
    Docs: https://anypay.io/doc/api
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
        project_id: Optional[int]=None, 
        project_secret: Optional[str]=None,
        use_md5: bool=False,
        check: bool=True,
    ):
        """
        Initialize AnyPay API wrapper.

        :param api_id: API ID, can be found in your profile settings.
        :param api_key: API Key, can be found in your profile settings.
        :param project_id: Project ID, can be found in your project settings.
        :param project_secret: Project Secret, can be found in your project settings. Add it if you need to use SCI.
        :param use_md5: Use MD5 signature instead of SHA256 (change to MD5 in settings).
        :param check: Disable API ID and API Key check.

        :raises: AnyPayAPIError if API ID or API Key is invalid. 
        """

        self.api_id = api_id
        self.api_key = api_key

        self.project_id = project_id
        self.project_secret = project_secret

        self.use_md5 = use_md5
        self.session = httpx.AsyncClient(headers=self.HEADERS, timeout=60)

        if check:

            # Check API ID and API Key by making request to `ip-notification` endpoint
            self._make_request('ip-notification')


    def _form_signature(self, method: str, template: str, params: dict, use_md5: bool=False) -> str:
        """
        Form signature for AnyPay API.

        :param method: API method (endpoint).
        :param template: Template for signature.
        :param params: Request params.
        :param use_md5: Use MD5 signature instead of SHA256 (change to MD5 in project settings).

        :return: Encoded signature string.
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


    @staticmethod
    def _check_response(response: dict) -> None:
        """
        Method for checking for errors in responses.
        If there is an `error` key in the response, raises an AnyPayAPIError.

        :param response: Response data.

        :raises: AnyPayAPIError.
        """

        if 'error' in response:

            raise AnyPayAPIError(response['error'])


    def _make_request(self, endpoint: str, sign_template: str='', **params) -> dict:
        """
        Make request to AnyPay API (sync).

        :param endpoint: API endpoint.
        :param sign_template: Template for signature.
        :param params: Request params.

        :return: Response data.
        :raises: AnyPayAPIError.
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

        response = response.json()
        self._check_response(response)

        return response['result']


    async def _make_request_async(self, endpoint: str, sign_template: str='', **params) -> dict:
        """
        Make request to AnyPay API (async).

        :param endpoint: API endpoint.
        :param sign_template: Template for signature.
        :param params: Request params.

        :return: Response data.
        :raises: AnyPayAPIError.
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

        response = response.json()
        self._check_response(response)

        return response['result']


    async def get_balance(self) -> Union[float, int]:
        """
        Get balance.
        Docs: https://anypay.io/doc/api/balance

        :return: Balance.
        :raises: AnyPayAPIError
        """

        result = await self._make_request_async('balance')
        return result['balance']

    
    @property
    def balance(self) -> Union[float, int]:
        """
        Get balance.
        Docs: https://anypay.io/doc/api/balance
        
        :return: Balance.
        :raises: AnyPayAPIError
        """

        result = self._make_request('balance')
        return result['balance']


    async def get_convertion_rates(self) -> Rates:
        """
        Get convertion rates.
        Docs: https://anypay.io/doc/api/rates
        
        :return: Rates object.
        :raises: AnyPayAPIError
        """

        result = await self._make_request_async('rates')
        return Rates(**result)


    @property
    def convertion_rates(self) -> Rates:
        """
        Get convertion rates from property. Synchronous.
        Docs: https://anypay.io/doc/api/rates
        
        :return: Rates object.
        :raises: AnyPayAPIError
        """


        result = self._make_request('rates')
        return Rates(**result)


    async def get_commissions(self, project_id: Optional[int]=None) -> dict:
        """
        Get commissions.
        Docs: https://anypay.io/doc/api/commissions
         
        :param project_id: Project ID, can be found in your project settings.  

        :return: Commissions object.
        :raises: AnyPayAPIError
        """

        result = await self._make_request_async(
            'commissions',
            '%(project_id)s',
            project_id=project_id or self.project_id,
        )
        return result


    @property
    def commissions(self) -> dict:
        """
        Get commissions from property. Synchronous.
        Docs: https://anypay.io/doc/api/commissions
        
        :return: Commissions object.
        :raises: AnyPayAPIError
        """

        result = self._make_request(
            'commissions',
            '%(project_id)s',
            project_id=self.project_id,
        )
        return result


    async def create_payment(
        self, 
        pay_id: int,
        amount: float,
        email: str,
        method: str,
        project_id: Optional[int] = None,
        currency: str='RUB',
        desc: str='',
        method_currency: Optional[str]=None,
        phone: Optional[str]=None,
        tail: Optional[str]=None,
        success_url: Optional[str]=None,
        fail_url: Optional[str]=None,
        lang: Optional[str]=None,
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

        result = await self._make_request_async(
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
        return Bill(**result)


    async def get_payments(
        self,
        project_id: Optional[int]=None,
        transaction_id: Optional[int]=None,
        pay_id: Optional[int]=None,
        offset: int=0,
    ) -> List[Payment]:
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

        result = await self._make_request_async(
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
            in result['payments'].values()
        ] if result['payments'] else []


    async def create_payout(
        self,
        payout_id: int,
        payout_type: str,
        amount: float,
        wallet: str,
        wallet_currency: Optional[str]=None,
        commission_type: Optional[str]=None,
        status_url: Optional[str]=None,
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

        result = await self._make_request_async(
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

        return Payout(**result)


    async def get_payouts(
        self,
        transaction_id: Optional[int]=None,
        payout_id: Optional[int]=None,
        offset: int=0,
    ) -> List[Payout]:
        """
        Get payouts.
        Docs: https://anypay.io/doc/api/payouts
        
        :param transaction_id: Transaction ID.
        :param payout_id: Payout ID.
        :param offset: Offset (defaults to 0).

        :return: List of Payout objects.
        :raises: AnyPayAPIError
        """

        result = await self._make_request_async(
            'payouts',
            transaction_id=transaction_id,
            payout_id=payout_id,
            offset=offset,
        )

        return [
            Payout(**payout)
            for payout 
            in result['payouts'].values()
        ] if result['payouts'] else []


    async def get_service_ip(self) -> List[str]:
        """
        Get service IPs.
        Docs: https://anypay.io/doc/api/ip

        :return: List of service IPs.
        :raises: AnyPayAPIError
        """

        return await self._make_request_async('ip-notification')


    @property
    def service_ip(self) -> List[str]:
        """
        Get service IPs via property. Synchronous.
        Docs: https://anypay.io/doc/api/ip

        :return: List of service IPs.
        :raises: AnyPayAPIError
        """

        return self._make_request('ip-notification')


    async def create_bill(
        self, 
        pay_id: int,
        amount: Union[int, float],
        project_id: Optional[int]=None,
        project_secret: Optional[str]=None,
        currency: str='RUB',
        description: str='Payment',
        method: Optional[str]=None,
        email: Optional[str]=None,
        phone: Optional[str]=None,
        success_url: Optional[str]=None,
        fail_url: Optional[str]=None,
        lang: Optional[str]=None,
        use_md5: bool=True,
        **kwargs,
    ) -> Bill:
        """
        Create a bill via eased up SCI methods (only pay_id, amount, project_id and project_secret are required).
        Note that this method does not raise an exception if the credentials are incorrect, the exception is show to user on the bill's page.
        
        Docs: https://anypay.io/doc/sci/

        :param pay_id: Payment ID.
        :param amount: Payment amount.
        :param project_id: Project ID, can be added in __init__.
        :param project_secret: Project secret key, can be added in __init__.
        :param currency: Payment currency.
        :param description: Payment description.
        :param method: Payment method.
        :param email: User email.
        :param phone: User phone.
        :param success_url: Success URL.
        :param fail_url: Fail URL.
        :param lang: Bill page language.
        :param use_md5: Use MD5 (defaults to True).

        :return: Bill object.
        """
    
        if use_md5:

            singature_string = '%s:%s:%s:%s:%s' % (
                currency,
                amount,
                project_secret or self.project_secret,
                project_id or self.project_id,
                pay_id,
            )
            signature = hashlib.md5(
                singature_string.encode('utf-8'),
            ).hexdigest()

        else:

            signature_string = '%s:%s:%s:%s:%s:%s:%s:%s' % (
                project_id or self.project_id,
                pay_id,
                amount,
                currency,
                description,
                success_url,
                fail_url,
                project_secret or self.project_secret,
            )
            signature = hashlib.sha256(
                signature_string.encode('utf-8'),
            ).hexdigest()

        params = {
            'merchant_id': project_id or self.project_id,
            'pay_id': pay_id,
            'amount': amount,
            'currency': currency,
            'desc': description,
            'method': method,
            'email': email,
            'phone': phone,
            'success_url': success_url,
            'fail_url': fail_url,
            'lang': lang,
            'sign': signature,
            **kwargs,
        }
        response = await self.session.get(
            'https://anypay.io/merchant',
            params={
                key: value
                for key, value
                in params.items()
                if value is not None
            },
        )

        return Bill(pay_id=pay_id, payment_url=str(response.url))
