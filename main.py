import cli, connection_manager, utils, message_manager, threading, time

CONNECTION = True
ADDRESS = 'vlbelintrocrypto.hevs.ch'
PORT = 6000

my_client = connection_manager.Client()
my_client.connect(ADDRESS, PORT)
messager = message_manager.MessageHandler(my_client)
terminal = cli.Cli(my_client, messager)

def ecoute_serveur():
    while my_client.connection_state:
        data = my_client.receive()
        if data is not None:
            messager.add_data(data)
            messager.afficher_messages()
        time.sleep(0.01)

if my_client.connection_state == True:
    terminal.afficher_menu()
    thread_ecoute = threading.Thread(target=ecoute_serveur, daemon=True) #daemon: le thread s'arrete tout seul a la fin du programme
    thread_ecoute.start()
    while my_client.connection_state:
        cmd = terminal.listen_to_user()