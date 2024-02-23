from . import QRCode
import decimal
import datetime
from typing import Iterable


def make_wifi_data(ssid: str, password: str | None, security: str | None,
                   hidden: bool = False) -> str: ...


def make_wifi(ssid: str, password: str | None, security: str | None,
              hidden: bool = False) -> QRCode: ...


def make_mecard_data(name: str | Iterable[str],
                     reading: str | None = None,
                     email: str | Iterable[str] | None = None,
                     phone: str | Iterable[str] | None = None,
                     videophone: str | Iterable[str] | None = None,
                     memo: str | None = None,
                     nickname: str | None = None,
                     birthday: str | datetime.date | None = None,
                     url: str | Iterable[str] | None = None,
                     pobox: str | None = None,
                     roomno: str | None = None,
                     houseno: str | None = None,
                     city: str | None = None,
                     prefecture: str | None = None,
                     zipcode: str | None = None,
                     country: str | None = None) -> str: ...


def make_mecard(name: str | Iterable[str],
                reading: str | None = None,
                email: str | Iterable[str] | None = None,
                phone: str | Iterable[str] | None = None,
                videophone: str | Iterable[str] | None = None,
                memo: str | None = None,
                nickname: str | None = None,
                birthday: str | datetime.date | None = None,
                url: str | Iterable[str] | None = None,
                pobox: str | None = None,
                roomno: str | None = None,
                houseno: str | None = None,
                city: str | None = None,
                prefecture: str | None = None,
                zipcode: str | None = None,
                country: str | None = None) -> QRCode: ...


def make_vcard_data(name: str, displayname: str,
                    email: str | Iterable[str] | None = None,
                    phone: str | Iterable[str] | None = None,
                    fax: str | Iterable[str] | None = None,
                    videophone: str | Iterable[str] | None = None,
                    memo: str | None = None,
                    nickname: str | None = None,
                    birthday: str | datetime.date | None = None,
                    url: str | Iterable[str] | None = None,
                    pobox: str | None = None,
                    street: str | None = None,
                    city: str | None = None,
                    region: str | None = None,
                    zipcode: str | None = None,
                    country: str | None = None,
                    org: str | None = None,
                    lat: float | None = None,
                    lng: float | None = None,
                    source: str | None = None,
                    rev: str | datetime.date | None = None,
                    title: str | Iterable[str] | None = None,
                    photo_uri: str | Iterable[str] | None = None,
                    cellphone: str | Iterable[str] | None = None,
                    homephone: str | Iterable[str] | None = None,
                    workphone: str | Iterable[str] | None = None) -> str: ...


def make_vcard(name: str, displayname: str,
               email: str | Iterable[str] | None = None,
               phone: str | Iterable[str] | None = None,
               fax: str | Iterable[str] | None = None,
               videophone: str | Iterable[str] | None = None,
               memo: str | None = None,
               nickname: str | None = None,
               birthday: str | datetime.date | None = None,
               url: str | Iterable[str] | None = None,
               pobox: str | None = None,
               street: str | None = None,
               city: str | None = None,
               region: str | None = None,
               zipcode: str | None = None,
               country: str | None = None,
               org: str | None = None,
               lat: float | None = None,
               lng: float | None = None,
               source: str | None = None,
               rev: str | datetime.date | None = None,
               title: str | Iterable[str] | None = None,
               photo_uri: str | Iterable[str] | None = None,
               cellphone: str | Iterable[str] | None = None,
               homephone: str | Iterable[str] | None = None,
               workphone: str | Iterable[str] | None = None) -> QRCode: ...


def make_geo_data(lat: float, lng: float) -> str: ...


def make_geo(lat: float, lng: float) -> QRCode: ...


def make_make_email_data(to: str | Iterable[str],
                         cc: str | Iterable[str] | None = None,
                         bcc: str | Iterable[str] | None = None,
                         subject: str | None = None,
                         body: str | None = None) -> str: ...


def make_email(to: str | Iterable[str],
               cc: str | Iterable[str] | None = None,
               bcc: str | Iterable[str] | None = None,
               subject: str | None = None,
               body: str | None = None) -> QRCode: ...


def make_epc_qr(name: str, iban: str, amount: int | float | decimal.Decimal,
                text: str | None = None,
                reference: str | None = None,
                bic: str | None = None,
                purpose: str | None = None,
                encoding: str | int | None = None) -> QRCode: ...
