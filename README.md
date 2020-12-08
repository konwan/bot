# Tools:   
  - Python 3.5    
  - Selenium, Beautifulsoup4    
  - [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)  

# Prepare:
1. https server     
   * [Ngrok](https://ngrok.com/)- tunnel local ports to public URLs and inspect traffic    
   $ brew cask install ngrok    
   $ ngrok http -auth="username:password" port       
   * [Heroku](https://dashboard.heroku.com/apps)
2. [Google Apps Script(GSA)](https://developers.google.com/apps-script/overview#your_first_script)   
以 Javascript 為基準所開發出的語言。可用來操作 Google Docs, Sheets, Forms。   
發佈 web apps，單獨或嵌入 google sites    
與其他 Google 服務互動，包含 AdSense、Analytics、Calendar、Drive、Gmail、Maps    



# Steps:   
1. [get access_token and set IP whitelist](https://developers.line.me/ba/ip)      
2. add line_access_token and line_channel_secret(.bash_profile/config.ini)    
export LINE_CHANNEL_ACCESS_TOKEN='Your line channel access token'   
export LINE_CHANNEL_SECRET='Your line channel secret'   
echo $LINE_CHANNEL_SECRET

# Reference      
1. [Ngrok  intro](https://tenten.co/blog/how-to-use-ngrok-to-connect-your-localhost/)       
2. [GAS intro](http://white5168.blogspot.tw/2017/02/line-bot-2-line-messaging-api-v2-google.html#.WMdKChJ969u)      
3. [Google App Engine](https://spreadcode.blogspot.tw/2017/02/google-app-enginepythonline-bot.html)
