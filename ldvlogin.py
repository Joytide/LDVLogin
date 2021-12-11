# LDVLogin by Joytide (09/2021)

#### DISCLAIMER:

# **EN**
# I am not responsible for the misuse of this script, it isn't in any case a tool to be used to commit attendance fraud. 
# If you are in my school, check the 8.2 section of our Internal Rules for more informations on attendance fraud.

# **FR**
# Je ne suis pas responsable d'abus d'utilisation de ce script par autrui, 
# il ne devrait en aucun cas être utilisé pour frauder à la présence en ligne. 
# Si vous faites parti de mon école, la section 8.2 du réglement intérieur vous 
# donnera plus d'information sur la fraude à l'appel en ligne.

# USAGE:
# 1. Install the requirements with pip3 install -r requirements.txt
# 2. Add user, password and script path in the crontab and just under this comments
# 3. Change and add the following line in your crontab for checks every 5 minutes: ($ crontab -e)
# */5 8-20 * * 1-6 /usr/bin/python3 /path/to/your/ldvlogin.py

user = ""           # TO CHANGE 
passwd = ""         # TO CHANGE 
logfile= "./.ldvlogs/ldvlogs.log"

import os, sys

if not os.path.exists("./.ldvlogs"):
    os.makedirs("./.ldvlogs")

try:
    from loguru import logger
except Exception as e:
    print("You are missing loguru, please run pip3 install -r requirements.txt")
    with open(logfile,"a+") as f:
        f.write("You are missing loguru, please run pip3 install -r requirements.txt")


if sys.stdout.isatty():
    logger.remove()
    logger.add(sys.stdout, colorize=True, format="<green>{time}</green> |<level>{level}</level>| <level>{message}</level>")
    logger.add(logfile, rotation="200 MB", format="<green>{time}</green> | <level>{level}</level> | <level>{message}</level>")
    logger.debug("Running manual check...")
else:
    logger.remove()
    logger.add(logfile, rotation="200 MB", format="<green>{time}</green> | <level>{level}</level> | <level>{message}</level>")
    logger.debug("Cronjob doing its job...")


user_agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"

try:
    import requests
    import json
    import lxml
    import re
    import bs4 as BeautifulSoup
except Exception as e:
    logger.critical("Missing package: "+str(e)+", have you installed the requirements?")
    exit(0)

class Course():
    @logger.catch
    def __init__(self,class_row) -> None:
        status = class_row["class"]
        if len(status)==1:
            self.status=status[0]
        else:
            self.status="later"
        els=class_row.findChildren("td" , recursive=False)
        for i in range(len(els)):
            #print("###",i,str(els[i]))
            if i==0:
                self.time=els[i].find(text=True)
                if not self.time:
                    self.time = "[No time]"
            elif i==1:
                self.name=els[i].find(text=True)
                if not self.name:
                    self.name = "[No name]"
            elif i==2:
                self.teacher=els[i].find(text=True)
                if not self.teacher:
                   self.teacher="[No teacher]"
            elif "student" in str(els[i]):
                try:
                    self.releve_link = "https://www.leonard-de-vinci.net" + re.findall(r"(href=\")(/student/presences/[0-9]+)\"",str(els[i]))[0][1]
                    self.id = re.findall(r"(href=\")(/student/presences/[0-9]+)\"",str(els[i]))[0][1].split("/")[-1]
                except:
                    logger.error("Error while finding releve link or id")
                    self.releve_link,self.id="",""
            elif "devinci-online.zoom.us" in str(els[i]):
                try:
                    self.zoom_link = re.findall(r"(https://devinci-online\.zoom\.us/.+?pwd=[a-zA-Z0-9]+)(\")",str(els[i]))[0][0]
                except:
                    self.zoom_link=""
                    logger.error("Error while finding zoom link for this course")
        try:
            print(self,end="")
        except:
            logger.error("Error while displaying course")


    @logger.catch
    def set_presence(self,session):
        d={"act":"set_present","seance_pk":self.id}
        res = session.post("https://www.leonard-de-vinci.net/student/presences/upload.php",data=d)
        return res


    @logger.catch
    def __str__(self) -> str:
        logger.info("Course: "+self.name+" with "+self.teacher)
        logger.info("Course Status: "+self.status)
        logger.info("Course time: "+self.time.replace(" ",""))
        return  ""


@logger.catch
def login_status(session):
    res=session.get("https://www.leonard-de-vinci.net")
    if "Mot de passe" in res.text:
        return False
    elif "Mon compte" in res.text:
        return True
    else:
        logger.critical("ERROR in login status")
        return None


@logger.catch
def login(session):

    res = session.post("https://www.leonard-de-vinci.net/ajax.inc.php",
        data="act=ident_analyse&login="+user,
        headers={"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"})
    try:
        lssop_endpoint = re.findall(r"\/lssop\/[a-z0-9]*/.*@edu\.devinci\.fr",res.text)[0]
    except:
        logger.critical("Unknown user")
        exit(0)
    res = session.get("https://www.leonard-de-vinci.net" + lssop_endpoint, allow_redirects=False)
    SAMLRequest = re.findall(r"(\?SAMLRequest=)(.*)\">",res.text)[0][1]
    res = session.post("https://adfs.devinci.fr/adfs/ls?SAMLRequest="+SAMLRequest.replace("&amp;","&"),
    data = {"UserName": user , "Password" : passwd, "AuthMethod" : "FormsAuthentication"},)
    try:
        lssop_endpoint_2 = re.findall(r"(name=\"RelayState\" value=\")(https://www\.leonard-de-vinci\.net/lssop/[0-9a-z]*)\"",res.text)[0][1]
    except:
        logger.critical("Wrong user/password combination")
        exit(0)
    SAMLResponse = re.findall(r"(name=\"SAMLResponse\" value=\")(.*)(\" /><input)",res.text)[0][1]
    res = session.get(lssop_endpoint_2)
    m = session.post("https://www.leonard-de-vinci.net/include/SAML/module.php/saml/sp/saml2-acs.php/devinci-sp", data = {"SAMLResponse": SAMLResponse})
    if login_status(session):
        logger.success("Logged in as "+user)
    else:
         logger.error("Error while logging in!")

    return session


@logger.catch
def list_classes(session):
    res=session.get("https://www.leonard-de-vinci.net/student/presences/")
    soup = BeautifulSoup.BeautifulSoup(res.text,"lxml")
    body_presences = soup.find("tbody", {"id": "body_presences"})
    courses=[]
    if body_presences:
        classes_row = body_presences.findChildren("tr" , recursive=False)
        for class_row in classes_row:
            try:
                courses.append(Course(class_row=class_row))
            except:
                logger.critical("Error while creating course object")
    else:
        if "Pas de cours" in res.text:
            logger.info("No classes today!")
    return courses


@logger.catch
def main():
    session = requests.Session()
    session.headers.update({"User-Agent": user_agent})
    session = login(session)
    if login_status(session):
        courses = list_classes(session)

        for course in courses:
            if course.status=="warning":
                res = session.get(course.releve_link)
                if "pas encore ouvert" in res.text:
                    logger.info("Course is ongoing but attendance record isn't up")
                elif "Vous avez été noté" in res.text:
                    logger.info("Already set presence")
                else:
                    res = course.set_presence(session)
                    if res.status_code==200:
                        logger.success("You're logged in!")
                    else:
                        logger.error("Uhoh, there was an error setting your presence")
                        print(res.status_code,res.text)

if __name__ == "__main__":
    main()
