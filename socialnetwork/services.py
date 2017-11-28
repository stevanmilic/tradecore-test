from email_hunter import EmailHunterClient
import clearbit

email_hunter_client = EmailHunterClient('8552b3b2908a8f4bc745f7915cd8f393548c475d')
clearbit.key = 'my_key'


def email_exists(email):
    return email_hunter_client.exist(email)[0]


def get_user_additional_data(email):
    """Can't create valid api key...mocking data
    """
    # response = clearbit.Enrichment.find(email=email, stream=True)
    response = {
        'first_name': 'John',
        'last_name': 'Snow'
    }
    return response
