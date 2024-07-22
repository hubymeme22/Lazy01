from colorama import init, Fore, Style

APP_DESCRIPTION = 'This app is a simple app for intercepting and analyzing API endpoints for scanning A01:2021 OWASP\'s Broken Authentication common vulnerability'
VERBOSE_DESCRIPTION = 'Increase the console output verbosity'
INTERCEPT_DESCRIPTION = 'Starts interception of HTTP packets on specified port'
FORWARD_DESCRIPTION = 'Forwards the packet to the specified host'
UNIQUE_DESCRIPTION = 'Ignores the same http requests'
PACKET_LOAD_DESCRIPTION = 'Loads the saved recorded packets'
PACKET_CONTINUE_DESCRIPTION = 'Continues the saved recorded packets'
PACKET_SUMMARY_DESCRIPTION = 'Summarizes the loaded packets'
PACKET_METHOD_DESCRIPTION = 'Filters method from the packet loaded'
PACKET_READ_DESCRIPTION = 'Reads the specific contents of the packet'
TEST_REPEAT_DESCRIPTION = 'Tests all the loaded packets and repeats the request'
TEST_STATUS_DESCRIPTION = 'Filters the test status provided, separated by comma (ex: 200,500,404,...)'
TEST_PUBLIC_DESCRIPTION = 'Includes tests for public access'
SET_BEARER_DESCRIPTION = 'Sets one or multiple bearer token value(s) to be tested separated by comma (ex. token1,token2,token3,...).'
GET_BEARER_DESCRIPTION = 'Retrieves all the bearer tokens in a session'
AUTO_BEARER_DESCRIPTION = 'Automatically retrieve all the bearer tokens and sets for testing'

init()
class ConsoleStr:
    def g(string: str=''):
        return Fore.GREEN + string + Style.RESET_ALL

    def b(string: str=''):
        return Fore.BLUE + string + Style.RESET_ALL

    def r(string: str=''):
        return Fore.RED + string + Style.RESET_ALL

    def v(string: str=''):
        return Fore.MAGENTA + string + Style.RESET_ALL

    def y(string: str=''):
        return Fore.YELLOW + string + Style.RESET_ALL

    def green(string: str, end='\n'):
        print(ConsoleStr.g(string), end=end)

    def blue(string: str, end='\n'):
        print(ConsoleStr.b(string), end=end)

    def red(string: str, end='\n'):
        print(ConsoleStr.r(string), end=end)

    def violet(string: str, end='\n'):
        print(ConsoleStr.v(string), end=end)

    def yellow(string: str, end='\n'):
        print(ConsoleStr.y(string), end=end)

ASCII_ART = r'''
 ___       ________  ________      ___    ___             ________    _____     
|\  \     |\   __  \|\_____  \    |\  \  /  /|           |\   __  \  / __  \    
\ \  \    \ \  \|\  \\|___/  /|   \ \  \/  / /___________\ \  \|\  \|\/_|\  \   
 \ \  \    \ \   __  \   /  / /    \ \    / /\____________\ \  \\\  \|/ \ \  \  
  \ \  \____\ \  \ \  \ /  /_/__    \/  /  /\|____________|\ \  \\\  \   \ \  \ 
   \ \_______\ \__\ \__\\________\__/  / /                  \ \_______\   \ \__\
    \|_______|\|__|\|__|\|_______|\___/ /                    \|_______|    \|__|
                                 \|___|/                                        
'''

# I mean, I'm too lazy too, so...
ASCII_ART = ASCII_ART.replace('________    _____', ConsoleStr.y('________    _____') + Fore.GREEN)
ASCII_ART = ASCII_ART.replace(r'|\   __  \  / __  \ ', ConsoleStr.y(r'|\   __  \  / __  \ ') + Fore.GREEN)
ASCII_ART = ASCII_ART.replace(r'\ \  \|\  \|\/_|\  \ ', ConsoleStr.y(r'\ \  \|\  \|\/_|\  \ ') + Fore.GREEN)
ASCII_ART = ASCII_ART.replace(r'\ \  \\\  \|/ \ \  \ ', ConsoleStr.y(r'\ \  \\\  \|/ \ \  \ ') + Fore.GREEN)
ASCII_ART = ASCII_ART.replace(r'\ \  \\\  \   \ \  \ ', ConsoleStr.y(r'\ \  \\\  \   \ \  \ ') + Fore.GREEN)
ASCII_ART = ASCII_ART.replace(' \\ \\_______\\   \\ \\__\\', ConsoleStr.y(' \\ \\_______\\   \\ \\__\\') + Fore.GREEN)
ASCII_ART = ASCII_ART.replace('\\|_______|    \\|__|', ConsoleStr.y('\\|_______|    \\|__|') + Fore.GREEN)
ASCII_ART += ConsoleStr.g('Author: ') + ConsoleStr.v('HowHowBurry@2024') + '\n'
ASCII_ART += ConsoleStr.y('Disclaimer: ') + 'Any use of this application for purposes other than education and research is not endorsed. The developers and contributors of this software are not liable for any misuse or illegal activities performed with this application.'