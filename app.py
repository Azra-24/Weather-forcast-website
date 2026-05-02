from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("API_KEY")
@app.route("/", methods=["GET", "POST"])
def home():
    temp = humidity = weather = error = None
    bg_class = "default"
    temps = []
    dates = []
    
    if request.method == "POST":
        city = request.form.get("city")

        if not city:
            error = "Please enter a city name"
        else:
            try:
                #Current weather
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url)
                data = response.json()

                if str(data.get("cod")) != "200":
                    error = data.get("message", "Something went wrong")
                else:
                    temp = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    weather = data["weather"][0]["description"]

                    # Background logic
                    w = weather.lower()
                    if "clear" in w:
                        bg_class = "sunny"
                    elif "rain" in w or "drizzle" in w:
                        bg_class = "rainy"
                    elif "cloud" in w:
                        bg_class = "cloudy"

                    #Forecast graph
                    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
                    forecast_response = requests.get(forecast_url)
                    forecast_data = forecast_response.json()

                    if str(forecast_data.get("cod")) == "200":
                        # take 1 reading per day (clean graph)
                        for item in forecast_data["list"][::8][:5]:
                            temps.append(item["main"]["temp"])
                            dates.append(item["dt_txt"].split()[0])

            except Exception as e:
                error = "Error fetching data. Try again."

    return render_template(
        "index.html",
        temp=temp,
        humidity=humidity,
        weather=weather,
        error=error,
        bg_class=bg_class,
        temps=temps,
        dates=dates
    )

if __name__ == "__main__":
    app.run(debug=True)