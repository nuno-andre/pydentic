from ..core import RegExpString


class CnPostalCode(
    RegExpString,
    pattern=r'^(?P<province>\d\d)(?P<zone>\d)(?P<prefecture>\d)(?P<area>\d\d)$'
):
    '''China Postal Code.

    Attrs:
        province: province, province-equivalent municipality, or
            autonomous region.
        zone: postal zone within the province, municipality or
            autonomous region.
        prefecture: postal office within prefectures or prefecture-level
            cities.
        area: specific mailing area for delivery.
    '''
