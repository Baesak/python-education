#! /usr/bin/env bash

content=$(curl 'http://api.openweathermap.org/data/2.5/weather?lat=49.9923181&lon=36.2310146&units=metric&appid=a74f0a3859261fcdbcf295bc2bb61013')

description=$(echo $content | jq '.weather[0].description')
feels_like=$(echo $content | jq '.main.feels_like')
temp=$(echo $content | jq '.main.temp')
temp_max=$(echo $content | jq '.main.temp_max')
temp_min=$(echo $content | jq '.main.temp_min')
wind=$(echo $content | jq '.wind.speed')
city=$(echo $content | jq '.name')

echo -e "City: $city\nWeather description is: $description\nTemperature:$temp, feels like:$feels_like, max temperature:$temp_max, min temperature:$temp_min\nWind speed: $wind" > /home/$(whoami)/weather"


# crontab:
# 0 7 * * * /home/bogdan/scripts/weather.sh
