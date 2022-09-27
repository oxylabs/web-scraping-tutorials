# A Complete Date Parser Tutorial

<img src="https://img.shields.io/static/v1?label=&message=Python&color=blueviolet" />  <img src="https://img.shields.io/static/v1?label=&message=Data%20Parsing&color=blue" /> <img src="https://img.shields.io/static/v1?label=&message=Parser%20Date&color=yellowgreen" /> <img src="https://img.shields.io/static/v1?label=&message=Python%20Date%20Parser&color=brightgreen" />

This article covers everything you need to know about parsing dates in Python. By the end of this article, you will be able to extract human-readable strings from dates and parse strings into dates.

## Table of Contents

- [Introduction](#introduction)
- [Parsing Dates Into String](#parsing-dates-into-string)
  - [Quick Conversion to String Using Attributes](#quick-conversion-to-string-using-attributes)
  - [Extract String With a Finer Control](#extract-string-with-a-finer-control)
- [Parsing Dates From String](#parsing-dates-from-string)
- [Date Parser Package](#date-parser-package)
	- [Basic Usage of Date Parser](#basic-usage-of-date-parser)
	- [Parsing Ambiguous Dates With Date Parser](#parsing-ambiguous-dates-with-date-parser)
	- [Parsing Relative Dates With Date Parser](#parsing-relative-dates-with-date-parser)
	- [Handling Time Zones and Languages](#handling-time-zones-and-languages)

## Introduction

Python comes with a very powerful module for handing dates—[datetime](https://docs.python.org/3/library/datetime.html). This module ships with a class that also has the same name—[datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime).

This class is very powerful and it can handle *aware* and *naïve* objects. *Aware* objects are the ones that have time zone information attribute, `tzinfo`. While *naïve* objects are open to interpretation because there is no time zone information.

Quite often, there will be a need to represent the `datetime` object as `string`. On the other hand, there will be a need to parse `datetime` objects from `string` objects.

Let's explore extracting `string` from `datetime` objects first.

## Parsing Dates Into String

The `datetime` class has a useful method - `today()`. This method returns a new `datetime` object representing the current time.

```python
>>> from datetime import datetime
>>> published_date = datetime.today()
>>> published_date
datetime.datetime(2021, 9, 17, 17, 21, 2, 397259)
>>> print(today)
2021-09-17 17:21:02.397259
```

As evident here, `published_date` is an object of datetime. Printing this on the console prints out the year, month, date, hours, minutes, seconds, and milliseconds in one long string.

### Quick Conversion to String Using Attributes

This object has some useful attributes which can help in getting the day, month, year, etc. Here are few examples.

```python
>>> published_date.year
2021
>>> published_date.month
5
>>> published_date.day
20
```

Similarly, there are other useful attributes like `hour`, `minute`, `second`.

```python
>>> published_date.hour
17
>>> published_date.minute
21
>>> published_date.second
2
```

These attributes may be good enough for few cases.

Typically, a more refined control is needed.

### Extract String With a Finer Control

The `datetime.datetime` object can be easily converted to strings in any desired format, thanks to the [strftime](https://docs.python.org/3/library/datetime.html#datetime.date.strftime) function.  

Here is one example:

```python
>>> published_date.strftime('%m/%d/%Y')
'09/17/2021'
```

Note that `Y` in this example is an uppercase Y. A lowercase `y` prints the year in a two-digit format.

```python
>>> published_date.strftime('%m/%d/%y')
'09/17/21'
```

For month, `%B` will extract the Month as full name, and `%b` will extract the abbreviated month name:

```python
>>> published_date.strftime('%b %d,%Y')
'Sep 17,2021'
>>> published_date.strftime('%B %d,%Y')
'September 17,2021'
```

The only difficult aspect of `strftime` function is that remembering all these format codes is not easy.

#### Format Codes Quick Reference

Here is a quick reference of the commonly used codes. For the full list, see [official documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

**Note**: Every number is zero-padded by default.

| Directive | Meaning                    | Example   |
| --------- | -------------------------- | --------- |
| `%d`      | Day of the month.          | 17        |
| `%b`      | Month as abbreviated name. | Sep       |
| `%B`      | Month as full name.        | September |
| `%m`      | Month as number.           | 09        |
| `%y`      | Year without century.      | 21        |
| `%Y`      | Year with century.         | 2021      |
| `%H`      | Hour (24-hour clock).      | 17        |
| `%I`      | Hour (12 hour clock).      | 05        |
| `%M`      | Minute.                    | 21        |
| `%S`      | Second.                    | 02        |

## Parsing Dates From String

Often, there is a need to convert a string representation of a date to a `datetime` object. The source of these strings can be anything such as user input, files, scraped data, etc.

Any string that represents date and/or time can be converted into `datetime` objects by using Python's `strpdate` function.  This function uses the same format codes that are used by [`strtftime`](#Format-Codes-Quick-Reference).

The Let's look at an example:

```python
>>> date_mdy = '09/17/21'
>>> type(date_mdy)
<class 'str'>
>>> datetime.strptime(date_mdy,'%m/%d/%y')
datetime.datetime(2021, 9, 17, 0, 0)
```

This function takes two arguments: the first is the string that represents the date. The second parameter is the format. If this function cannot parse the string into datetime using the format supplied, it will raise a `ValueError`.

The format string can be customized to convert a variety of scenarios.

```python
>>> date_Bdy ='September 17,2021'
>>> datetime.strptime(date_Bdy,'%B %d,%Y')
datetime.datetime(2021, 9, 17, 0, 0)
```

Note that even one extra space will result in failed parsing.

```python
>>> date_Bdy ='September 17,2021' # No space before year
>>> datetime.strptime(date_Bdy,'%B %d, %Y') # Space before year
 ...  
ValueError: time data 'September 17,2021' does not match format '%B %d, %Y'
```

Moreover, for every format, the format string has to be carefully constructed. This involves rereferring the  [official documentation](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) to find the format codes, taking care of all the edge cases. Handling relative dates like "tomorrow" are even more difficult. Other problems are handling time zones and various locales.

All these complexities can be reduced with the help of Date Parser package.

## Date Parser Package

Date Parser is a package that aims to make parsing dates from string much easier, without going into the complexities required by `strptime` function, while still being powerful.

Date Parser package can be installed easily from the terminal.

```shell
pip install dateparser
```

If you are using Anaconda, it is available on the default channel as well as `conda-forge`.

```shell
conda install dateparser
```

The next step is to explore the basic usage of Date Parser.

### Basic Usage of Date Parser

The most common way of working with date parser is to use the `parse` function. The only mandatory argument for this function is the string that represents the date.

For most of the commonly used date formats, simply supplying the date string to the parse string works.

```python
>>> from dateparser import parse
>>> parse('09/17/21')
datetime.datetime(2021, 9, 17, 0, 0)
```

This method takes away the complication of building the format string and create the `datetime` object.

The parse method is forgiving about the separator and space. Here are few more examples of how easily date parser takes care of parsing without worrying about format strings.

```python
>>> parse('09/17/21')
datetime.datetime(2021, 9, 17, 0, 0)
>>> parse('09-17-21')
datetime.datetime(2021, 9, 17, 0, 0)
>>> parse('09 17 21')
datetime.datetime(2021, 9, 17, 0, 0)
>>> parse('09~17~21')
datetime.datetime(2021, 9, 17, 0, 0)
```

Note that, unlike `datetime.strptime` function, date parser's `parse` method does not raise `ValueError` if it  is unable to convert to a `datetime` object.

```python
>>> print(parse('091721'))
None
```

Apart from the numeric date formats, date parser can handle month names.

```python
>>> parse('September 17,2021')
datetime.datetime(2021, 9, 17, 0, 0)
>>> parse('September17,2021') # No space anywhere
datetime.datetime(2021, 9, 17, 0, 0)
```

Apart from the date, date parser can also parse strings that contain time values. For example, lets take the string '2021-09-17 17:21:02.397259'. This contains year, date, month, hours, minutes, seconds and microseconds.  The `parse` method handles it perfectly:

```python
>>> parse('2021-09-17 17:21:02.397259')
datetime.datetime(2021, 9, 17, 17, 21, 2, 397259)
```

Here are few more examples:

```python
>>> dateparser.parse('Wed, 17 May 2021 17:21:02')
datetime.datetime(2021, 5, 17, 17, 21, 2)
```

This takes care of the most common date formats. However, often there are cases when this is not sufficient. For example, the date string `'09/07/21'` is ambiguous. The month can be 09 or 07, based on the source of the data. There are few ways to handle this.

### Parsing Ambiguous Dates with Date Parser

The parse method has many optional parameters. One of the parameter is `date_formats`. Note that this parameter expects a `list` of format strings. This will contains a list of possible formats that date parser can use to detect the date.

```python
>>> parse('09/07/21')
datetime.datetime(2021, 9, 7, 0, 0)
>>> parse('09/07/21', date_formats=['%d/%m/%y']) # Month is 07
datetime.datetime(2021, 7, 9, 0, 0)
```

The other way is to provide the locale. For example, for locale  `en-US` month is written first, while for locale `en-GB`, the day is written first. The locale information can be supplied using the optional parameter `locales`, which is again a `list` of possible locales.

```python
>>> parse('09/07/21')
datetime.datetime(2021, 9, 7, 0, 0)
>>> parse('09/07/21', locales=['en-GB'])
datetime.datetime(2021, 7, 9, 0, 0)
```

Another option is to use the `settings` parameter. This parameter expects a dictionary. Here is an example to handle this date:

```python
>>> parse('09/07/21', settings={'DATE_ORDER': 'MDY'}) # Month first
datetime.datetime(2021, 9, 7, 0, 0)
>>> parse('09/07/21', settings={'DATE_ORDER': 'DMY'}) # Day first
datetime.datetime(2021, 7, 9, 0, 0)
```

### Parsing Relative Dates With Date Parser

Strings like `today`, `tomorrow`, `yesterday`  can be parsed directly with Date Parser. More impressively, relative dates like `3 days ago`, `in two days` work as well. Be careful with this as this works only with specific phrases. For example, `in two days` can be parsed work but aft two days does not work.

```python
>>> parse('today')
datetime.datetime(2021, 9, 17, 10, 54, 17, 197078)
>>> parse('tomorrow')
datetime.datetime(2021, 9, 18, 10, 54, 23, 906776)
>>> parse('yesterday')
datetime.datetime(2021, 9, 16, 10, 54, 31, 875047)
>>> parse('3 days ago')
datetime.datetime(2021, 9, 14, 10, 54, 43, 614972)
>>> parse('in 3 days')
datetime.datetime(2021, 9, 20, 10, 54, 57, 176714)
>>> parse('after 3 days') # Can not be parsed
```



### Handling Time Zones and Languages

Date Parser can handle time zone information in various ways. The first and easiest way is to supply the time zone abbreviation in the parse string directly. Three-letter abbreviations like `EST` and UTC offsets like `-0500` both work.

```python
>>> parse('09/07/21 9:30pm EST')
datetime.datetime(2021, 9, 7, 21, 30, tzinfo=<StaticTzInfo 'EST'>)
>>> parse('09/07/21 9:30pm -0500')
datetime.datetime(2021, 9, 7, 21, 30, tzinfo=<StaticTzInfo 'UTC\-05:00'>)
```

Another way of attaching time zone information is to set it in settings parameter. Note that this would need both `TIMEZONE` and `RETURN_AS_TIMEZONE_AWARE` to be supplied.

```python
>>> parse('09/07/21 9:30pm', settings={'TIMEZONE': 'EST','RETURN_AS_TIMEZONE_AWARE': True})
datetime.datetime(2021, 9, 7, 21, 30, tzinfo=<StaticTzInfo 'EST'>)
```

Apart from time zones, Date Parser can handle over 200 locales.

```python
>>> parse('27 सितंबर, 2021') # Hindi
datetime.datetime(2021, 9, 27, 0, 0)
>>> parse('17 сентября 2021') # Russian
datetime.datetime(2021, 9, 27, 0, 0)
>>> parse('2021年9月17日') # Simplified Chinese
datetime.datetime(2021, 9, 27, 0, 0)
```
