import calendar
import datetime
import time

from dateutil.relativedelta import relativedelta


class DateTimeTypeConversion(object):
    """类型转换"""

    def str_datetime(self, date_time: str):
        """
        date_time = 2000-01-01
        字符串转 datetime"""
        if isinstance(date_time, str):
            try:
                return datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            except:
                return datetime.datetime.strptime(date_time, '%Y-%m-%d')
        elif isinstance(date_time, datetime.datetime):
            return date_time

    def datetime_str(self, date_time: object):
        """
        date_time = datetime.datetime(2021, 9, 15, 0, 0)
        datetime转字符串
        """
        return date_time.strftime('%Y-%m-%d %H:%M:%S')

    def automatic(self, date_time):
        if isinstance(date_time, str):
            return self.str_datetime(date_time)
        if isinstance(date_time, datetime.datetime):
            return self.datetime_str(date_time)
        else:
            raise ValueError("时间格式必须为datetime 或者 str(2022-11-11)")

    def str_time_stamp(self, str_time):
        """str 转 时间戳"""
        try:
            str_time = time.strptime(str_time, '%Y-%m-%d %H:%M:%S')
        except:
            str_time = time.strptime(str_time, '%Y-%m-%d')
        print(str_time)
        return int(time.mktime(str_time))


class CustomBasicDateTime(DateTimeTypeConversion):
    """时间工具"""

    def __init__(self, this_time=None, type_str=True, type_time=False):
        """
        :param type_str: return的数据类型 True：str  False：date_object
        :param type_time: return的数据外观 # True：输出年月日时分秒  False: 输出年月日
        :param this_time: 默认当前时间, 支持 str类型 datetime类型
        """

        self.type_str = type_str

        # 只针对self.type_str=True起作用
        self.type_time = type_time  # True：输出年月日时分秒  False: 输出年月日

        # datetime.datetime(2022, 3, 1, 10, 49, 47, 806942)
        if this_time:
            if isinstance(this_time, str):
                self.this_time = self.str_datetime(this_time)
            else:
                self.this_time = this_time
        else:
            self.this_time = datetime.datetime.now()
        # 2022  int
        self.year = self.this_time.year
        # 3 int
        self.month = self.this_time.month
        # 1 int
        self.day = self.this_time.day
        # 星期几(0,6  0代表周1)， 本月共几天  int
        _, self.month_len = calendar.monthrange(self.year, self.month)
        self.this_week = datetime.date(self.year, self.month, self.day).weekday()
        # 季度
        self.quarter = (self.month - 1) // 3 + 1
        # 字符串时间
        self.str_date = self.this_time.strftime('%Y-%m-%d')

    def time_type(self, date_time=None, dtype=None):
        """
        return
        1 '2022-02-28 10:24:56'
        2 datetime.datetime(2022, 2, 28, 10, 24, 56, 221989)
        """
        if not date_time:
            date_time = self.this_time

        if isinstance(date_time, str):
            date_time = self.str_datetime(date_time)

        if dtype == 'ymd':
            return date_time.strftime('%Y-%m-%d')

        if self.type_str:
            if self.type_time:
                return date_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                return date_time.strftime('%Y-%m-%d')
        return date_time

    def current_year(self):
        """当年"""
        return str(self.year)

    def current_month(self):
        """当月"""
        return str(self.month)

    def current_day(self):
        """当日"""
        return str(self.day)

    def current_week(self):
        """周几"""
        return str(self.this_week)

    def current_month_len(self):
        """这个月多少天"""
        return str(self.month_len)

    def this_time(self):
        """当前时间"""
        return self.time_type(self.this_time)

    def current_yesterday(self):
        """昨天"""
        return self.time_type(self.this_time + datetime.timedelta(days=-1))

    #  =============================== 年月日周前后 ===============================

    def before_after_day(self, day_len):
        """
        前几天   后几天
        -N       N
        """
        return self.time_type(self.this_time + datetime.timedelta(days=day_len))

    def before_after_year(self, year_len, flg=False):
        """
        前几年   后几年  flg=True  如2020-12-01 得到的为2019-12-02
        -N       N
        """
        if year_len > 0:
            if flg:
                tm = self.this_time + datetime.timedelta(days=-1)
                return self.time_type(tm + relativedelta(years=abs(year_len)))
            return self.time_type(self.this_time + relativedelta(years=abs(year_len)))
        else:
            if flg:
                tm = self.this_time + datetime.timedelta(days=1)
                return self.time_type(tm - relativedelta(years=abs(year_len)))
            return self.time_type(self.this_time - relativedelta(years=abs(year_len)))

    def before_after_month(self, month_len, flg=False):
        """
        前几月   后几月
        -N       N
        """
        if month_len > 0:
            if flg:
                tm = self.this_time + datetime.timedelta(days=-1)
                return self.time_type(tm + relativedelta(months=abs(month_len)))
            return self.time_type(self.this_time + relativedelta(months=abs(month_len)))
        else:
            if flg:
                tm = self.this_time + datetime.timedelta(days=1)
                return self.time_type(tm - relativedelta(months=abs(month_len)))
            return self.time_type(self.this_time - relativedelta(months=abs(month_len)))

    def before_after_week(self, week_len):
        """
        前几周   后几周
        -N       N
        """
        if week_len > 0:

            return self.time_type(self.this_time + relativedelta(weeks=abs(week_len)))
        else:

            return self.time_type(self.this_time - relativedelta(weeks=abs(week_len)))

    #  =============================== 周 初 末 ===============================
    def week_first(self, date_time=None):
        """本周初"""
        if not date_time:
            date_time = self.this_time
        return self.time_type(date_time - datetime.timedelta(days=date_time.weekday()))

    def week_end(self, date_time=None):
        """本周末"""
        if not date_time:
            date_time = self.this_time
        return self.time_type(date_time + datetime.timedelta(days=6 - date_time.weekday()))

    def week_upper_end(self):
        """上周末"""
        return self.time_type(self.this_time - datetime.timedelta(days=self.this_time.weekday() + 1))

    def week_upper_first(self):
        """上周初"""
        return self.time_type(self.this_time - datetime.timedelta(days=self.this_time.weekday() + 7))

    def week_first_n(self, week_len):
        """
        前几周   后几周 的周一所在的时间
        -N       N
        """
        date_time = self.before_after_week(week_len)
        return self.week_first(self.str_datetime(date_time))

    def week_end_n(self, week_len):
        """
        前几周   后几周 的周日所在的时间
        -N       N
        """
        date_time = self.before_after_week(week_len)
        return self.week_end(self.str_datetime(date_time))

    #  =============================== 月 初 末 ===============================
    def month_first(self, this_time=None):
        """月初"""
        if not this_time:
            this_time = self.this_time
        return self.time_type(this_time.replace(day=1))

    def month_end(self, this_time=None):
        """月末"""
        if not this_time:
            this_time = self.this_time
        _, month_len = calendar.monthrange(this_time.year, this_time.month)
        return self.time_type(datetime.datetime(year=this_time.year, month=this_time.month, day=month_len))

    def month_upper_first(self):
        """上月初"""
        temporary = self.this_time.replace(day=1) + datetime.timedelta(days=-1)
        return self.time_type(datetime.datetime(temporary.year, temporary.month, 1))

    def month_upper_end(self):
        """上月末"""
        return self.time_type(self.this_time.replace(day=1) + datetime.timedelta(days=-1))

    def month_first_n(self, month_len):
        """
        前几月   后几月
        -N       N
        月的第一天的日期
        """
        date_time = self.before_after_month(month_len)
        return self.month_first(self.str_datetime(date_time))

    def month_end_n(self, month_len):
        """
        前几月   后几月
        -N       N
        月的最后一天的日期
        """
        date_time = self.before_after_month(month_len)
        return self.month_end(self.str_datetime(date_time))

    #  =============================== 年 初 末 ===============================
    def year_first(self, this_time=None):
        """年初"""
        if not this_time:
            this_time = self.this_time
        return self.time_type(this_time.replace(month=1, day=1))

    def year_end(self, this_time=None):
        """年末"""
        if not this_time:
            this_time = self.this_time
        return self.time_type(this_time.replace(month=12, day=31))

    def year_upper_end(self):
        """去年末"""
        return self.time_type(self.this_time.replace(month=1, day=1) + datetime.timedelta(days=-1))

    def year_upper_first(self):
        """去年初"""
        temporary = self.this_time.replace(month=1, day=1) + datetime.timedelta(days=-1)
        return self.time_type(datetime.datetime(temporary.year, 1, 1))

    def year_first_n(self, year_len):
        """
        前几年   后几年
        -N       N
        年的第一天的日期
        """
        year = self.year + year_len
        return self.year_first(self.str_datetime(str(year) + '-01-01'))

    def year_end_n(self, year_len):
        """
        前几年   后几年
        -N       N
        年的最后一天的日期
        """
        year = self.year + year_len
        return self.year_end(self.str_datetime(str(year) + '-01-01'))

    #  =============================== 季 初 末 ===============================
    def quarter_first(self):
        """季初"""
        month = (self.month - 1) - (self.month - 1) % 3 + 1
        return self.time_type(datetime.datetime(self.year, month, 1))

    def quarter_end(self):
        """季末"""
        month = (self.month - 1) - (self.month - 1) % 3 + 1
        if month == 10:
            return self.time_type(datetime.datetime(self.year + 1, 1, 1) + datetime.timedelta(days=-1))
        else:
            return self.time_type(datetime.datetime(self.year, month + 3, 1) + datetime.timedelta(days=-1))

    def quarter_upper_end(self):
        """上季末"""
        month = (self.month - 1) - (self.month - 1) % 3 + 1
        return self.time_type(datetime.datetime(self.year, month, 1) + datetime.timedelta(days=-1))

    def quarter_upper_first(self):
        """上季初"""
        month = (self.month - 1) - (self.month - 1) % 3 + 1
        temporary = datetime.datetime(self.year, month, 1) + + datetime.timedelta(days=-1)
        return self.time_type(datetime.datetime(temporary.year, temporary.month - 2, 1))

    #  =============================== 指定起始时间生成范围 ===============================

    def range_month_first(self, s, e):
        """
        指定时间范围的月的第一天的日期
        s, e = '2015-10-10', '2016-02-07'
        ['2015-10-01', '2015-11-01', '2015-12-01', '2016-01-01', '2016-02-01']
        """
        import pandas as pd
        s = CustomBasicDateTime(s).before_after_month(-1)
        return pd.date_range(s, e, freq='MS').strftime("%Y-%m-%d").tolist()

    def range_month_end(self, s, e):
        """指定时间范围的月的最后一天的日期
        ['2015-10-31', '2015-11-30', '2015-12-31', '2016-01-31', '2016-02-29']
        """
        return [CustomBasicDateTime(i).month_end() for i in self.range_month_first(s, e)]

    def range_month(self, s, e):
        """
        指定时间范围的月
        """
        return [i[0:7] for i in self.range_month_first(s, e)]

    def range_year(self, s, e):
        """年的范围"""
        s = s.split('-')[0]
        e = e.split('-')[0]
        return range(s, e + 1)


if __name__ == '__main__':

    # c = CustomBasicDateTime(this_time='2022-07-12')
    # print(c.this_week)
    pass

