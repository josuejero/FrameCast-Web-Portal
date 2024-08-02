import secrets
import string

alphabet = string.ascii_letters+string.digits
new_filename = ''.join(secrets.choice(alphabet) for _ in range(10))+'.jpg'

print(new_filename)
