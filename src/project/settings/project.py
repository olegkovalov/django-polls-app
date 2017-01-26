import environ


env = environ.Env()


POLLS_FROM_EMAIL = env.str('POLLS_FROM_EMAIL', default='no-reply@example.com')
