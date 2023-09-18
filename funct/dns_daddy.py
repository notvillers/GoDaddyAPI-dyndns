from godaddypy import Client, Account
import sys

# DEF: GoDaddy API
def daddy_api(d_key, d_secret, d_domain, d_type, d_record, d_ip_got):
    global userAccount
    userAccount = Account(api_key = d_key, api_secret = d_secret)
    global userClient
    userClient = Client(userAccount)
    global updateResult
    summary_cli = ""
    try:
        # Gets current GoDaddy IP
        currentIP = userClient.get_records(d_domain, record_type = d_type, name = d_record)
        # Updates GoDaddy's IP to the stored one
        if (d_ip_got != currentIP[0]["data"]):
            updateResult = userClient.update_record_ip(d_ip_got, d_domain, d_record, d_type)
        if updateResult is True:
            summary_cli = "Updated DNS record to: " + d_ip_got
        else:
           summary_cli = "Checked the DNS record, no update needed."
    except:
        summary_cli = str(sys.exc_info()[1])
    return summary_cli