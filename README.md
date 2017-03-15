#Prepare:
1. https server     
   * [Ngrok](https://ngrok.com/)- tunnel local ports to public URLs and inspect traffic    
   $ brew cask install ngrok    
   $ ngrok http -auth="username:password" port       
   * [Heroku](https://dashboard.heroku.com/apps)

#Intro:   
[Google Apps Script(GSA)](https://developers.google.com/apps-script/overview#your_first_script)   
以 Javascript 為基準所開發出的語言。可用來操作 Google Docs, Sheets, Forms。   
發佈 web apps，單獨或嵌入 google sites    
與其他 Google 服務互動，包含 AdSense、Analytics、Calendar、Drive、Gmail、Maps    


#Tools:   
  Python 3.5    
  Selenium, Beautifulsoup4    
  [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)    


#Steps:   
1. add line_access_token and line_channel_secret(.bash_profile)    
export LINE_CHANNEL_ACCESS_TOKEN='Your line channel access token'   
export LINE_CHANNEL_SECRET='Your line channel secret'   
echo $LINE_CHANNEL_SECRET

#Reference      
[ngrok  intro](https://tenten.co/blog/how-to-use-ngrok-to-connect-your-localhost/)
