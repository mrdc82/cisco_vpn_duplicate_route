**Clear duplicate route on VPN firewall**

When a user is connected via Cisco VPN Anyconnect, if the user moves to another location (ssid) without terminating their current connection, the users
static ip gets a second route.

In a distributed vpn environment where routes are balanced across different asa's.

The script takes input of affected user, and the users ip, and does a show ip route, it then takes the routes ip addresses, and determines
which of the distributed firewalls the users connection resides on, by searching for the route on the fw's config backups.

The user can then select which route they would like to terminate, so that only one route exists for the user, and they can gain network access.
Script logs onto that firewall, and logs off the users connection.

