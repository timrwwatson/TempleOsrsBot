import requests
import json
import logging
import os


FILE_LOCATION = "src/conf/time.output"
resp_test = b'{"data":[{"Username":"Saltysyra","Date":"2022-12-16 09:29:12","Skill":"Smithing","Type":"Skill","Xp":5000000},{"Username":"Consumption","Date":"2022-12-16 08:49:25","Skill":"General Graardor","Type":"Pvm","Xp":300},{"Username":"Lukezz","Date":"2022-12-15 23:17:05","Skill":"Hitpoints","Type":"Skill","Xp":90000000},{"Username":"Cookiehcake","Date":"2022-12-15 22:59:40","Skill":"Dagannoth Rex","Type":"Pvm","Xp":1300},{"Username":"Cookiehcake","Date":"2022-12-15 22:59:40","Skill":"Dagannoth Supreme","Type":"Pvm","Xp":1300},{"Username":"Cookiehcake","Date":"2022-12-15 22:59:40","Skill":"KreeArra","Type":"Pvm","Xp":1000},{"Username":"Syraspecial","Date":"2022-12-15 22:33:08","Skill":"Alchemical Hydra","Type":"Pvm","Xp":100},{"Username":"Top V1","Date":"2022-12-15 20:53:37","Skill":"Dagannoth Rex","Type":"Pvm","Xp":1900},{"Username":"Top V1","Date":"2022-12-15 20:53:37","Skill":"Dagannoth Supreme","Type":"Pvm","Xp":1800},{"Username":"Cinderal","Date":"2022-12-15 19:13:43","Skill":"Zulrah","Type":"Pvm","Xp":100},{"Username":"Vlk1ng","Date":"2022-12-15 17:43:22","Skill":"King Black Dragon","Type":"Pvm","Xp":1300},{"Username":"Top V1","Date":"2022-12-15 17:41:29","Skill":"Alchemical Hydra","Type":"Pvm","Xp":1600},{"Username":"Consumption","Date":"2022-12-15 17:33:24","Skill":"General Graardor","Type":"Pvm","Xp":200},{"Username":"Lukezz","Date":"2022-12-15 13:23:33","Skill":"Nex","Type":"Pvm","Xp":900},{"Username":"Confusedgali","Date":"2022-12-15 10:00:49","Skill":"Ehp","Type":"Skill","Xp":300},{"Username":"Confusedgali","Date":"2022-12-15 10:00:49","Skill":"Clue_medium","Type":"Pvm","Xp":200},{"Username":"Confusedgali","Date":"2022-12-15 10:00:49","Skill":"Wintertodt","Type":"Pvm","Xp":100},{"Username":"Waldroni","Date":"2022-12-15 06:56:00","Skill":"Attack","Type":"Skill","Xp":5000000},{"Username":"Cinderal","Date":"2022-12-15 06:31:50","Skill":"Mining","Type":"Skill","Xp":15000000},{"Username":"Top V1","Date":"2022-12-15 00:31:23","Skill":"Dagannoth Supreme","Type":"Pvm","Xp":1700},{"Username":"Top V1","Date":"2022-12-15 00:31:23","Skill":"Thermonuclear Smoke Devil","Type":"Pvm","Xp":3400},{"Username":"Top V1","Date":"2022-12-15 00:31:23","Skill":"Ranged","Type":"Skill","Xp":45000000},{"Username":"Top V1","Date":"2022-12-15 00:31:23","Skill":"Dagannoth Prime","Type":"Pvm","Xp":1700},{"Username":"Top V1","Date":"2022-12-14 13:02:43","Skill":"KreeArra","Type":"Pvm","Xp":100},{"Username":"The Nevster","Date":"2022-12-14 12:40:09","Skill":"Strength","Type":"Skill","Xp":25000000}]}'
resp_test2 = b'{"data":[{"Username":"Saltysyra1","Date":"2022-12-16 09:29:13","Skill":"Smithing1","Type":"Skill","Xp":5000001},{"Username":"Consumption","Date":"2022-12-16 08:49:25","Skill":"General Graardor","Type":"Pvm","Xp":300},{"Username":"Lukezz","Date":"2022-12-15 23:17:05","Skill":"Hitpoints","Type":"Skill","Xp":90000000},{"Username":"Cookiehcake","Date":"2022-12-15 22:59:40","Skill":"Dagannoth Rex","Type":"Pvm","Xp":1300},{"Username":"Cookiehcake","Date":"2022-12-15 22:59:40","Skill":"Dagannoth Supreme","Type":"Pvm","Xp":1300},{"Username":"Cookiehcake","Date":"2022-12-15 22:59:40","Skill":"KreeArra","Type":"Pvm","Xp":1000},{"Username":"Syraspecial","Date":"2022-12-15 22:33:08","Skill":"Alchemical Hydra","Type":"Pvm","Xp":100},{"Username":"Top V1","Date":"2022-12-15 20:53:37","Skill":"Dagannoth Rex","Type":"Pvm","Xp":1900},{"Username":"Top V1","Date":"2022-12-15 20:53:37","Skill":"Dagannoth Supreme","Type":"Pvm","Xp":1800},{"Username":"Cinderal","Date":"2022-12-15 19:13:43","Skill":"Zulrah","Type":"Pvm","Xp":100},{"Username":"Vlk1ng","Date":"2022-12-15 17:43:22","Skill":"King Black Dragon","Type":"Pvm","Xp":1300},{"Username":"Top V1","Date":"2022-12-15 17:41:29","Skill":"Alchemical Hydra","Type":"Pvm","Xp":1600},{"Username":"Consumption","Date":"2022-12-15 17:33:24","Skill":"General Graardor","Type":"Pvm","Xp":200},{"Username":"Lukezz","Date":"2022-12-15 13:23:33","Skill":"Nex","Type":"Pvm","Xp":900},{"Username":"Confusedgali","Date":"2022-12-15 10:00:49","Skill":"Ehp","Type":"Skill","Xp":300},{"Username":"Confusedgali","Date":"2022-12-15 10:00:49","Skill":"Clue_medium","Type":"Pvm","Xp":200},{"Username":"Confusedgali","Date":"2022-12-15 10:00:49","Skill":"Wintertodt","Type":"Pvm","Xp":100},{"Username":"Waldroni","Date":"2022-12-15 06:56:00","Skill":"Attack","Type":"Skill","Xp":5000000},{"Username":"Cinderal","Date":"2022-12-15 06:31:50","Skill":"Mining","Type":"Skill","Xp":15000000},{"Username":"Top V1","Date":"2022-12-15 00:31:23","Skill":"Dagannoth Supreme","Type":"Pvm","Xp":1700},{"Username":"Top V1","Date":"2022-12-15 00:31:23","Skill":"Thermonuclear Smoke Devil","Type":"Pvm","Xp":3400},{"Username":"Top V1","Date":"2022-12-15 00:31:23","Skill":"Ranged","Type":"Skill","Xp":45000000},{"Username":"Top V1","Date":"2022-12-15 00:31:23","Skill":"Dagannoth Prime","Type":"Pvm","Xp":1700},{"Username":"Top V1","Date":"2022-12-14 13:02:43","Skill":"KreeArra","Type":"Pvm","Xp":100},{"Username":"The Nevster","Date":"2022-12-14 12:40:09","Skill":"Strength","Type":"Skill","Xp":25000000}]}'

class Achievement():
    def __init__(self, entry: dict):
        self.username = entry["Username"]
        self.date = entry["Date"]
        self.skill = entry["Skill"]
        self.type = entry["Type"]
        self.xp = f'{entry["Xp"]:,}'

    def __eq__(self, other):
        return self.username == other.username and self.date == other.date and self.skill == other.skill and self.type == other.type and self.xp == other.xp

    def __repr__(self) -> str:
        rtn_str = f"{self.username}"
        if self.type == "Pvm" and not("Clue" in self.skill):
            rtn_str += f" has reached {self.xp} in {self.skill} kills!" 
        elif self.type == "Pvm" and ("Clue" in self.skill):
            idx = self.skill.find("Clue_") + 5
            rtn_str += f" has completed {self.xp} {self.skill[idx:]} clues!" 
        elif self.type == "Skill" and ("Ehp" in self.skill):
            rtn_str += f" has reached {self.xp} EHP" 
        elif self.type == "Skill" and not ("Ehp" in self.skill):
            rtn_str += f" has reached {self.xp} xp in {self.skill}!" 
        return rtn_str

class TempleOsrs():
    
    def __init__(self, id: str="1955"):
        self.id = id
        self.__last_current_achievements = []
        self.logger = logging.getLogger("TempleOsrs")

    def get_cc_current_achievements(self, debug: bool=False) -> list:
        if not debug:
            resp = requests.get("https://templeosrs.com/api/group_achievements.php", params={'id':self.id})
            if resp.ok:
                items = self.__parse_achievements(resp.content)
                return self.__compare_new_current_achievements(items)
            else:
                self.logger.error(f"Request to templeosrs failed with status code: {resp.status_code} with reason: {resp.reason}")
                return []
        else:

            resp = resp_test
            items = self.__parse_achievements(resp)
            items = self.__compare_new_current_achievements(items)
            for item in items:
                print(item)
            print("\n\n\n\n")
            resp = resp_test2
            print(resp)
            items = self.__parse_achievements(resp)
            items = self.__compare_new_current_achievements(items)
            for item in items:
                print(item)

        
    def __parse_achievements(self, response: str) -> list:
        # first convert from binary
        try:
            response = json.loads(response.decode())
            items = []
            # print(response["data"])
            for x in response["data"]:
                items.append(Achievement(x))
            return items
        except Exception as e:
            self.logger.error(f"Api response can't be decoded with error: {e}")

    def __read_time_file(self, time_file:str=FILE_LOCATION)->str:
        time = ""
        print(os.getcwd())
        with open(time_file, "r") as tf:
            time = tf.readline()
            time.strip()
        return time
    
    def __write_time_file(self,time:str, time_file:str=FILE_LOCATION)->None:
        with open(time_file, "w") as tf:
            tf.write(time)

    def __compare_new_current_achievements(self, new_current: list)-> list:
        new_list = []
        new_current_list = []
        time = self.__read_time_file()
        
        if new_current[0].date <= time:
            # Nothing to do, no new elements
            pass
        else:
            self.__write_time_file(new_current[0].date)
            for achiev in new_current:
                if achiev not in self.__last_current_achievements and achiev.date > time:
                    new_list.append(achiev)
                    new_current_list.append(achiev)
                elif len(new_list) < 20:
                    new_current_list.append(achiev) 
            # we only want to print NEW achievements, but we want to keep track of all of the ones the api
            # will return to us, so the next time we poll, we don't print ones we have already printed!
            self.__last_current_achievements = new_current_list
        return new_list



if __name__ == "__main__":
    TO = TempleOsrs()
    TO.get_cc_current_achievements(debug=True)