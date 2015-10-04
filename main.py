print "loading graph... please wait..."
import query as q
import re
import pprint

result = []

def menu():
    state = True
    while(state):
        input = raw_input('> ')
        cmd = re.split('"([^"]*)"+', input)
        command = [] if input != '' else ['nothing']
        for c in cmd:
            if not c.strip() == '':
                command.append(c.strip())
        state = process_input(command)

def process_input(user_input):
    action = user_input[0]
    if action in cmd_map.keys():
        return cmd_map[action](user_input[1::])
    return True

def quit(list):
    return False

def help(list):
    print """

        gernal usage of commands: <cmd> "param1" ... "paramn"

        commands:
        help - shows this help

        find_person - finds a person by matching name (find_person "name")
        find_politican - finds a politican by matching name (find_politican "name")
        find_organization - finds a organization by matching name (find_organization "name")
        find_party - finds a party by matching name (find_party "name")

        network - shows the egozentric network of given entity, level can also be specifed
                  (network "name" ["level"])
        connection - finds a connection between two entites if available,
                     level can also be specifed
                     (connection "entity" "target" ["level"])

        doner_of - shows all doners of given party (doner_of "name")
        donated - show all donation the given organization made (doneted "name")

        plot - renders last result as graph
        list - prints last result as list

        quit - exit programm
    """
    return True

def plot(list):
    q.plot(result)
    return True

def list(list):
    pprint.pprint(result)
    return True

def find_person(param):
    global result
    if len(param) > 0:
        result = q.find_person(param[0])
        results_info(result)
    else:
        print "missing persons name"
    return True

def find_politican(param):
    global result
    if len(param) > 0:
        result = q.find_politican(param[0])
        results_info(result)
    else:
        print "missing politican name"
    return True


def results_info(result):
    print "your query returned %i results" % len(result)
    print "type plot or list to display your results"


def find_organization(param):
    global result
    if len(param) > 0:
        result = q.find_organization(param[0])
        results_info(result)
    else:
        print "missing organizations name"
    return True

def find_party(param):
    global result
    if len(param) > 0:
        result = q.find_party(param[0])
        results_info(result)
    else:
        print "missing party name"
    return True

def find_entity(param):
    global result
    if len(param) > 0:
        result = q.find_person(param[0])
        results_info(result)
    else:
        print "missing entity name"
    return True

def network(param):
    global result
    if len(param) == 1:
        result = q.network_entity_level(param[0])
        results_info(result)
    elif len(param) > 1:
        result = q.network_entity_level(param[0], int(param[1]))
        results_info(result)
    else:
        print "missing entity name and depths (default 1)"
    return True

def connection(param):
    global result
    if len(param) == 2:
        result = q.connection(param[0], param[1])
        results_info(result)
    elif len(param) > 2:
        result = q.connection(param[0], param[1], int(param[2]))
        results_info(result)
    else:
        print "missing entity and/or target name and depths (default 1)"
    return True

def doner_of(param):
    global result
    if len(param) > 0:
        result = q.entity_object_relation(param[0], "org:donation")
        results_info(result)
    else:
        print "missing party name"
    return True

def donated(param):
    global result
    if len(param) > 0:
        result = q.entity_subject_relation(param[0], "org:donation")
        results_info(result)
    else:
        print "missing organization name"
    return True

cmd_map = {
    "quit": quit,
    "help": help,
    "plot": plot,
    "list": list,
    "find_person": find_person,
    "find_politican": find_politican,
    "find_organization": find_organization,
    "find_party": find_party,
    "find_entity": find_entity,
    "network": network,
    "connection": connection,
    "doner_of": doner_of,
    "donated": donated
}

print "welcome"
print "Type in a query. Examples: "
print "network \"Angela Merkel\" "
print "doner_of \"FDP\" "
print "find_organisation \"ag\" "
print "find_person \"angela m\" "
print "enter help for the complete user guide."
menu()
