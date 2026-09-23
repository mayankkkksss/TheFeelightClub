# The Feelight Club

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

A Python flight deal tracker that searches for cheap flights and sends notifications when a flight is found below the target price.

The project uses **Google Sheets + Sheety** for destination and customer data, **SerpAPI Google Flights** for flight searches, **Twilio** for WhatsApp/SMS notifications, and **Gmail SMTP** for email notifications.

## Features

* Search round-trip flights from a configurable origin airport.
* Read destinations and target prices from Google Sheets.
* Search for direct flights first.
* Automatically search for indirect flights when no direct flight is available.
* Track the number of stops for indirect flights.
* Compare flight prices with target prices.
* Send flight deal notifications through WhatsApp and SMS.
* Send flight deals to registered customers by email.
* Collect customer information through a Google Form.
* Configure the currency symbol and currency code.
* Handle missing or unavailable flight data.

## How It Works

```text
Google Sheets
     │
     ├── prices
     │    ├── City
     │    ├── IATA Code
     │    └── Lowest Price
     │
     └── users
          ├── First Name
          ├── Last Name
          └── Email
     │
     ▼
   Sheety API
     │
     ▼
  SerpAPI Google Flights
     │
     ├── Search direct flights
     │
     └── No direct flight
              │
              ▼
       Search indirect flights
     │
     ▼
 Compare with target price
     │
     ├── No cheaper flight → No notification
     │
     └── Cheaper flight found
              │
              ├── WhatsApp / SMS
              └── Email customers
```

## Flight Search

The program searches each destination in the `prices` sheet.

The search process is:

1. Search for a direct flight.
2. If a direct flight is available, use the cheapest direct flight.
3. If no direct flight is available, search for an indirect flight.
4. Capture the number of stops.
5. Compare the flight price with the target price.
6. Send notifications when a cheaper flight is found.

The starting airport is configured in `main.py`:

```python
ORIGIN_CITY_IATA = "BOM"
```

This can be changed to another airport's IATA code.

## Google Sheets

### `prices`

Stores the destinations and target prices.

| City      | IATA Code | Lowest Price |
| --------- | --------- | -----------: |
| Paris     | CDG       |          145 |
| Frankfurt | FRA       |          152 |
| Tokyo     | HND       |          892 |

### `users`

Stores customers collected through the Google Form.

| Timestamp | First Name | Last Name | Email |
| --------- | ---------- | --------- | ----- |
| ...       | ...        | ...       | ...   |

The Google Form is connected to the `users` sheet so new customers can be added automatically.

## Notifications

### WhatsApp / SMS

Twilio is used to send flight deal notifications.

Notifications include:

* Flight price
* Origin airport
* Destination airport
* Outbound date
* Return date
* Number of stops

Example direct-flight notification:

```text
Low price alert! Only GBP 152 to fly direct from LHR to FRA,
on 2026-09-23 until 2027-03-21.
```

Example indirect-flight notification:

```text
Low price alert! Only GBP 892 to fly from LHR to DPS,
with 1 stop(s) departing on 2026-09-23 and returning on 2027-03-21.
```

WhatsApp notifications were tested successfully.

### Email

The project uses SMTP for email notifications and was tested with Gmail SMTP.

When a cheap flight is found, the program retrieves customers from the `users` sheet and sends them the flight deal by email.

## Currency Configuration

Currency can be configured through environment variables:

```env
CURRENCY_SYMBOL="₹"
CURRENCY_CODE="INR"
```

For example:

```env
CURRENCY_SYMBOL="$"
CURRENCY_CODE="USD"
```

or:

```env
CURRENCY_SYMBOL="€"
CURRENCY_CODE="EUR"
```

## Environment Variables

Create a `.env` file with the following configuration:

```env
# Sheety
SHEETY_PRICES_ENDPOINT="your_sheety_prices_endpoint"
SHEETY_USERS_ENDPOINT="your_sheety_users_endpoint"
SHEETY_USERNAME="your_sheety_username"
SHEETY_PASSWORD="your_sheety_password"

# SerpAPI
SERPAPI_API_KEY="your_serpapi_api_key"

# Twilio
TWILIO_SID="your_twilio_sid"
TWILIO_AUTH_TOKEN="your_twilio_auth_token"
TWILIO_VIRTUAL_NUMBER="your_twilio_virtual_number"
TWILIO_VERIFIED_NUMBER="your_verified_number"
TWILIO_WHATSAPP_NUMBER="your_twilio_whatsapp_number"

# Email / SMTP
EMAIL_PROVIDER_SMTP_ADDRESS="your_smtp_server"
MY_EMAIL="your_email_address"
MY_EMAIL_PASSWORD="your_email_password_or_app_password"

# Currency
CURRENCY_SYMBOL="£"
CURRENCY_CODE="GBP"
```

Replace the placeholder values with your own configuration.

## Project Structure

```text
TheFeelightClub/
│
├── data_manager.py
├── flight_data.py
├── flight_search.py
├── main.py
├── notification_manager.py
├── requirements.txt
└── README.md
```

### Main Components

* **`main.py`** — Runs the application and connects all components.
* **`data_manager.py`** — Handles Google Sheets data through Sheety.
* **`flight_search.py`** — Searches for flights using SerpAPI.
* **`flight_data.py`** — Stores and structures flight information.
* **`notification_manager.py`** — Handles WhatsApp, SMS, and email notifications.

## Technologies Used

* Python
* SerpAPI Google Flights
* Sheety API
* Google Sheets
* Google Forms
* Twilio
* Gmail SMTP
* `requests`
* `python-dotenv`
* `twilio`

## Testing

The project was tested with three destinations.

Testing covered:

* Direct flights
* Indirect flight fallback
* WhatsApp notifications
* Email notifications
* Customer data from Google Forms
* Multiple destinations and target prices

Twilio SMS functionality can depend on the configuration and verification status of the Twilio account.

## Error Handling

The project includes handling for cases such as:

* Flight search errors
* Missing flight data
* Missing flight prices
* No direct flight availability
* No usable flight results

When a direct flight cannot be found, the program automatically attempts an indirect flight search.

## Caching

Request caching is not currently enabled.

The caching code from the course remains commented out in `main.py`.

## What I Practiced

* Object-oriented programming
* REST APIs
* API authentication
* Environment variables
* JSON data handling
* Google Sheets integration
* Sheety API
* SerpAPI Google Flights
* Date and time handling
* Flight price comparison
* Direct and indirect flight searching
* Twilio notifications
* SMTP email
* Google Forms integration
* Error handling

## Course

This project was built as part of **100 Days of Code: The Complete Python Pro Bootcamp** by Angela Yu.

**This README.md is AI-generated; perception are not.**
