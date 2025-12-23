import requests
import google.generativeai as genai

def extract_cities_from_prompt(prompt, gemini_api_key):
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        extract_prompt = (
            f"Extract all city names from this user prompt. "
            f"Return a comma-separated list of cities only, no extra text.\n"
            f"Prompt: {prompt}"
        )
        response = model.generate_content(extract_prompt)
        cities = [city.strip() for city in response.text.split(',') if city.strip()]
        return cities
    except Exception as e:
        print(f"Error extracting cities: {e}")
        return []

def get_weather_content(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data['name'],
            "weather": data['weather'][0]['description'],
            "temp": data['main']['temp'],
            "success": True
        }
    elif response.status_code == 404:
        if ',' not in city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city},PK&appid={api_key}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data['name'],
                    "weather": data['weather'][0]['description'],
                    "temp": data['main']['temp'],
                    "success": True
                }
        return {"success": False, "error": f"Sorry, I couldn't find the weather for '{city}'."}
    else:
        return {"success": False, "error": f"Error: Unable to fetch weather data (status code {response.status_code})."}

def generate_reply(user_prompt, weather_contents, gemini_api_key):
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    weather_info = "\n".join(
        f"City: {w['city']}, Weather: {w['weather']}, Temperature: {w['temp']}°C"
        for w in weather_contents if w.get("success")
    )
    error_info = "\n".join(
        w['error'] for w in weather_contents if not w.get("success")
    )
    prompt = (
        f"User asked: {user_prompt}\n"
        f"Weather data:\n{weather_info}\n"
        f"{error_info}\n"
        f"Based on the above, generate a helpful, friendly, and informative reply."
    )
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    api_key = "2f399c653c9da2e49cce024d9ecdcbb5"
    gemini_api_key = "AIzaSyAOynelmDcIZsxxtmV1WUXC1ufuDVdnO-o"
    last_prompt = None
    print("Ask anything about the weather (e.g., 'What's the weather in Karachi and Lahore?', 'Tell me if it's raining in Islamabad', etc.)")
    while True:
        user_input = input("Ask about the weather (or type 'exit'): ").strip()
        if user_input.lower() == 'exit':
            break
        if user_input.lower() in ['again', 'repeat', 'same']:
            if last_prompt:
                user_input = last_prompt
            else:
                print("No previous prompt found. Please ask a weather-related question.")
                continue
        if not user_input:
            print("Please enter a weather-related prompt.")
            continue
        last_prompt = user_input
        cities = extract_cities_from_prompt(user_input, gemini_api_key)
        if not cities:
            print("Sorry, I couldn't find any city in your prompt. Please try again.")
            continue
        weather_contents = [get_weather_content(city, api_key) for city in cities]
        print(generate_reply(user_input, weather_contents, gemini_api_key))