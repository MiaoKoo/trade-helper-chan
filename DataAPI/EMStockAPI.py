from datetime import datetime
from typing import Iterable

from gm.api import history, ADJUST_PREV, ADJUST_POST, ADJUST_NONE

from Common.CTime import CTime
from KLine.KLine_Unit import CKLine_Unit
from .CommonStockAPI import CCommonStockApi
from Common.CEnum import AUTYPE, DATA_FIELD, KL_TYPE


def parse_column_name_from_fields(fields: str):
    _dict = {
        "eob": DATA_FIELD.FIELD_TIME,
        "open": DATA_FIELD.FIELD_OPEN,
        "high": DATA_FIELD.FIELD_HIGH,
        "low": DATA_FIELD.FIELD_LOW,
        "close": DATA_FIELD.FIELD_CLOSE,
        "volume": DATA_FIELD.FIELD_VOLUME,
        "amount": DATA_FIELD.FIELD_TURNOVER,
    }
    return [_dict[x] for x in fields.split(",")]


def create_item_dict(row_data, column_name):
    return dict(zip(column_name, row_data))


def parse_time_column(dt: datetime):
    year = int(dt.year)
    month = int(dt.month)
    day = int(dt.day)
    hour = int(dt.hour)
    minute = int(dt.minute)

    return CTime(year, month, day, hour, minute)


class EMStockAPI(CCommonStockApi):
    def __init__(self, code, k_type=KL_TYPE.K_DAY, begin_date=None, end_date=None, autype=AUTYPE.QFQ):
        super(EMStockAPI, self).__init__(code, k_type, begin_date, end_date, autype)

    def get_kl_data(self) -> Iterable[CKLine_Unit]:
        autype_dict = {AUTYPE.QFQ: ADJUST_PREV, AUTYPE.HFQ: ADJUST_POST, AUTYPE.NONE: ADJUST_NONE}
        fields = 'eob,open,high,low,close'
        data = history(self.code, frequency=self.__convert_type(), start_time=self.begin_date, end_time=self.end_date,
                       fields=fields, adjust=autype_dict[self.autype], adjust_end_time=self.end_date, df=True)
        parsed_fields = parse_column_name_from_fields(fields)
        if len(data) == 0:
            raise Exception("Get history data failed")
        for index, row in data.iterrows():
            # row['open'], row['high'], row['low'], row['close'], row['eob']
            kl_unit = CKLine_Unit(
                create_item_dict([parse_time_column(row['eob']), row['open'], row['high'], row['low'], row['close']],
                                 parsed_fields))
            yield kl_unit

    def SetBasciInfo(self):
        pass

    @classmethod
    def do_init(cls):
        pass

    @classmethod
    def do_close(cls):
        pass

    def __convert_type(self):
        _dict = {
            KL_TYPE.K_DAY: '1d',
            KL_TYPE.K_5M: '5m',
            KL_TYPE.K_30M: '30m',
        }
        return _dict[self.k_type]
