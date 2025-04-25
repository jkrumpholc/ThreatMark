Your task is to get environmental data from a sense box. Use https://docs.opensensemap.org for documentation.

1. Use public api for opensensemap.org to get data from a box with id 6693dc2ce3b7f100081984f8
2. From this box get the temperature and humidity data
3. Add some form of cache that ensures that you don't call the api more than once in 5 minutes.
4. Print the last temperature and humidity data in format defined in config.json,
together with the time of measurement in the specified format.
Example output:

- Temperature: 53.42°F Measured on: Thursday, 03. April 2025 08:32PM
- Temperature: 53.438°F Measured on: Thursday, 03. April 2025 08:30PM
- Temperature: 53.456°F Measured on: Thursday, 03. April 2025 08:27PM
- Temperature: 53.492°F Measured on: Thursday, 03. April 2025 08:25PM
- Temperature: 53.492°F Measured on: Thursday, 03. April 2025 08:22PM
- Humidity: 48.16% Measured on: Thursday, 03. April 2025 08:35PM
- Humidity: 48.22% Measured on: Thursday, 03. April 2025 08:32PM
- Humidity: 47.93% Measured on: Thursday, 03. April 2025 08:30PM
- Humidity: 48.23% Measured on: Thursday, 03. April 2025 08:27PM
- Humidity: 48.19% Measured on: Thursday, 03. April 2025 08:25PM


Hints:
    The date format in config.json is a python datetime strftime format string
    Load the json config and create a Config class with the attributes temperature_unit and date_format
    The cache can be implemented as a temporary file on disk.
    Add some tests

Commit and push your code to your private GitHub repository and share it with petr.barton@threatmark.com

