from non_essentials.colors import Colors

try:
    banner = open('non_essentials\\banner.txt','r')
    banner_content = banner.read()
    print(Colors.OKGREEN + Colors.BOLD + banner_content + Colors.ENDC)
    banner.close()
    print(Colors.UNDERLINE + Colors.OKGREEN + 'WhatsApp Key / Database Extrator on non-rooted Android' + Colors.ENDC)
except FileNotFoundError : 
    print('WhatsApp Key / Database Extrator on non-rooted Android')