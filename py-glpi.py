import json
from glpi import GLPI
from glpi import GlpiProfile
from glpi import GlpiTicket, Ticket

url = ""
user = ""
password = ""
token = ""

glpi = GLPI(url, token, (user, password))


print "Getting all Tickets: "
print json.dumps(glpi.get_all('ticket'),
                  indent=4,
                  separators=(',', ': '),
                  sort_keys=True)