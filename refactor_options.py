import json

# changes characters and classes from arrays of objects to objects with names as keys

def main():
    old_options = {}
    new_options = { "routes": {}, "characters": {}, "classes": {} }

    with open("options.json") as file:
        old_options = json.loads(file.read())
    # Keep old route structure
    new_options["routes"] = old_options["routes"]
    # Remap characters and classes as key-value pairs of name-unique_to
    for character in old_options["characters"]:
        new_options["characters"][character["name"]] = { "unique_to": character["unique_to"] }
    # Also move all incompatible lists into unique_to as reverse of characters
    character_names = list(new_options["characters"].keys())
    for class_info in old_options["classes"]:
        incompatible = class_info["incompatible"]
        incompatible_reversed = []
        unique_to = class_info["unique_to"]
        if len(incompatible) > 0:
            incompatible_reversed = [character for character in character_names if character not in incompatible]
            unique_to = class_info["unique_to"] + incompatible_reversed if len(class_info["unique_to"]) > 0 else incompatible_reversed
        new_options["classes"][class_info["name"]] = { "unique_to": unique_to }
    
    with open("options_refactored.json", "w") as file:
        file.write(json.dumps(new_options))

if __name__ == "__main__":
    main()