from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from icecream import ic
from termcolor import colored
from keyboard import press
from time import sleep as wait
from random import uniform as randfloat
from os import system as cmd

monkeyhackjs = """
document.querySelector("h1.text").innerText = "MONKEYHACK"
document.querySelector("h1.text").style = "color: red;"
"""

print(colored("MONKEYHACK", "red"))
print(colored("Now loading...", "yellow"))


driver = webdriver.Firefox()
print(colored("Webdriver Created.", "yellow"))

class Tools:
    def __init__(self, driver: webdriver.Firefox):
        self.driver = driver
    
    def get_children_from_parent(self, parent: WebElement) -> list[WebElement]:
        return parent.find_elements(By.XPATH, "./*")  # Selects all children
    
    def get_word_from_wordel(self, wordel: WebElement) -> str:
        word = ""
        for letterel in self.get_children_from_parent(wordel):
            word += letterel.text
        return word
    
    def get_delayrange(self) -> tuple[float, float]:
        try:
            delayrange = open("delayrange.txt").readlines()[1] # skip first line which is a comment
        except KeyError:
            delayrange = open("delayrange.txt").readlines()[0] # fallback to first line if the comment was deleted
        delayrange = delayrange.split(",")
        delayrange_start = eval(delayrange[0])
        delayrange_end = eval(delayrange[1])
        
        return (delayrange_start, delayrange_end)
    
    def get_words(self) -> list[str]:
        print("Reading words...")
        wordels: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, ".word")
        words = []
        for wordel in wordels:
            words.append(self.get_word_from_wordel(wordel=wordel))
        
        sanitizedwords = []
        for word in words:
            if word != "":
                sanitizedwords.append(word)
        
        return sanitizedwords

    def form_sentence_from_list(self, words: list[str]):
        sentence: str = ""
        for word in words:
            sentence += f"{word} "
        return sentence
    

    def auto(self):
        sentence: str = self.form_sentence_from_list(self.get_words()) # monkeytype cheat (sentence)
        delayrange: tuple[float] = self.get_delayrange()
        
        print(colored("Starting to type!", "light_green"))
        print(colored(f"Detected sentence: {sentence}", "green"))
        print(colored(f"Detected delay: {delayrange[0]}-{delayrange[1]}"))
        
        wait(3)
        for letter in sentence:
            print(colored(f"Pressing {letter},", "cyan"))
            press(letter)
            wait(randfloat(delayrange[0], delayrange[1]))
        print(colored("Finished typing!", "green"))
        cmd("pause")
    
    def static_auto(self):
        sentence: str = self.form_sentence_from_list(self.get_words()) # monkeytype cheat (sentence)
        delay: float = self.get_delayrange()[0]
        
        print(colored("Starting to type!", "light_green"))
        print(colored(f"Detected sentence: {sentence}", "green"))
        print(colored(f"Detected delay: {delay}"))
        
        wait(3)
        for letter in sentence:
            print(colored(f"Pressing {letter},", "cyan"))
            press(letter)
            wait(delay)
        print(colored("Finished typing!", "green"))
        cmd("pause")
    
    def no_delay_auto(self):
        sentence: str = self.form_sentence_from_list(self.get_words()) # monkeytype cheat (sentence)
        
        print(colored("Starting to type!", "light_green"))
        print(colored(f"Detected sentence: {sentence}", "green"))
        
        wait(3)
        for letter in sentence:
            print(colored(f"Pressing {letter},", "cyan"))
            press(letter)
        print(colored("Finished typing!", "green"))
        cmd("pause")
        
        




tools = Tools(driver=driver)
driver.get("https://monkeytype.com/login")
input("Please log in...")
print("Logged in...\nAttaching to monkeytype.")
driver.get("https://monkeytype.com")
driver.execute_script(monkeyhackjs)
print("Successfully injected.")

prompt = """
Select an option:
-[1]- Read Words
-[2]- Auto
-[3]- (STATIC) Auto
-[4]- (NO DELAY) Auto
-[9]- Exit
"""

try:
    while True:
        cmd("cls")
        print(colored("**FINS MONKEYHACK**", "red"))
        match input(prompt):
            case "1":
                ic(tools.get_words())
                cmd("pause")
            case "2":
                print(colored("Starting AUTO!", "green"))
                tools.auto()
            case "3":
                if input(colored("WARNING: Static Auto MAY be detected. It does not use changing patterns.\nType Y to continue.\n", "red")).lower() == "y":
                    tools.static_auto()
                else:
                    pass
            case "4":
                if input(colored("WARNING: NO DELAY Auto is likely to not save. It goes way to fast.\nType Y to continue.\n", "red")).lower() == "y":
                    tools.no_delay_auto()
                else:
                    pass
            case "9":
                print(colored("Closing browser...", "light_red"))
                driver.quit()
                print(colored("Bye!", "light_red"))
                quit()
                
except KeyboardInterrupt:
    print(colored("Closing browser...", "light_red"))
    driver.quit()