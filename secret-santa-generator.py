from random import choice as randchoice


yeses = ("y", "yes", "")


def min_calculator(included_names: dict[str, list[str]]):
    min_name = randchoice(list(included_names))
    for name in included_names:
        if len(included_names[name]) < len(included_names[min_name]):
            min_name = name
    return min_name


def remove_selected_person(
    included_names: dict[str, list[str]], min_name: str, selected_name_for_person: str
) -> dict[str, list[str]]:

    del included_names[min_name]

    for name in included_names:
        if selected_name_for_person in included_names[name]:
            included_names[name].remove(selected_name_for_person)
            _temp = [tuple(included_names[name]) for name in included_names]
            if list(set(_temp)) != _temp:
                included_names[name].append(selected_name_for_person)
    return included_names


def selector(names: list[str], excluded_dict: dict[str, list[str]]) -> dict[str, str]:
    selected_names = {name: "" for name in names}
    included_names = {name: [] for name in names}
    for name in names:
        for other_name in names:
            if (other_name not in excluded_dict[name]) and (other_name != name):
                included_names[name].append(other_name)
    done = False
    while not done:
        min_name = min_calculator(included_names)
        selected_name_for_person = randchoice(included_names[min_name])
        if min_name != selected_names[selected_name_for_person]:
            selected_names[min_name] = selected_name_for_person
            included_names = remove_selected_person(
                included_names, min_name, selected_name_for_person
            )
        if not included_names:
            done = True
    return selected_names


def unique_names(names: list[str]) -> list[str]:
    # Make it unique in case they entered host twice
    return list(set(list(map(lambda x: x.strip().casefold(), names))))


def get_excluded_names(names: list[str]) -> dict[str, list[str]]:
    excluded_dict = {name: [""] for name in names}
    for name in names:
        add_to_excluded_dict = False
        print(
            "Enter the exception list can't gift. (Separate multiple names with commas)."
        )
        while not add_to_excluded_dict:
            excluded_names_for_person = unique_names(
                input(f"{name.title()} can't gift: ").split(",")
            )
            _continue = False
            for excluded_name in excluded_names_for_person:
                if excluded_name.casefold() not in names and (excluded_name != ""):
                    print(
                        f"{excluded_name.title()} not in participants. Participants is/are {', '.join([str(particpant).title() for particpant in names])}. Enter names of people {name.title()} can't gift again"
                    )
                    _continue = True
                    break
            if _continue:
                continue
            if len(unique_names(excluded_names_for_person)) >= (len(names) - 1):
                print(
                    f"Not possible to generate a draw because you have excluded all possibilities for {name}. Enter the names of people {name} can't gift again! :("
                )
            else:
                add_to_excluded_dict = True
        excluded_dict[name] = excluded_names_for_person

        if len(excluded_dict[name]) >= (len(names) - 1):
            print(
                f"Not possible to generate a Secret Santa draw because you have excluded all possibilities for {name.title()}. You need to start over! :("
            )
            start()
    return excluded_dict


def start():
    host_name = input("Enter name of the host: ")
    is_host_participating = (
        True if input(f"Is {host_name} participating? [Y/n] ").casefold() in yeses else False
    )

    names = input(
        "Enter names of people participating. (Separate multiple names with commas, eg: Vishal, Jahnavi,Shaili,Vaishnavi): "
    ).split(",")

    if is_host_participating:
        names = [host_name] + names

    names = unique_names(names)

    exclude_certain_people_from_getting_certain_people = (
        True
        if input(f"Exclude certain people from getting certain people? [Y/n] ").casefold() in yeses
        else False
    )

    if exclude_certain_people_from_getting_certain_people:
        excluded_dict = get_excluded_names(names)

    selected_names = selector(names, excluded_dict)
    print(selected_names)


if __name__ == "__main__":
    print(
        selector(
            ["V", "J", "S"],  # , "Ysh", "P", "H"],
            {
                "V": ["J"],
                "J": ["S"],
                # "P": ["H"],
                "S": ["V"],
                # "Ysh": [],
                # "H": ["P", "Ysh"],
            },
        )
    )

    start()
