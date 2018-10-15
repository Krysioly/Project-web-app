<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>

    ###########################################################################





What am I grateful for today?<br>
        <textarea id= "grateful" rows="2" cols="40" placeholder="I am grateful for..."></textarea><br>
        What book/ artwork /music /video inspired me today?<br>
        <textarea id="inspired" rows="2" cols="40" placeholder="I was inspired by..."></textarea><br>
        What did I do to imporve my health (physical/mental)?<br>
        <textarea id= "improved" rows="2" cols="40" placeholder="I improved my health by..."></textarea><br>
        What have I accomplished today?<br>
        <textarea id= "accomplished" rows="2" cols="40" placeholder="I have accomplished..."></textarea><br>


# grateful = request.form.get("grateful")
    # inspired = request.form.get("inspired")
    # improved = request.form.get("improved")
    # accomplished = request.form.get("accomplished")
    
    # text = " ".join([base, grateful, inspired, improved, accomplished])



#################### Weather ############
weather = api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}



{"coord":{"lon":-122.09,"lat":37.39},
"sys":{"type":3,"id":168940,"message":0.0297,"country":"US","sunrise":1427723751,"sunset":1427768967},
"weather":[{"id":800,"main":"Clear","description":"Sky is Clear","icon":"01n"}],
"base":"stations",
"main":{"temp":285.68,"humidity":74,"pressure":1016.8,"temp_min":284.82,"temp_max":286.48},
"wind":{"speed":0.96,"deg":285.001},
"clouds":{"all":0},
"dt":1427700245,
"id":0,
"name":"Mountain View",
"cod":200}

API call:
http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID={APIKEY}
Parameters:
APPID {APIKEY} is your unique API key 

################## Quote ##############3


# These code snippets use an open-source library. http://unirest.io/python


<span style="z-index:50;font-size:0.9em;"><img src="https://theysaidso.com/branding/theysaidso.png" height="20" width="20" alt="theysaidso.com"/><a href="https://theysaidso.com" title="Powered by quotes from theysaidso.com" style="color: #9fcc25; margin-left: 4px; vertical-align: middle;">theysaidso.com</a></span>





##################### Calendar #####################3

calendar.setfirstweekday(6)
    year = ['January','February','March','April','May',
    'June','July','August','September','October',
    'November','December'] 
    today = datetime.datetime.date(datetime.datetime.now())
    current_list = re.split("-", str(today))
    month_num = int(current[1])
    current_month = year[month_num-1]
    current_day = int(current[2])
    current_yr = int(current[0])






 {
    "success": {
        "total": 1
    },
    "contents": {
        "quotes": [
            {
                "quote": "Be daring, be different, be impractical, be anything that will assert integrity of purpose and imaginative vision against the playitsafers, the creatures of the commonplace, the slaves of the ordinary.",
                "length": "201",
                "author": "Cecil Beaton",
                "tags": [
                    "inspire"
                ],
                "category": "inspire",
                "date": "2018-10-08",
                "permalink": "https://theysaidso.com/quote/fFVOORfFvnr1bt5mNNhZtQeF/15328-cecil-beaton-be-daring-be-different-be-impractical-be-anything-that-will-assert",
                "title": "Inspiring Quote of the day",
                "background": "https://theysaidso.com/img/bgs/man_on_the_mountain.jpg",
                "id": "fFVOORfFvnr1bt5mNNhZtQeF"
            }
        ],
        "copyright": "2017-19 theysaidso.com"
    }
}

