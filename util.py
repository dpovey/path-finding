from colorama import Fore, Style, init

PATH_CHARS=list('<>`,/\\^V')

init()

def dump(map, args):
  for row in map:
    if args.colorize:
        for col in row:
            if (col == 'X'):
                print(Style.NORMAL + Fore.RED + col, end='')
            elif (col == 'S'):
                print(Style.BRIGHT + Fore.CYAN + col, end='')
            elif (col == 'O'):
                print(Style.BRIGHT + Fore.YELLOW + col, end='')
            elif (col in PATH_CHARS):
                print(Style.BRIGHT + Fore.GREEN + col, end='') 
            else:
                print(Style.RESET_ALL + col, end='')
            if args.space:
               print(Style.RESET_ALL + ' ', end='')
        print(Style.RESET_ALL)
    else:   
        print((' ' if args.space else '').join(row))

