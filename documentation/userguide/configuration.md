# EasyTl documentation

## 1. Obtaining the credentials
For execute the EasyTl you must get API ID, API HASH [here](https://my.telegram.org)

1. Go to the [https://my.telegram.org](https://my.telegram.org) and authorize to it
2. Click to the `API development tools` ([It is here](https://my.telegram.org/apps))
3. Create your "application"
4. Save the API ID and API HASH values

## 2. Editing the `easytl.py` file
For get configured the EasyTl you must open the `easytl.py` and paste there credentials

1. Open the `easytl.py` in any editor. On Windows you can use notepad or any other editor. On Linux you can use "vim" or "nano" also can use any other editor
2. You will see it code:
    ```python
    # There is EasyTl usebot default instance
    
    # How to get API_ID and API_HASH:
    #    - Sign up for Telegram using any application.
    #    - Log in to your Telegram core: https://my.telegram.org.
    #    - Go to "API development tools" and fill out the form.
    #    - You will get basic addresses as well as the api_id and api_hash parameters
    
    # settings
    API_ID    = -1
    API_HASH  = ''
    
    MY_ID     = -1               # ur id from @myidbot
    lang      = 'en'             # language of userbot
    ```
3. Replace **-1** to your **API ID** where `API_ID = -1`. Result must be as `API_ID = 55555555`
4. Insert your **API HASH** inside the quotes where `API_ID = ''`. Result must be as `API_HASH = 'aaaabbbbccccddddeeeeffffgggghhhh'`
5. Go to the [@myidbot](https://t.me/myidbot) and get **your id**
6. Replace **-1** to **your id** where `MY_ID = -1`. Result must be as `MY_ID = 9999999999`
7. As optional, you can change the language of the userbot. To do this, change value in `lang` to this:
   - `en` - English language
   - `ru` - Russian language
   - `ua` - Ukrainian language
   Example of the configured EasyTl (there isn't correct credentials):
   ```python
    # settings
    API_ID    = 55555555
    API_HASH  = 'aaaabbbbccccddddeeeeffffgggghhhh'
    
    MY_ID     = 9999999999       # ur id from @myidbot
    lang      = 'ua'             # language of userbot
    ```
8. Congratulations! You configured the EasyTl and can run it!