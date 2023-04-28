import requests
import weather_apikey
from weather_apikey import headers

# Station ID for request
station_id = 'USW00013874'

# Data types 
data_types = 'ANN-TAVG-NORMAL,ANN-PRCP-NORMAL,ANN-SNOW-NORMAL,DJF-TAVG-NORMAL,MAM-TAVG-NORMAL,SON-TAVG-NORMAL,JJA-TAVG-NORMAL'

# API request to retrieve the data
response = requests.get(f'https://www.ncei.noaa.gov/access/services/data/v1?dataset=normals-annualseasonal&stations={station_id}&startDate=1991-01-01&endDate=2020-12-31&dataTypes={data_types}&format=json', headers = headers)
# Check if the request was successful using 200 status code
if response.status_code == 200:
    # Extracts data from response
    data = response.json()
    # Prints data
    print(data)
else:
    print('Failed to retrieve data. Status code:', response.status_code)
