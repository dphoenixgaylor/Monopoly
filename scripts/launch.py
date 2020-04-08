from dependencies import colored

print(colored("""
|\  /| |‾‾‾| |\  | |‾‾‾| |‾‾‾| |‾‾‾| |    |   |
| \/ | |   | | \ | |   | |___| |   | |    |___|
|    | |___| |  \| |___| |     |___| |___   |

         P H O E N I X   E D I T I O N      \n""", "red"))

print(colored("Welcome!", "magenta"))
exec(open("scripts\\initialize_parameters.py").read())