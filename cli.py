import connection_manager as cm
import cli, connection_manager, utils, message_manager
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout


class Cli:

    def __init__(self, client, messager):
        self.active = True
        self.scale = 60
        self.client = client
        self.messager = messager
        

    def afficher_menu(self):
        self._print_line_equals()  
        print('CryptoSecuritySocialNetwork - CLI'.center(self.scale))
        self._print_line_equals()
        print()
        if self.client.connection_state == True:
            print("[+] Successfully connected to " + self.client.connect_infos[0] + ":" + str(self.client.connect_infos[1]))
        else:
            print('[-] Connexion failed !')
            self.active == False
        print()
        print()
        self._print_line_equals()
        print('AVAILABLE COMMANDS'.center(self.scale))
        self._print_line_equals()
        print()
        print('/help\t\t\t- Show this message')
        print('/quit, /exit, /q\t- Disconnect and exit')
        print('/send <text>\t\t- Send to all clients')
        print('/send -s <text>\t\t- Send to server')
        print('<text>\t\t\t- Send to all clients')
        print('/clear\t\t\t- Clear the terminal')
        self._print_line_equals()
        print()
        print('Type a message and press ENTER to send.')
        print('Type /help to see available commands')
        print()
    def _print_line_equals(self):
        for i in range(self.scale):
            if i != self.scale-1:
                print('=',end='')
            else:
                print('=')
    def _clear_terminal(self):
        print("\033[H\033[J", end="")
    def _parse_cmd(self, cmd : str):
        cmd_tab = cmd.split(" ")
        print(cmd_tab)
        match cmd_tab[0]:
            case '/help':
                self._clear_terminal()
                self.afficher_menu()
            case '/quit' | '/exit' | '/q':
                self.client.close()
            case '/send':
                self.client.send(cmd_tab[1::])
            case '/clear':
                self._clear_terminal()
            case '/health':
                self.client.send(cmd_tab[0])
            case 'task':
                self.client.send(cmd_tab)
            case _:
                self.client.send(cmd_tab)
    def listen_to_user(self):
        with patch_stdout(): #assure que l'ecriture sur le terminal ne se fait pas sur la cli
            raw_cmd = prompt("> ") 
        parsed_cmd = self._parse_cmd(raw_cmd)
        return parsed_cmd
    

