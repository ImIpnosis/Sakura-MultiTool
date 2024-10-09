import requests
import time
import threading
import os
import colorama
import random
import webbrowser
import tls_client
from discord.ext import commands
from time import sleep
from json import loads, dumps
import json
import sys
from base64 import b64encode
import logging
from websocket import WebSocket
import httpx
import os
from concurrent.futures import ThreadPoolExecutor
import ctypes
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System, Box
from colorama import Fore

tokens = open('data/tokens.txt', 'r').read().splitlines()

light_magenta = Fore.LIGHTMAGENTA_EX
purple_dark = Fore.LIGHTMAGENTA_EX
light_gray = Fore.LIGHTCYAN_EX
light_blue = Fore.LIGHTBLUE_EX
green = Fore.GREEN
magenta = Fore.MAGENTA
lightmagenta = Fore.LIGHTMAGENTA_EX
white = Fore.WHITE

Locked = f"{light_blue} [LOCKED]? {light_blue}"
Invalid = f"{light_blue} [INVALID]? {light_blue}"
Valid = f"{colorama.Fore.GREEN} [VALID] {colorama.Fore.GREEN}"
NoAcces = f"{light_blue} [NO ACCESS] {light_blue}"
Succes = f"{colorama.Fore.GREEN} [SUCCESS] {colorama.Fore.GREEN}"
RateLimit = f"{colorama.Fore.LIGHTCYAN_EX} [RATELIMIT] {colorama.Fore.LIGHTCYAN_EX}"
Banned = f"{light_blue} [BANNED]? {light_blue}"

class Session:
    def __init__(self):
        self.ja3 = '771,4866-4867-4865-49196-49200-49195-49199-52393-52392-159-158-52394-49327-49325-49326-49324-49188-49192-49187-49191-49162-49172-49161-49171-49315-49311-49314-49310-107-103-57-51-157-156-49313-49309-49312-49308-61-60-53-47-255,0-11-10-35-16-22-23-49-13-43-45-51-21,29-23-30-25-24,0-1-2'
        self.identifier = 'chrome_106'
        self._session = tls_client.Session(            
            client_identifier=self.identifier,
            random_tls_extension_order=True,
            ja3_string=self.ja3)

    def session(self):
        return self._session

class Gateway:
    def __init__(self):
        self.ws = websocket.WebSocket()
    def __connect_ws(self):
        self.ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
    def __identify_ws(self, token):
        payload = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": sys.platform,
                    "$browser": "",
                    "$device": f"{sys.platform} Device"
                },
            },
            "s": None,
            "t": None
        }
        self.ws.send(json.dumps(payload))
    def close_ws(self):
        self.ws.close()
    def get_session_id(self):
      for i in range(5):
        try:recv = self.ws.recv();sessionid = json.loads(recv)['d']['session_id'];return sessionid
        except:pass
      return 
    def return_ws(self):return self.ws
    def run_gateway(self, token):
        self.__connect_ws()
        self.__identify_ws(token)

class DiscordTools:
  def __init__(self):
    self.client_build_num = self.__client_build_num()
    session = Session()
    self.useragent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9013 Chrome/108.0.5359.215 Electron/22.3.2 Safari/537.36'
    self.session = session.session()
    self.__cookies()
  def __headers(self, token):
    return {
      'authority'             : 'discord.com',
      'accept'                : '*/*',
      'accept-language'       : 'it,it-IT;q=0.9',
      'authorization'         : token,
      'content-type'          : 'application/json',
      'origin'                : 'https://discord.com',
      'referer'               : 'https://discord.com',
      'sec-ch-ua'             : '"Not?A_Brand";v="8", "Chromium";v="108"',
      'sec-ch-ua-mobile'      : '?0',
      'sec-ch-ua-platform'    : '"Windows"',
      'sec-fetch-dest'        : 'empty',
      'sec-fetch-mode'        : 'cors',
      'sec-fetch-site'        : 'same-origin',
      'user-agent'            : self.useragent,
      'x-debug-options'       : 'bugReporterEnabled',
      'x-discord-locale'      : 'en-GB',
      'x-super-properties'    : self.__build_super_prop(),
    }
  def __cookies(self):
        self.url = 'https://discord.com'
        r = self.session.get(self.url)
        cs = {};c = r.cookies
        for ck in c:cs[ck.name] = ck.value
        self.cookies = cs
  def __build_super_prop(self):
        webapp_properties = {
            "os"                    :"Windows",
            "browser"               :"Discord Client",
            "release_channel"       :"stable",
            "client_version"        :"1.0.9012",
            "os_version"            :"10.0.19044",
            "os_arch"               :"x64",
            "system_locale"         :"en-GB",
            "client_build_number"   :self.client_build_num,
            "native_build_number"   :32020,
            "client_event_source"   :None,
            "design_id"             :0
        }
        return b64encode(json.dumps(webapp_properties, separators=(',', ':')).encode()).decode()
  def __build_context_prop(self, location :str = "Join Guild",location_guild_id :str = "1090282970474106920",location_channel_id :str = "1090289026533163018",location_channel_type :int = 0,):
        webapp_properties = {"location":location,"location_guild_id":location_guild_id,"location_channel_id":location_channel_id,"location_channel_type":location_channel_type}
        return b64encode(json.dumps(webapp_properties, separators=(',', ':')).encode()).decode()
  def __client_build_num(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0','Accept': '*/*','Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br','Alt-Used': 'discord.com','Connection': 'keep-alive','Referer': 'https://discord.com/','Sec-Fetch-Dest': 'script','Sec-Fetch-Mode': 'no-cors','Sec-Fetch-Site': 'same-origin','Pragma': 'no-cache','Cache-Control': 'no-cache','TE': 'trailers',}
        try:
            html = httpx.get(f"https://discord.com/app?_={(time.time() * 1000)}", headers=headers).text;last_index = html.rfind('/assets/')
            closing_quote_index = html.find('"', last_index);prefetched_script = html[last_index:closing_quote_index]
            response = httpx.get(f'https://discord.com{prefetched_script}', headers=headers).text;buildnum = response.split("buildNumber:\"")[1].split("\"")[0]
            print(Colorate.Horizontal(Colors.green_to_white, 'Discord build number retrived : '+str(buildnum), 1))
            return buildnum
        except:
            print(Colorate.Horizontal(Colors.light_blue_to_white, 'Could not retrieve discord build number.', 1))
            return 185832
  def __fetch_invite(self, invite, headers):
        res = self.session.get('https://discord.com/api/v9/invites/{0}?inputValue={0}&with_counts=true&with_expiration=true'.format(invite),headers=headers,cookies=self.cookies)
        if res.status_code == 200:return res.json()
        else:return
  def __generate_nonce(self, channelid):
        nonce_generated = []
        z = str(channelid)[:len(str(channelid))-5]
        last = str(channelid)[len(str(channelid))-5:]
        for word_last in last:
            x = str(int(word_last) ^ random.randint(500, 1000))[1]
            nonce_generated.append(x)
        z += "".join(nonce_generated)
        return z

def count_lines(file_path):
    with open(file_path, 'r') as file:
        lines_starting_with_mte = sum(1 for line in file if line.strip().startswith("MTE"))
    return lines_starting_with_mte

file_path_tokens = "data/tokens.txt"
total_mte_lines = count_lines(file_path_tokens)

file_path_tokens = "data/tokens.txt"
total_lines = count_lines(file_path_tokens)

class SakuraUI:
  def __init__(self):
    self.discordtools = DiscordTools()
  def run(self):
    System.Clear()

def login():
    while True:
        Write.Print("""
                                         ██╗      ██████╗  ██████╗ ██╗███╗   ██╗
                                         ██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
                                         ██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
                                         ██║     ██║   ██║██║   ██║██║██║╚██╗██║
                                         ███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
                                         ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝
                                       
                                          
        """, Colors.purple_to_blue, interval=0.000)

        desilight_blue_username = Write.Input("Username    | ", Colors.purple_to_blue, interval=0.020)
        password = Write.Input("        Password    | ", Colors.purple_to_blue, interval=0.020)

        if desilight_blue_username != "" and password == "Sakura":
            return desilight_blue_username 
        else:
            print("Incorrect password, try again")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')


sakura = (f"""
███████╗ █████╗ ██╗  ██╗██╗   ██╗██████╗  █████╗ 
██╔════╝██╔══██╗██║ ██╔╝██║   ██║██╔══██╗██╔══██╗
███████╗███████║█████╔╝ ██║   ██║██████╔╝███████║
╚════██║██╔══██║██╔═██╗ ██║   ██║██╔══██╗██╔══██║
███████║██║  ██║██║  ██╗╚██████╔╝██║  ██║██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
                                                         
  Welcome to Sakura Tool, press enter to login!

              Made by Ipnosis & Ethan
         
""")
System.Size(120, 30)
System.Clear()
Anime.Fade(Center.Center(sakura), Colors.purple_to_blue,  Colorate.Vertical, interval=0.040, enter=True)


finger_fail = False
session = requests.Session()

headers = {
        'Accept': '*/*',
        'Referer': 'https://discord.com/',
        'User-Agent': 'Mozilla/5.0'
}
response = session.get('https://discord.com/api/v9/experiments', headers=headers)

if response.status_code == 200:
    data = response.json()
    fingerprint = data["fingerprint"]
else:
    finger_fail = True


if not os.path.exists("data"):
    os.makedirs("data")


file_path = os.path.join("data", "tokens.txt")
if not os.path.exists(file_path):
    with open(file_path, 'w'):
        pass


file_path_logs = os.path.join("data", "logs.txt")
if not os.path.exists(file_path_logs):
    with open(file_path_logs, 'w'):
        pass


discord = "discord.gg/millennium"
file_path_tokens = "data/tokens.txt"
file_path_logs = "data/logs.txt"


log_file_path = "data/logs.txt"

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
msg_sent = 0
msg_failed = 0
msg_ratelimited = 0

def TokenOnliner(self):
    def _online(token,_):
      gateway = Gateway()
      gateway.run_gateway(token)
    for token in tokens:threading.Thread(target= _online, args=(token, True)).start()
    
def main_program():
    username = login()
    while True:
        os.system('cls')
        logging.info("console was clealight_blue")
        
        def title():
            ctypes.windll.kernel32.SetConsoleTitleW(f"EstriperRaider")
        
        def count_lines(file_path):
            with open(file_path, 'r') as file:
                line_count = 0
                for _ in file:
                    line_count += 1
            return line_count
        
        Write.Print(f"logged as: {username}", Colors.purple_to_blue, interval=0.005)
        Write.Print(f"""


                                    ███████╗ █████╗ ██╗  ██╗██╗   ██╗██████╗  █████╗ 
                                    ██╔════╝██╔══██╗██║ ██╔╝██║   ██║██╔══██╗██╔══██╗
                                    ███████╗███████║█████╔╝ ██║   ██║██████╔╝███████║
                                    ╚════██║██╔══██║██╔═██╗ ██║   ██║██╔══██╗██╔══██║
                                    ███████║██║  ██║██║  ██╗╚██████╔╝██║  ██║██║  ██║
                                    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
                                          
        """, Colors.purple_to_blue, interval=0.000)
        logging.info("printed sakura logo")
        
        
        Write.Print(f"""         
                                                    Total tokens: {total_lines} """, Colors.purple_to_blue, interval=0.000)
        print(f'''

                            {Colors.light_blue}[{Colors.light_gray}1{Colors.light_blue}]  Joiner     -     {Colors.light_blue}[{Colors.light_gray}4{Colors.light_blue}]  Reaction adder    -     {Colors.light_blue}[{Colors.light_gray}7{Colors.light_blue}] Token Checker
                            {Colors.light_blue}[{Colors.light_gray}2{Colors.light_blue}]  Leaver     -     {Colors.light_blue}[{Colors.light_gray}5{Colors.light_blue}]  Vc spammer        -     {Colors.light_blue}[{Colors.light_gray}8{Colors.light_blue}] Token Locker
                            {Colors.light_blue}[{Colors.light_gray}3{Colors.light_blue}]  Spammer    -     {Colors.light_blue}[{Colors.light_gray}6{Colors.light_blue}]  Token typer       -     {Colors.light_blue}[{Colors.light_gray}9{Colors.light_blue}] Server lookup 

                                                       {Colors.light_blue}[{Colors.light_gray}10{Colors.light_blue}] Exit 
''')
              
        print(" ")
        choice = int(Write.Input("[Choice?] ", Colors.purple_to_blue, interval=0.020))
        logging.info("printed option chooser")
                
            
        if choice == 0:
            logging.info("chose socials (0)")
            Write.Print('''
Secret option, shhh
[1]Discord             
                  ''', Colors.purple_to_blue, interval=0.020)
            logging.info("printed social options")
            choice_socials = int(input(purple_dark + 
"[>>>]: "))
            logging.info("printed option choser for socials")
            if choice_socials == 1:
                webbrowser.open(discord)
                logging.info("chose discord (socials) (1)")
            else:
                print ("no such option")
                logging.info("put in a option that doesnt exist (socials)")
                
            

 
                
        
        elif choice == 1:
            import concurrent.futures
            import random
            import string
            import tls_client
            from colorama import Fore, Style
            import dtypes


            class Joiner:
                def __init__(self, data: dtypes.Instance) -> None:
                    self.session = data.client
                    self.session.headers = data.headers
                    self.get_cookies()
                    self.instance = data

                def rand_str(self, length: int) -> str:
                    return ''.join(random.sample(string.ascii_lowercase + string.digits, length))

                def get_cookies(self) -> None:
                    site = self.session.get("https://discord.com")
                    self.session.cookies = site.cookies

                def join(self) -> None:
                    self.session.headers.update({"Authorization": self.instance.token})
                    result = self.session.post(f"https://discord.com/api/v9/invites/{self.instance.invite}", json={
                        'session_id': self.rand_str(32),
                    })

                    if result.status_code == 200:
                       print(Succes, light_gray + token[:-5] + "*****", light_gray, )
                       logging.info("joiner succes")
                       title()

                    else:
                        print(NoAcces, light_gray + 'Something went wrong captcha?')

            class logger:
                colors_table = dtypes.OtherInfo.colortable

                @staticmethod
                def printk(text) -> None:
                    print(f"{text}")

                @staticmethod
                def convert(color):
                    return color if color.__contains__("#") else logger.colors_table[color]

                @staticmethod
                def color(opt, obj):
                    return f"{logger.convert(opt)}{obj}{Style.RESET_ALL}"

            class intilize:
                @staticmethod
                def start(i):
                    Joiner(i).join()

            if __name__ == '__main__':
                with open("data/tokens.txt") as file:
                    tokens = [line.strip() for line in file]

                instances = []
                max_threads = 5
                invite = Write.Input("Discord code: ", Colors.purple_to_blue, interval=0.020)
                invite = invite.replace("https://discord.gg/", "").replace("https://discord.com/invite/", "").replace("discord.gg/", "").replace("https://discord.com/invite/", "")
                invite_parts = invite.split("/")

                for token_ in tokens:
                    header = dtypes.OtherInfo.headers
                    instances.append(
                        dtypes.Instance(
                            client=tls_client.Session(
                                client_identifier=f"chrome_{random.randint(110, 115)}",
                                random_tls_extension_order=True,
                            ),
                            token=token_,
                            headers=header,
                            invite=invite,
                        )
                    )

                with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
                    for i in instances:
                        executor.submit(intilize.start, i)
        
        
        elif choice == 2:
            logging.info("chose leaver (2)")
            with open(file_path_tokens, "r") as file:
                tokens = file.read().splitlines()

            guild_id = Write.Input("Guild ID: ", Colors.blue, interval=0.020)
            logging.info("put in guild id (leaver)")

            def leaver(token):
                header = {'Authorization': token}

                url = f"https://discord.com/api/v9/users/@me/guilds/{guild_id}"

                response = requests.delete(url, headers=header)

                if response.status_code == 204:
                    print(Succes, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("leaver succes")
                elif response.status_code == 401:
                    print(Invalid, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("leaver invalid token")
                elif response.status_code == 403:
                    print(Locked, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("leaver locked token")
                else:
                    print(Invalid, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("leaver invalid token")

            threads = []
            for token in tokens:
                thread = threading.Thread(target=leaver, args=(token,))
                thread.start()
                threads.append(thread)
                
            for thread in threads:
                thread.join()

        elif choice == 3:
            global msg_sent
            logging.info("chose spammer (3)")
            with open(file_path_tokens, "r") as file:
                tokens = file.read().splitlines()

            channel_id = Write.Input("Channel ID: ", Colors.purple_to_blue, interval=0.020)
            logging.info("put in channel id")
            message_content = Write.Input("Message: ", Colors.purple_to_blue, interval=0.020)
            logging.info("put in message content")
            repeat_count = int(Write.Input("How many times?: ", Colors.purple_to_blue, interval=0.020))
            logging.info("put in repeat count")
        

            def spammer(token):
                url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
                headers = {'Authorization': token}
                payload = {'content': f'{message_content}'}

                for _ in range(repeat_count):
                    response = requests.post(url, json=payload, headers=headers)
                    if response.status_code == 200:
                        print(Succes, light_gray + token[:-5] + "*****", light_gray, )
                        logging.info("spammer succes")
                        msg_sent =+ 1
                        title()
                    elif response.status_code == 401:
                        print(Invalid, light_gray + token[:-5] + "*****", light_gray, )
                        logging.info("spammer invalid token")
                        msg_failed =+ 1
                        title()
                    elif response.status_code == 429:
                        print(RateLimit, light_gray + token[:-5] + "*****", light_gray, )
                        logging.info("spammer ratelimit (use proxies to bypass)")
                        msg_ratelimited =+ 1
                        title()
                    elif response.status_code == 403:
                        print(Invalid, "/", Banned, light_gray + token[:-5] + "*****", light_gray, )
                        logging.info("spammer invalid or banned token")
                        msg_failed =+ 1
                        title()
                    else:
                        print("Unknown Error", light_gray + token[:-5] + "*****", light_gray, )
                        logging.info("spammer unknown error")

            threads = []
            for token in tokens:
                thread = threading.Thread(target=spammer, args=(token,))
                thread.start()
                threads.append(thread)
                
            for thread in threads:
                thread.join()

        elif choice == 4:
            logging.info("chose reactor (4)")
            with open(file_path_tokens, "r") as file:
                tokens = file.read().splitlines()

            channel_id = Write.Input("Channel ID: ", Colors.purple_to_blue, interval=0.020)
            logging.info("put in channel id")
            message_id = Write.Input("Message ID: ", Colors.purple_to_blue, interval=0.020)
            logging.info("put in message id")
            emoji = Write.Input("Emoji : ", Colors.purple_to_blue, interval=0.020)
            logging.info("put in emoji")

            def reactor(token):
                headers = {'Authorization': token}
                url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"

                response = requests.put(url, headers=headers)
                if response.status_code == 204:
                    print(Succes, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("reactor succes")
                elif response.status_code == 401:
                    print(Invalid, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("reactor invalid token")
                elif response.status_code == 403:
                    print(Locked, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("reactor locked token")
                else:
                    print(Invalid, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("reactor invalid token")

            threads = []
            for token in tokens:
                thread = threading.Thread(target=reactor, args=(token,))
                thread.start()
                threads.append(thread)
                
            for thread in threads:
                thread.join()

        elif choice == 5:
            logging.info("chose reactor (4)")
            with open(file_path_tokens, "r") as file:
                tokens = file.read().splitlines()
            channel = Write.Input("Voice channel ID: ", Colors.purple_to_blue, interval=0.020)
            server = Write.Input("Server id: ", Colors.purple_to_blue, interval=0.020)
            deaf = Write.Input("Defean?: ", Colors.purple_to_blue, interval=0.020)
            if deaf == "y":
                deaf = True
            if deaf == "n":
                deaf = False
            mute = Write.Input("Mute?: ", Colors.purple_to_blue, interval=0.020)
            if mute == "y":
                mute = True
            if mute == "n":
                mute = False
            stream = Write.Input("Stream?: ", Colors.purple_to_blue, interval=0.020)
            if stream == "y":
                stream = True
            if stream == "n":
                stream = False
            video = Write.Input("Video?: ", Colors.purple_to_blue, interval=0.020)
            if video == "y":
                video = True
            if video == "n":
                video = False

            executor = ThreadPoolExecutor(max_workers=int(1000))
            def run(token):
                while True:
                    ws = WebSocket()
                    ws.connect("wss://gateway.discord.gg/?v=8&encoding=json")
                    hello = loads(ws.recv())
                    heartbeat_interval = hello['d']['heartbeat_interval']
                    ws.send(dumps({"op": 2,"d": {"token": token,"properties": {"$os": "windows","$browser": "Discord","$device": "desktop"}}}))
                    ws.send(dumps({"op": 4,"d": {"guild_id": server,"channel_id": channel,"self_mute": mute,"self_deaf": deaf, "self_stream?": stream, "self_video": video}}))
                    ws.send(dumps({"op": 18,"d": {"type": "guild","guild_id": server,"channel_id": channel,"preferlight_blue_region": "singapore"}}))
                    ws.send(dumps({"op": 1,"d": None}))
                    sleep(0.1)

            i = 0

            for token in tokens:
                executor.submit(run, token)
                i+=1
                print(Succes, light_gray + token[:-5] + "*****", light_gray, )
                logging.info("VC joiner succes")
                sleep(0.01)
            yay = Write.Input("                                                                                                                        Press enter to stop VC spammer", Colors.purple_to_blue, interval=0.020)
        

        elif choice == 6:
            logging.info("chose is typing (6)")
            with open(file_path_tokens, "r") as file:
                tokens = file.read().splitlines()

            channel_id = Write.Input("Channel ID: ", Colors.purple_to_blue, interval=0.020)
            logging.info("put in channel id")
            logging.info("put in deleay")
            url = f"https://discord.com/api/v9/channels/{channel_id}/typing"

            def is_typing(token):
                headers = {'Authorization': token}
                response = requests.post(url, headers=headers)

                if response.status_code == 204:
                    print(Succes, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("is typing succes")
                elif response.status_code == 401:
                    print(Invalid, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("is typing invalid token")
                elif response.status_code == 403:
                    print(Locked, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("is typing locked token")
                else:
                    print(Invalid, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("is typing invalid token")

            threads = []
            for token in tokens:
                thread = threading.Thread(target=is_typing, args=(token,))
                thread.start()
                threads.append(thread)
                
            for thread in threads:
                thread.join()

        elif choice == 7:
            logging.info("chose checker (7)")
            with open(file_path_tokens, "r") as file:
                tokens = file.read().splitlines()

            def checker(token):
                url = "https://discord.com/api/v9/users/@me/affinities/guilds"
                headers = {'Authorization': token}
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    print(Valid, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("checker valid token")
                elif response.status_code == 401:
                    print(Invalid, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("checker invalid token")
                elif response.status_code == 403:
                    print(Locked, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("checker locked token")
                else:
                    print(Invalid, light_gray + token[:-5] + "*****", light_gray, )
                    logging.info("checker invalid token")

            threads = []
            for token in tokens:
                thread = threading.Thread(target=checker, args=(token,))
                thread.start()
                threads.append(thread)
                
            for thread in threads:
                thread.join()

        elif choice == 8:
            logging.info("chose token locker (8)")
            with open(file_path_tokens, "r") as file:
                tokens = file.read().splitlines()
            Write.Print("ARE U SURE U WANT TO **LOCK** ALL THE TOKENS IN TOKENS.TXT? y/n", Colors.purple_to_blue, interval=0.020)
            token_locker_confirm = Write.Input("[>>>]: ", Colors.purple_to_blue, interval=0.020)
            
            def token_locker(token):
                if token_locker_confirm == "y" or "Y":
                    logging.info("Token locker was confirmed")
                    logging.info("token locking has started")
                    Write.Print("Reccomend using like 2-3 times to make sure tokens are locked", Colors.purple_to_blue, interval=0.020)
                    payload = {"bio": "."}
                    headers = {'Authorization': token}
                    url = "https://discord.com/api/v9/users/%40me/profile"
                    response = requests.patch(url, json=payload, headers=headers)

                    if response.status_code == 200:
                        print(Succes, light_gray + token[:-5] + "*****", light_gray, )
                        logging.info("token locker succes")
                    elif response.status_code == 401:
                        print(Invalid, light_gray + token[:-5] + "*****", light_gray, )
                        logging.info("token locker invalid token")
                    elif response.status_code == 403:
                        print(Locked, light_gray + token[:-5] + "*****", light_gray, )
                        logging.info("token locker locked token")
                    else:
                        print(Invalid, light_gray + token[:-5] + "*****", light_gray, )
                        logging.info("token locker invalid token")

                    threads = []
                    for token in tokens:
                        thread = threading.Thread(target=token_locker, args=(token,))
                        thread.start()
                        threads.append(thread)
                        
                    for thread in threads:
                        thread.join()


        elif choice == 9:

                headers = {
                    'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
                    'Authorization' : Write.Input("Token: ", Colors.purple_to_blue, interval=0.020)
                }

                guildId = Write.Input("Server id: ", Colors.purple_to_blue, interval=0.020)

                response = requests.get(
                    f"https://discord.com/api/guilds/{guildId}",
                    headers = headers,
                    params = {"with_counts" : True}
                ).json()

                owner = requests.get(
                    f"https://discord.com/api/guilds/{guildId}/members/{response['owner_id']}",
                    headers = headers,
                    params = {"with_counts" : True}
                ).json()

                print(f"""
{Colors.green}####### Server Information #######
[{Colors.light_blue}Name]      $:   {response['name']} 
[{Colors.light_blue}ID]        $:   {response['id']}
[{Colors.light_blue}Owner]     $:   {owner['user']['username']}#{owner['user']['discriminator']} 
[{Colors.light_blue}Owner ID]  $:   {response['owner_id']}
[{Colors.light_blue}Members]   $:   {response['approximate_member_count']}
[{Colors.light_blue}Region]    $:   {response['region']}
[{Colors.light_blue}Icon URL]  $:   https://cdn.discordapp.com/icons/{guildId}/{response['icon']}.webp?size=256
""")
                sleep(15)

        elif choice == 10:
            logging.info("exited (10)")
            exit()

        else:
            print("No such option")
            logging.info("put in an option that doesn't exist")

        Write.Print("Clearing in 3s", Colors.purple_to_blue, interval=0.020)
        time.sleep(3)
        logging.info("clealight_blue")


if __name__ == "__main__":
    main_program()