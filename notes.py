bobs hashed password = 6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090





<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>

###########################################################################
<!-- <form action="/search-category" name="radioCat">
        <input type="radio" name="radioCat" value="business">Business
        <input type="radio" name="radioCat" value="entertainment">Entertainment
        <input type="radio" name="radioCat" value="health">Health
        <input type="radio" name="radioCat" value="science">Science
        <input type="radio" name="radioCat" value="sports">Sports
        <input type="radio" name="radioCat" value="technology">Technology
        <input type="submit" id="searchcat" value="search category" class="btn btn-dark"></form> -->



<div>
    <!-- <h2>Daily Quote</h2>
    <p>  
    {
    { quote }}  </p> -->
    

   <!--  <h2>Weather</h2>
    <img src="
    {
    { img_src }}" id="weather-icon">
    <p><b>Weather: </b><br>
    
    {
    { weathers["main"] }}<br>
    <b>Tempurature: </b><br>
    Current: 
    {
    { weathers["temp"] }}F<br>
    High: 
    {
    { weathers["temp_min"] }}F<br>
    Low: 
    {
    { weathers["temp_max"] }}F
    </p> -->
</div>



// function changeNewsCat(results) 
{
//     console.log(results);
//     $('#categorynews').html(results);
// }

// function updateNewsCat(evt) 
{
//     evt.preventDefault();

//     let searchCat = 
{'category' : $('radioCat').val(),};
//     console.log(searchCat)
    
//     $.get("/search-category", searchCat ,changeNewsCat);
// }

// $('#searchcat').on('click', updateNewsCat);

//////////////////////////////////////

# def get_news():
    """ news api """

    # /v2/everything
    # all_articles = newsapi.get_everything(q='technology',
                                      #     sources='bbc-news,the-verge',
                                      # domains='bbc.co.uk,techcrunch.com',
                                      # language='en',
                                      # sort_by='relevancy')

#     # news = requests.get("https://newsapi.org/v2/sources?language=en&country=us&apiKey="+news_key)
#     # news_json = news.text
#     news_json = open("news.json").read()
#     news_info = json.loads(news_json)
#     news_list = news_info['sources']

    # return all_articles




@app.route("/search-category")
def search_category():
    newscategory = request.args.get('radioCat') 

    top_headlines = newsapi.get_top_headlines(
        q=None, sources=None, category=newscategory,
        language='en', country='us')
    # news_info = json.loads(top_headlines)
    # print("\n\n",news_info,"\n\n")
    # news_list = news_info['articles']

    return jsonify(top_headlines)




    # print("\n\n",all_articles,"\n\n")
    # articles = all_articles["articles"]
    # dictionary = 
    {}
    # i=0
    # for article in articles:
    #     print("\n\n\naritcle\n",article,"\n\n")
    #     dictionary[i] = article
    #     i=i+1



>>> dir(calendar)
['Calendar', 'EPOCH', 'FRIDAY', 'February', 'HTMLCalendar',
 'IllegalMonthError',    'IllegalWeekdayError', 'January',
 'LocaleHTMLCalendar', 'LocaleTextCalendar', '   MONDAY',
 'SATURDAY', 'SUNDAY', 'THURSDAY', 'TUESDAY', 'TextCalendar',
 'WEDNESDAY   ', '_EPOCH_ORD', '__all__', '__builtins__', 
 '__cached__', '__doc__', '__file__',    '__loader__', 
 '__name__', '__package__', '__spec__', '_colwidth', '_locale',
 '_   localized_day', '_localized_month', '_spacing', 'c',
 'calendar', 'datetime', 'da   y_abbr', 'day_name', 
 'different_locale', 'error', 'firstweekday', 'format', 
 'for   matstring', 'isleap', 'leapdays', 'main', 'mdays', 
 'month', 'month_abbr', 'month   _name', 'monthcalendar', 
 'monthrange', 'prcal', 'prmonth', 'prweek', 'repeat', 
 'setfirstweekday', 'sys', 'timegm', 'week', 'weekday', 
 'weekheader']


<table border="0" cellpadding="0" cellspacing="0" class="month">
<tr><th colspan="7" class="month">October 2018</th></tr>
<tr><th class="sun">Sun</th><th class="mon">Mon</th><th class="tue">Tue</th><th class="wed">Wed</th><th class="thu">Thu</th><th class="fri">Fri</th><th class="sat">Sat</th></tr>
<tr><td class="noday">&nbsp;</td><td class="mon">1</td><td class="tue">2</td><td class="wed">3</td><td class="thu">4</td><td class="fri">5</td><td class="sat">6</td></tr>
<tr><td class="sun">7</td><td class="mon">8</td><td class="tue">9</td><td class="wed">10</td><td class="thu">11</td><td class="fri">12</td><td class="sat">13</td></tr>
<tr><td class="sun">14</td><td class="mon">15</td><td class="tue">16</td><td class="wed">17</td><td class="thu">18</td><td class="fri">19</td><td class="sat">20</td></tr>
<tr><td class="sun">21</td><td class="mon">22</td><td class="tue">23</td><td class="wed">24</td><td class="thu">25</td><td class="fri">26</td><td class="sat">27</td></tr>
<tr><td class="sun">28</td><td class="mon">29</td><td class="tue">30</td><td class="wed">31</td><td class="noday">&nbsp;</td><td class="noday">&nbsp;</td><td class="noday">&nbsp;</td></tr>
</table>






<div class="md-col-6">
<div id="earnings-before open" class="col-12 md-col-12 inline-block align-top" style="break-after: page;">
<div class="py1 border-box m2 border-top-light undefined">
<div style="border-top: 0px solid rgb(187, 187, 187);">
<h2 class="mt0 undefined" style="font-size: 20px;">
<!-- react-text: 1120 -->Earnings Before Open<!-- /react-text -->
<sup></sup></h2>
<div>
<div class="clearfix py1">
<a class="border-box bg-none no-underline-on-hover" href="/apps/stocks/T" style="min-width: 30%; height: auto;">
<div class="col-12 rounded transition-100 shadow-inset-on-hover-light" style="background: rgb(248, 248, 248); height: 100%; vertical-align: top;">
<div class="flex">
<div class="px2 pt2 relative flex flex-1 col-12 flex-column border-box">
<div class="block flex">
<div class="block flex-column">
<h3 class="medium-text bold mt0 mb0 top-0 nowrap flex flex-column flex-1" style="line-height: 1; color: rgb(34, 34, 34);">T</h3>
<p class="smallest-text col-10 flex-column flex mb0 mt0" style="color: rgb(34, 34, 34);">AT&amp;T Inc.</p>
</div>
<div class="flex-1 flex-column">
<p class="medium-text mt0 bold nowrap mb0 flex-column right-align" style="line-height: 1; color: rgb(34, 34, 34);">0.93</p>
<p class="small-text nowrap bold mb0 right-align" style="color: rgb(25, 190, 135);">+25.68% yoy</p>
</div></div></div></div>
<div class="flex pt1 pb2 flex-justify-content">
<div class="px2 flex flex-1 border-box">
<div class="block flex flex-1">
<p class="small-text nowrap bold mb0 flex-1" style="color: rgb(34, 34, 34);"></p></div></div>
<div class="px2 flex flex-1 border-box">
<div class="block flex flex-1">
<p class="smallest-text mt0 mb0 uppercase flex-1 right-align" style="color: rgb(68, 68, 68);">Estimated EPS</p>
</div></div></div></div></a></div></div>







