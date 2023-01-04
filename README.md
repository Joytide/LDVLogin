# LDVLogin

Just a little script to automate the logging process as well as the validation of the attendance record, because I keep forgetting to confirm my attendance although I'm in class.



#### Deploy

- Install [docker and docker compose](https://docs.docker.com/desktop/install/ubuntu/)

- Run:

```bash
git clone git@github.com:Joytide/LDVLogin.git
cd LDVLogin
cp config.example.py config.py
vim config.py # Add your email and password here
docker compose up --build
```

- Add the following line in your crontab:

``` */5 8-20 * * 1-5 cd /path/to/your/LDVLogin/ ; docker compose up```



And you're all set!



### Development

- Install

```bash
git clone git@github.com:Joytide/LDVLogin.git
cd LDVLogin
```

- Install the requirements with:

```bash
pip3 install -r requirements.txt
```

- Add user, password in ldvlogin.py

- Add the following line in your crontab:

``` */5 8-20 * * 1-5 /usr/bin/python3 /path/to/your/ldvlogin.py```



If you find any bugs or crashes, please open a ticket and join the relevant logs.

Don't hesitate to add tickets for enhancements too!



#### DISCLAIMER: 

**EN**
I am not responsible for the misuse of this script, it isn't in any case a tool to be used to commit attendance fraud. If you are in my school, check the 8.2 section of our Internal Rules for more informations on attendance fraud.

**FR**
Je ne suis pas responsable d'abus d'utilisation de ce script par autrui, il ne devrait en aucun cas être utilisé pour frauder à la présence en ligne. Si vous faites parti de mon école, la section 8.2 du réglement intérieur vous donnera plus d'information sur la fraude à l'appel en ligne.

