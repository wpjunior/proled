'''tzinfo timezone information for Iran.'''
from pytz.tzinfo import DstTzInfo
from pytz.tzinfo import memorized_datetime as d
from pytz.tzinfo import memorized_ttinfo as i

class Iran(DstTzInfo):
    '''Iran timezone definition. See datetime.tzinfo for details'''

    zone = 'Iran'

    _utc_transition_times = [
d(1,1,1,0,0,0),
d(1915,12,31,20,34,16),
d(1945,12,31,20,34,16),
d(1977,10,31,20,30,0),
d(1978,3,20,20,0,0),
d(1978,10,20,19,0,0),
d(1978,12,31,20,0,0),
d(1979,3,20,20,30,0),
d(1979,9,18,19,30,0),
d(1980,3,20,20,30,0),
d(1980,9,22,19,30,0),
d(1991,5,2,20,30,0),
d(1991,9,21,19,30,0),
d(1992,3,21,20,30,0),
d(1992,9,21,19,30,0),
d(1993,3,21,20,30,0),
d(1993,9,21,19,30,0),
d(1994,3,21,20,30,0),
d(1994,9,21,19,30,0),
d(1995,3,21,20,30,0),
d(1995,9,21,19,30,0),
d(1996,3,20,20,30,0),
d(1996,9,20,19,30,0),
d(1997,3,21,20,30,0),
d(1997,9,21,19,30,0),
d(1998,3,21,20,30,0),
d(1998,9,21,19,30,0),
d(1999,3,21,20,30,0),
d(1999,9,21,19,30,0),
d(2000,3,20,20,30,0),
d(2000,9,20,19,30,0),
d(2001,3,21,20,30,0),
d(2001,9,21,19,30,0),
d(2002,3,21,20,30,0),
d(2002,9,21,19,30,0),
d(2003,3,21,20,30,0),
d(2003,9,21,19,30,0),
d(2004,3,20,20,30,0),
d(2004,9,20,19,30,0),
d(2005,3,21,20,30,0),
d(2005,9,21,19,30,0),
d(2006,3,21,20,30,0),
d(2006,9,21,19,30,0),
d(2007,3,21,20,30,0),
d(2007,9,21,19,30,0),
d(2008,3,20,20,30,0),
d(2008,9,20,19,30,0),
d(2009,3,21,20,30,0),
d(2009,9,21,19,30,0),
d(2010,3,21,20,30,0),
d(2010,9,21,19,30,0),
d(2011,3,21,20,30,0),
d(2011,9,21,19,30,0),
d(2012,3,20,20,30,0),
d(2012,9,20,19,30,0),
d(2013,3,21,20,30,0),
d(2013,9,21,19,30,0),
d(2014,3,21,20,30,0),
d(2014,9,21,19,30,0),
d(2015,3,21,20,30,0),
d(2015,9,21,19,30,0),
d(2016,3,20,20,30,0),
d(2016,9,20,19,30,0),
d(2017,3,21,20,30,0),
d(2017,9,21,19,30,0),
d(2018,3,21,20,30,0),
d(2018,9,21,19,30,0),
d(2019,3,21,20,30,0),
d(2019,9,21,19,30,0),
d(2020,3,20,20,30,0),
d(2020,9,20,19,30,0),
d(2021,3,21,20,30,0),
d(2021,9,21,19,30,0),
d(2022,3,21,20,30,0),
d(2022,9,21,19,30,0),
d(2023,3,21,20,30,0),
d(2023,9,21,19,30,0),
d(2024,3,20,20,30,0),
d(2024,9,20,19,30,0),
d(2025,3,21,20,30,0),
d(2025,9,21,19,30,0),
d(2026,3,21,20,30,0),
d(2026,9,21,19,30,0),
d(2027,3,21,20,30,0),
d(2027,9,21,19,30,0),
d(2028,3,20,20,30,0),
d(2028,9,20,19,30,0),
d(2029,3,20,20,30,0),
d(2029,9,20,19,30,0),
d(2030,3,21,20,30,0),
d(2030,9,21,19,30,0),
d(2031,3,21,20,30,0),
d(2031,9,21,19,30,0),
d(2032,3,20,20,30,0),
d(2032,9,20,19,30,0),
d(2033,3,20,20,30,0),
d(2033,9,20,19,30,0),
d(2034,3,21,20,30,0),
d(2034,9,21,19,30,0),
d(2035,3,21,20,30,0),
d(2035,9,21,19,30,0),
d(2036,3,20,20,30,0),
d(2036,9,20,19,30,0),
d(2037,3,20,20,30,0),
d(2037,9,20,19,30,0),
        ]

    _transition_info = [
i(12360,0,'LMT'),
i(12360,0,'TMT'),
i(12600,0,'IRST'),
i(14400,0,'IRST'),
i(18000,3600,'IRDT'),
i(14400,0,'IRST'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
i(16200,3600,'IRDT'),
i(12600,0,'IRST'),
        ]

Iran = Iran()

