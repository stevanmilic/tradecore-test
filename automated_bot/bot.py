"""Script for an automated bot, testing social network.
A more cleaner solution is possible, but it has been written very fast,
so certain things may seem confusing. A program with main function should be
implemented, but for now this seems to work
"""
import configparser
import random

from email_hunter import EmailHunterClient
from faker import Faker
from faker.providers import internet
import requests

config = configparser.ConfigParser()
config.read('config.ini')

email_hunter_client = EmailHunterClient(config['DEFAULT']['EmailHunterKey'])

fake = Faker()
fake.add_provider(internet)


def signup(email):
    user = {
        'username': fake.user_name(),
        'password': fake.password(),
    }

    response = requests.post(
        config['API']['BaseUrl'] + 'users/',
        data={
            'username': user['username'],
            'password': user['password'],
            'email': email
        }
    )

    if response.status_code != 201:
        exit('Error...')

    return user


def signup_users(number_of_users):
    users = email_hunter_client.search('google.com')
    return [signup(users[i]['value']) for i in range(number_of_users)]


def login(user):
    response = requests.post(
        config['API']['BaseUrl'] + 'login/',
        data={
            'username': user['username'],
            'password': user['password']
        }
    )

    if response.status_code != 200:
        exit('Error...')

    return response.json()


def login_users(users):
    return [login(user) for user in users]


def post(token):
    response = requests.post(
        config['API']['BaseUrl'] + 'posts/',
        headers={'Authorization': 'JWT ' + token['token']},
        data={
            'text': fake.text()
        }
    )

    if response.status_code != 201:
        exit('Error...')

    return response.json()


def max_post(tokens, max_posts_per_user):
    for token in tokens:
        for i in range(random.randint(1, max_posts_per_user)):
            post(token)


def get_posts(token):
    response = requests.get(
        config['API']['BaseUrl'] + 'posts/',
        headers={'Authorization': 'JWT ' + token['token']}
    )

    if response.status_code != 200:
        exit('Error...')

    return response.json()


def get_users():
    response = requests.get(
        config['API']['BaseUrl'] + 'users/'
    )

    if response.status_code != 200:
        exit('Error...')

    return response.json()


def get_user(post):
    response = requests.get(
        config['API']['BaseUrl'] + 'users/' + str(post['user']) + '/'
    )

    if response.status_code != 200:
        exit('Error...')

    return response.json()


def get_post_likes(post_id, token):
    response = requests.get(
        config['API']['BaseUrl'] + 'posts/' + str(post_id) + '/',
        headers={'Authorization': 'JWT ' + token['token']}
    )

    if response.status_code != 200:
        import ipdb
        ipdb.set_trace()
        exit('Error...')

    return response.json()['number_of_likes']


def like(post, token):
    response = requests.post(
        config['API']['BaseUrl'] + 'posts/' + str(post['id']) + '/like/',
        headers={'Authorization': 'JWT ' + token['token']}
    )

    if response.status_code != 200:
        exit('Error...')

    return response.json()


def get_random(exclude, max_number):
    """Faster solution is possible...
    """
    r = random.randint(0, max_number)
    while r in exclude:
        r = random.randint(0, max_number)
    return r


signed_up_users = signup_users(int(config['DEFAULT']['NumberOfUsers']))
print(signed_up_users)

users_tokens = login_users(signed_up_users)

max_post(users_tokens, int(config['DEFAULT']['MaxPostsPerUser']))

users = get_users()
posts = get_posts(users_tokens[0])
min_likes = 0
max_likes_per_user = int(config['DEFAULT']['MaxLikesPerUser'])

while min_likes == 0 and users:
    print('Working...')

    user_to_like_index = users.index(max(users, key=lambda user: len(user['posts'])))
    user_to_like = users.pop(user_to_like_index)
    user_to_like_token = users_tokens.pop(user_to_like_index)

    i = 0
    random_likes = []
    while i < max_likes_per_user:
        random_post_id = get_random(random_likes, len(posts) - 1)
        random_user = get_user(posts[random_post_id])

        if random_user['id'] != user_to_like['id'] and min(get_post_likes(post_id, user_to_like_token) for post_id in random_user['posts']) == 0:
            like(posts[random_post_id], user_to_like_token)
            random_likes.append(random_post_id)
            i += 1

    posts = get_posts(user_to_like_token)
    min_likes = min(post['number_of_likes'] for post in posts)


for post in posts:
    print(str(post['id']) + ': ' + str(post['number_of_likes']))
