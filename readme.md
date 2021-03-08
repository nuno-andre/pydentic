# Pydentic

**_Pydentic_** is a thin wrapper over _[python-stdnum]_ to facilitate the use
of its extensive collection of validators and formatters in _[Pydantic]_ models.

```
pip install pydentic
```

## Features

Automatic validation and formatting.

```python
from pydentic.strings import Iban
from pydantic import BaseModel

class User(BaseModel):
    name: str
    iban: Iban

user = User(name='John Doe', iban='es1000750080110600658108')
print(user)

#> name='John Doe' iban='ES10 0075 0080 1106 0065 8108'
```

```python
# note the extra last character
user = User(name='John Doe', iban='es1000750080110600658108Ñ')

# raises
...
pydantic.error_wrappers.ValidationError: 1 validation error for User
iban
  es1000750080110600658108Ñ (type=value_error.format; error=invalid literal for int() with base 36: 'Ñ')
```

Title and description in the JSON Schema.
```json
{
  "title": "User",
  "type": "object",
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "iban": {
      "title": "IBAN",
      "description": "International Bank Account Number",
      "type": "string"
    }
  },
  "required": ["user", "iban"]
}
```

## Identifiers

The list below contains some available common identifiers. There are around 200
more included (see [the python-stdnum docs] for the complete list.)

### Information and documentation

| identifier   | spec       | description |
| ------------ | ---------- | ----------- |
| DOI          | ISO 26324  | [Digital Object Identifier][DOI]
| GRid         |            | [Global Release Identifier][GRid]
| ISAN         | ISO 15706  | [International Standard Audiovisual Number][ISAN]
| ISBN         | ISO 2108   | [International Standard Book Number][ISBN]
| ISIL         | ISO 15511  | [International Standard Identifier for Libraries][ISIL]
| ISMN         | ISO 10957  | [International Standard Music Number][ISMN] for notated music
| ISSN         | ISO 3297   | [International Standard Serial Number][ISSN]

### Technology

| identifier   | spec          | description |
| ------------ | ------------- | ----------- |
| IMEI         |               | International Mobile Equipment Identity
| IMSI         | [ITU E.212]   | [International Mobile Subscriber Identity][IMSI]
| MAC address  | IEEE 802      | [Media Access Control address][MAC]
| MEID         | 3GPP2 S.R0048 | Mobile Equipment Identifier

### Other 

| identifier   | spec       | description |
| ------------ | ---------- | ----------- |
| BIC          | [ISO 9362] | [Business Identifier Code][BIC]
| BIC-Code     | ISO 6346   | [International standard for container identification][BIC-Code]
| Bitcoin address |         |
| CAS RN       |            | [Chemical Abstracts Service Registry Number][CASRN]
| CUSIP number |            | [financial security identification number ][CUSIP]
| EAN          |            | [International Article Number][EAN]
| FIGI         | [OMG FIGI] | [Financial Instrument Global Identifier][FIGI]
| GS1-128      |            | GS-1 (product information) using [Code 128 barcodes][C128]
| IBAN         | ISO 13616  | [International Bank Account Number][IBAN]
| IMO number   |            | [International Maritime Organization number][IMO]
| ISIN         | ISO 6166   | International Securities Identification Number
| LEI          | ISO 17442  | [Legal Entity Identifier][LEI]
|              | ISO 11649  | Structured Creditor Reference

[Pydantic]: https://github.com/samuelcolvin/pydantic
[python-stdnum]: https://github.com/arthurdejong/python-stdnum
[the python-stdnum docs]: https://arthurdejong.org/python-stdnum/formats

[BIC]: https://www.swift.com/standards/data-standards/bic-business-identifier-code "(SWIFT) Society for Worldwide Interbank Financial Telecommunication"
[BIC-Code]: https://www.bic-code.org/ "Bureau International des Containers et du Transport Intermodal"
[CASRN]: https://www.cas.org/support/documentation/chemical-substances/faqs "(CAS) Chemical Abstracts Service"
[CUSIP]: https://www.cusip.com/identifiers.html#/CUSIP "CUSIP Global Services"
[C128]: https://en.wikipedia.org/wiki/Code_128
[DOI]: https://www.doi.org/hb.html "DOI handbook"
[EAN]: https://www.gs1.org/standards/barcodes/ean-upc "GS1 - EAN/UPC"
[FIGI]: https://www.openfigi.com/ "Open FIGI"
[GRid]: https://www.ifpi.org/resource/grid/ "(IFPI) International Federation of the Phonographic Industry. I've said \"pho-no-gra-phic\""
[IBAN]: https://www.swift.com/standards/data-standards/iban-international-bank-account-number "(SWIFT) Society for Worldwide Interbank Financial Telecommunication"
[IMO]: https://www.imo.org/en/OurWork/MSAS/Pages/IMO-identification-number-scheme.aspx "(IMO) International Maritime Organization"
[IMSI]: https://imsiadmin.com/
[ISAN]: https://www.isan.org/ "ISAN International Agency"
[ISBN]: https://www.isbn-international.org/content/what-isbn "International ISBN Agency"
[ISIL]: https://english.slks.dk/libraries/library-standards/isil/ "Danish Agency for Culture and Palaces (ISIL international authority)"
[ISMN]: https://www.ismn-international.org/ "International ISMN Agency"
[ISSN]: https://portal.issn.org/ "ISSN International Centre"
[LEI]: https://www.gleif.org/en/about-lei/introducing-the-legal-entity-identifier-lei "(GLEIF) Global Legal Entity Identifier Foundation"
[MAC]: https://standards.ieee.org/content/ieee-standards/en/products-services/regauth/index.html

<!-- standard specs -->
[ISO 9362]: https://www.iso9362.org/isobic/overview.html
[ITU E.212]: https://www.itu.int/rec/T-REC-E.212
[OMG FIGI]: https://www.omg.org/spec/FIGI/1.0
