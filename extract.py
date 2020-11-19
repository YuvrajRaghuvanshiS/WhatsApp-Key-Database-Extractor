from non_essentials.colors import Colors

banner = open('non_essentials\\banner.txt','r')
banner_content = banner.read()
print(Colors.OKGREEN + Colors.BOLD + banner_content + Colors.ENDC)
banner.close()