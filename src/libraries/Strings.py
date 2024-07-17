from colorama import init, Fore, Style

APP_DESCRIPTION = 'This app is a simple app for intercepting and analyzing API endpoints for scanning A01:2021 OWASP\'s Broken Authentication common vulnerability'
VERBOSE_DESCRIPTION = 'Increase the console output verbosity'
INTERCEPT_DESCRIPTION = 'Starts interception of HTTP packets on specified port'
UNIQUE_DESCRIPTION = 'Ignores the same http requests'
PACKET_LOAD_DESCRIPTION = 'Loads the saved recorded packets'
PACKET_SUMMARY_DESCRIPTION = 'Summarizes the loaded packets'
PACKET_METHOD_DESCRIPTION = 'Filters method from packet summary'
PACKET_READ_DESCRIPTION = 'Reads the specific contents of the packet'
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
# ASCII_ART += ConsoleStr.v('HowHowBurry@2024') + '\n'
ASCII_ART += ConsoleStr.y('Disclaimer: ') + 'Any use of this application for purposes other than education and research is not endorsed. The developers and contributors of this software are not liable for any misuse or illegal activities performed with this application.'