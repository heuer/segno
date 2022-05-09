from . import QRCode
import decimal
import datetime
from typing import Optional, Union, Iterable


def make_wifi_data(ssid: str, password: Optional[str], security: Optional[str],
                   hidden: bool = False) -> str: ...


def make_wifi(ssid: str, password: Optional[str], security: Optional[str],
              hidden: bool = False) -> QRCode: ...


def make_mecard_data(name: Union[str, Iterable[str]],
                     reading: Optional[str] = None,
                     email: Optional[Union[str, Iterable[str]]] = None,
                     phone: Optional[Union[str, Iterable[str]]] = None,
                     videophone: Optional[Union[str, Iterable[str]]] = None,
                     memo: Optional[str] = None,
                     nickname: Optional[str] = None,
                     birthday: Optional[Union[str, datetime.date]] = None,
                     url: Optional[Union[str, Iterable[str]]] = None,
                     pobox: Optional[str] = None,
                     roomno: Optional[str] = None,
                     houseno: Optional[str] = None,
                     city: Optional[str] = None,
                     prefecture: Optional[str] = None,
                     zipcode: Optional[str] = None,
                     country: Optional[str] = None) -> str: ...


def make_mecard(name: Union[str, Iterable[str]],
                reading: Optional[str] = None,
                email: Optional[Union[str, Iterable[str]]] = None,
                phone: Optional[Union[str, Iterable[str]]] = None,
                videophone: Optional[Union[str, Iterable[str]]] = None,
                memo: Optional[str] = None,
                nickname: Optional[str] = None,
                birthday: Optional[Union[str, datetime.date]] = None,
                url: Optional[Union[str, Iterable[str]]] = None,
                pobox: Optional[str] = None,
                roomno: Optional[str] = None,
                houseno: Optional[str] = None,
                city: Optional[str] = None,
                prefecture: Optional[str] = None,
                zipcode: Optional[str] = None,
                country: Optional[str] = None) -> QRCode: ...


def make_vcard_data(name: str, displayname: str,
                    email: Optional[Union[str, Iterable[str]]] = None,
                    phone: Optional[Union[str, Iterable[str]]] = None,
                    fax: Optional[Union[str, Iterable[str]]] = None,
                    videophone: Optional[Union[str, Iterable[str]]] = None,
                    memo: Optional[str] = None,
                    nickname: Optional[str] = None,
                    birthday: Optional[Union[str, datetime.date]] = None,
                    url: Optional[Union[str, Iterable[str]]] = None,
                    pobox: Optional[str] = None,
                    street: Optional[str] = None,
                    city: Optional[str] = None,
                    region: Optional[str] = None,
                    zipcode: Optional[str] = None,
                    country: Optional[str] = None,
                    org: Optional[str] = None,
                    lat: Optional[float] = None,
                    lng: Optional[float] = None,
                    source: Optional[str] = None,
                    rev: Optional[Union[str, datetime.date]] = None,
                    title: Optional[Union[str, Iterable[str]]] = None,
                    photo_uri: Optional[Union[str, Iterable[str]]] = None,
                    cellphone: Optional[Union[str, Iterable[str]]] = None,
                    homephone: Optional[Union[str, Iterable[str]]] = None,
                    workphone: Optional[Union[str, Iterable[str]]] = None) -> str: ...


def make_vcard(name: str, displayname: str,
               email: Optional[Union[str, Iterable[str]]] = None,
               phone: Optional[Union[str, Iterable[str]]] = None,
               fax: Optional[Union[str, Iterable[str]]] = None,
               videophone: Optional[Union[str, Iterable[str]]] = None,
               memo: Optional[str] = None,
               nickname: Optional[str] = None,
               birthday: Optional[Union[str, datetime.date]] = None,
               url: Optional[Union[str, Iterable[str]]] = None,
               pobox: Optional[str] = None,
               street: Optional[str] = None,
               city: Optional[str] = None,
               region: Optional[str] = None,
               zipcode: Optional[str] = None,
               country: Optional[str] = None,
               org: Optional[str] = None,
               lat: Optional[float] = None,
               lng: Optional[float] = None,
               source: Optional[str] = None,
               rev: Optional[Union[str, datetime.date]] = None,
               title: Optional[Union[str, Iterable[str]]] = None,
               photo_uri: Optional[Union[str, Iterable[str]]] = None,
               cellphone: Optional[Union[str, Iterable[str]]] = None,
               homephone: Optional[Union[str, Iterable[str]]] = None,
               workphone: Optional[Union[str, Iterable[str]]] = None) -> QRCode: ...


def make_geo_data(lat: float, lng: float) -> str: ...


def make_geo(lat: float, lng: float) -> QRCode: ...


def make_make_email_data(to: Union[str, Iterable[str]],
                         cc: Optional[Union[str, Iterable[str]]] = None,
                         bcc: Optional[Union[str, Iterable[str]]] = None,
                         subject: Optional[str] = None,
                         body: Optional[str] = None) -> str: ...


def make_email(to: Union[str, Iterable[str]],
               cc: Optional[Union[str, Iterable[str]]] = None,
               bcc: Optional[Union[str, Iterable[str]]] = None,
               subject: Optional[str] = None,
               body: Optional[str] = None) -> QRCode: ...


def make_epc_qr(name: str, iban: str, amount: Union[int, float, decimal.Decimal],
                text: Optional[str] = None,
                reference: Optional[str] = None,
                bic: Optional[str] = None,
                purpose: Optional[str] = None,
                encoding: Optional[Union[str, int]] = None) -> QRCode: ...
