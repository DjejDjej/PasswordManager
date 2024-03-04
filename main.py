from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from managing_databases import create_database,open_database


def main():
    commands = ["quit","create","open"]
    command_completer = WordCompleter(commands, ignore_case=True)

    while True:
        user_input = prompt("Enter command: ", completer=command_completer)
        if user_input.lower() == "quit":
                print("Exiting...")
                break

        elif user_input.lower() == "create":
                create_database("entry")

        elif user_input.lower() == "open":
                openned_database = open_database("entry")
                database_handle_loop(openned_database)
                


        else:
            print("Wrong command bro")


def database_handle_loop(openned_database):
    commands = ["quit","create","delete","view"]
    command_completer = WordCompleter(commands, ignore_case=True)
    print("you are now in database")
    while True:
        user_input = prompt("Enter command for handling database: ", completer=command_completer)
        if user_input.lower() == "quit":
                print("Exiting...")
                break

        elif user_input.lower() == "view":
            print(openned_database)


if __name__ == "__main__":
    main()