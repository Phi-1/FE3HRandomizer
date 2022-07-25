import json
import random
from uuid import uuid4


def load_options(filename: str) -> dict:
    options = {}
    with open(filename) as file:
        options = json.loads(file.read())
    return options

def get_n_characters() -> int:
    while True:
        try:
            n_characters = int(input("Enter amount of characters to generate: "))
            if n_characters != 0 and n_characters <= 36:
                return n_characters
            else:
                print("Number must be between 1 and 36")
        except ValueError:
            print("Not a valid number")

def get_protagonist() -> str:
    while True:
        protagonist = input("Choose protagonist (F/M): ")
        if protagonist == "F" or protagonist == "M":
            return protagonist + "Byleth"
        else:
            print("Protagonist must be F or M")

def get_guarantee_dancer() -> bool:
    while True:
        wants_dancer = input("Guarantee Dancer? (Y/N): ")
        if wants_dancer == "Y" or wants_dancer == "N":
            return True if wants_dancer == "Y" else False

def choose_route(routes: dict) -> tuple:
    route, leader = random.choice(list(routes.items()))
    return (route, leader if leader != "" else None)

def choose_characters(n_characters: int, character_options: dict, route: str) -> list:
    character_names = []
    for i in range(n_characters):
        successful_pick = False
        while not successful_pick:
            character_name = random.choice(list(character_options.keys()))
            if character_name in character_names:
                continue
            if len(character_options[character_name]["unique to"]) > 0 and route not in character_options[character_name]["unique to"]:
                continue
            character_names.append(character_name)
            successful_pick = True
    return character_names

def choose_classes(character_names: list, class_options: dict, guarantee_dancer: bool) -> list:
    characters_classes = []
    dancer = ""
    if guarantee_dancer:
        picked_dancer = False
        while not picked_dancer:
            character_pick = random.choice(character_names)
            if len(class_options["Dancer"]["unique to"]) > 0 and character_pick not in class_options["Dancer"]["unique to"]:
                continue
            dancer = character_pick
            characters_classes.append((character_pick, "Dancer"))
            picked_dancer = True
    for character in character_names:
        if character == dancer:
            continue
        class_picked = False
        while not class_picked:
            class_pick = random.choice(list(class_options.keys()))
            if len(class_options[class_pick]["unique to"]) > 0 and character not in class_options[class_pick]["unique to"]:
                continue
            if class_pick == "Dancer":
                if dancer == "":
                    dancer = character
                else:
                    continue
            characters_classes.append((character, class_pick))
            class_picked = True
    return characters_classes

def save_run(folder: str, route: str, characters_classes: list, classes: dict) -> None:
    with open(f"{folder}/{str(uuid4())}.txt", "w") as file:
        lines = []
        lines.append(f"Route: {route}\n\n")
        for character, class_name in characters_classes:
            lines.append(f"{character}: {class_name}\n")
            if len(classes[class_name]["requirements"]) > 0:
                lines.append("Skill Requirements: \n")
                for skill, level in classes[class_name]["requirements"].items():
                    lines.append(f"\t{skill}: {level}\n")
                lines.append("\n")
            else:
                lines.append("\n")
        file.writelines(lines)


def main():
    options = load_options("options_refactored.json")
    n_characters = get_n_characters()
    protagonist = get_protagonist()
    guarantee_dancer = get_guarantee_dancer()
    random.seed()
    route, leader = choose_route(options["routes"])
    character_names = [protagonist, leader] + choose_characters(n_characters - 2, options["characters"], route)
    characters_classes = choose_classes(character_names, options["classes"], guarantee_dancer)
    save_run("generated", route, characters_classes, options["classes"])

if __name__ == "__main__":
    main()