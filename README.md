# LDVLogin

Just a little script to automate the logging process as well as the validation of the attendance record, because I keep forgetting to confirm my attendance although I'm in class.



#### Usage

- Install the requirements with:

```bash
pip3 install -r requirements.txt
```

- Add user, password in ldvlogin.py

- Add the following line in your crontab:

``` */5 8-20 * * 1-5 /usr/bin/python3 /path/to/your/ldvlogin.py```



#### TODO:

- Add mail client for warning if a attendance submission fails
- Add a way to bypass in case I'm not attending a class on purpose (and cleanly storage this info)

- Intelligently cron at midnight and recall the script only during class hour (and cleanly storage the time)

#### DISCLAIMER:
**EN**
I am not responsible for the misuse of this script, it isn't in any case a tool to be used to commit attendance fraud. If you are in my school, check the 8.2 section of our Internal Rules for more informations on attendance fraud.

**FR**
Je ne suis pas responsable d'abus d'utilisation de ce script par autrui, il ne devrait en aucun cas être utilisé pour frauder à la présence en ligne. Si vous faites parti de mon école, la section 8.2 du réglement intérieur vous donnera plus d'information sur la fraude à l'appel en ligne.

