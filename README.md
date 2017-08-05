Czech Working Month
===================

Calculate the exact working month length including weekends and Czech national holidays.
This tool is usefull when working on full-time or part-time with irregular working hours,
homeoffice etc. but your salary is (by law) fixed each month.

Installation
------------
```bash
pip install git+https://github.com/petrbel/czech-working-month.git 
```

Examples
--------

Show me the details of the current working month:
```bash
czech-working-month
```

Show me the details of this year February (2nd month):
```bash
czech-working-month 2
```

Show me the details of February (2nd month) 2010:
```bash
czech-working-month 2 2010
```

Show me the the current working month in the case I am employed at 0.6 part-time ratio:
```bash
czech-working-month -p 0.6
```

Show me the details of February (2nd month) 2010 when I work at 0.6 part-time ratio:
```bash
czech-working-month 2 2010 -p 0.6
```
