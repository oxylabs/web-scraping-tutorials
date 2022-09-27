# Reading & Parsing JSON Data With Python

[<img src="https://img.shields.io/static/v1?label=&message=Json&color=brightgreen" />](https://github.com/topics/json) [<img src="https://img.shields.io/static/v1?label=&message=Python&color=important" />](https://github.com/topics/python)


- [What is JSON?](#what-is-json)
- [Converting JSON string to Python object](#converting-json-string-to-python-object)
- [Converting JSON file to Python object](#converting-json-file-to-python-object)
- [Converting Python object to JSON string](#converting-python-object-to-json-string)
- [Writing Python object to a JSON file](#writing-python-object-to-a-json-file)
- [Converting custom Python objects to JSON objects](#converting-custom-python-objects-to-json-objects)
- [Creating Python class objects from JSON objects](#creating-python-class-objects-from-json-objects)


JSON is a common standard used by websites and APIs and even natively supported by modern databases such as PostgreSQL. In this article, we’ll present a tutorial on how to handle JSON data with Python

For a detailed explanation, see our [blog post](https://oxy.yt/9rL7).

## What is JSON?

JSON, or JavaScript Object Notation, is a format that uses text to store data objects:

```json
{
   "name": "United States",
   "population": 331002651,
   "capital": "Washington D.C.",
   "languages": [
      "English",
      "Spanish"
   ]
}
```

## Converting JSON string to Python object

Let’s start with a simple example:

```python
# JSON string
country = '{"name": "United States", "population": 331002651}'
print(type(country))
```

The output of this snippet will confirm that this is indeed a string:

```python
<class 'str'>
```

We can call the `json.loads()` method and provide this string as a parameter.

```python
import json

country = '{"name": "United States", "population": 331002651}'
country_dict = json.loads(country)

print(type(country))
print(type(country_dict))
```

The output of this snippet will confirm that the JSON data, which was a string, is now a Python dictionary.

```python
<class 'str'>
<class 'dict'>
```

This dictionary can be accessed as usual:

```python
print(country_dict['name'])
# OUTPUT:   United States
```

It is important to note here that the `json.loads()` method will not always return a dictionary. The data type that is returned will depend on the input string. For example, this JSON string will return a list, not a dictionary.

```
countries = '["United States", "Canada"]'
counties_list= json.loads(countries)

print(type(counties_list))
# OUTPUT:  <class 'list'>
```

Similarly, if the JSON string contains `true`, it will be converted to Python equivalent boolean value, which is `True`.

```
import json
 
bool_string = 'true'
bool_type = json.loads(bool_string)
print(bool_type)
# OUTPUT:  True
```

The following table shows JSON objects and the Python data types after conversion. For more details, see [Python docs](https://docs.python.org/3/library/json.html%23json-to-py-table).

## Converting JSON file to Python object

Save the following JSON data as a new file and name it `united_states.json`:

```json
{
   "name": "United States",
   "population": 331002651,
   "capital": "Washington D.C.",
   "languages": [
      "English",
      "Spanish"
   ]
}
```

Enter this Python script in a new file:

```python
import json

with open('united_states.json') as f:
  data = json.load(f)

print(type(data))
```

Running this Python file prints the following:

```py'
<class 'dict'>
```

The dictionary keys can be checked as follows:

```py'
print(data.keys())
# OUTPUT:  dict_keys(['name', 'population', 'capital', 'languages'])
```

Using this information, the value of `name` can be printed as follows:

```python
data['name']
# OUTPUT:  United States
```

## Converting Python object to JSON string

Save this code in a new file as a Python script:

```python
import json

languages = ["English","French"]
country = {
    "name": "Canada",
    "population": 37742154,
    "languages": languages,
    "president": None,
}

country_string = json.dumps(country)
print(country_string)
```

When this file is run with Python, the following output is printed:

```python
{"name": "Canada", "population": 37742154, "languages": ["English", "French"],
 "president": null}
```

Lists can be converted to JSON as well. Here is the Python script and its output:

```python
import json

languages = ["English", "French"]

languages_string = json.dumps(languages)
print(languages_string)
# OUTPUT:   ["English", "French"]
```

It’s not just limited to a dictionary and a list. `string`, `int`, `float`, `bool` and even `None` value can be converted to JSON. 

## Writing Python object to a JSON file

The method used to write a JSON file is `dump()`:

```python
import json

# Tuple is encoded to JSON array.
languages = ("English", "French")
# Dictionary is encoded to JSON object.
country = {
    "name": "Canada",
    "population": 37742154,
    "languages": languages,
    "president": None,
}

with open('countries_exported.json', 'w') as f:
    json.dump(country, f)
```

 To make it more readable, we can pass one more parameter to the `dump()` function as follows:

```python
json.dump(country, f, indent=4)
```

This time when you run the code, it will be nicely formatted with indentation of 4 spaces:

```json
{
    "languages": [
        "English", 
        "French"
    ], 
    "president": null, 
    "name": "Canada", 
    "population": 37742154
}
```

## Converting custom Python objects to JSON objects

Save the following code as a Python script and run it:

```python
import json

class Country:
    def __init__(self, name, population, languages):
        self.name = name    
        self.population = population
        self.languages = languages

    
canada = Country("Canada", 37742154, ["English", "French"])

print(json.dumps(canada))
# OUTPUT:   TypeError: Object of type Country is not JSON serializable
```

To convert the objects to JSON, we need to write a new class that extends JSONEncoder:

```python
import json 
 
class CountryEncoder(json.JSONEncoder):
    def default(self, o): 
        if isinstance(o, Country):
           # JSON object would be a dictionary.
						return {
                "name" : o.name,
                "population": o.population,
                "languages": o.languages
            } 
        else:
            # Base class will raise the TypeError.
            return super().default(o)
```

This class can now be supplied to the `json.dump()` as well as `json.dumps()` methods.

```python
print(json.dumps(canada, cls=CountryEncoder))
# OUTPUT:  {“name": "Canada", "population": 37742154, "languages": ["English", "French"]}
```

## Creating Python class objects from JSON objects

Using a custom encoder, we were able to write code like this:

```python
# Create an object of class Country
canada = Country("Canada", 37742154, ["English", "French"])
# Use json.dump() to create a JSON file in writing mode
with open('canada.json','w') as f:
    json.dump(canada,f, cls=CountryEncoder)
```

If we try to parse this JSON file using the `json.load()` method, we will get a dictionary:

```python
with open('canada.json','r') as f:
    country_object = json.load(f)
# OUTPUT:  <type ‘dict'>
```

To get an instance of the `Country` class instead of a dictionary, we need to create a custom decoder:

```python
import json
 
class CountryDecoder(json.JSONDecoder):
    def __init__(self, object_hook=None, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):
        decoded_country =  Country(
            o.get('name'), 
            o.get('population'), 
            o.get('languages'),
        )
        return decoded_country
```

Finally, we can call the `json.load()` method and set the `cls` parameter to `CountryDecoder` class.

```python
with open('canada.json','r') as f:
    country_object = json.load(f, cls=CountryDecoder)

print(type(country_object))
# OUTPUT:  <class ‘Country'>
```


If you wish to find out more about Reading & Parsing JSON Data With Python, see our [blog post](https://oxy.yt/9rL7).
