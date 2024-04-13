import os 
import dotenv

dotenv.load_dotenv() 

# --- database part ---

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./database/e_blogger.db"
# can also use other relational database, like postgresql.
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# --- security ---

# jwt secret key.
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'DEFAULT_SECRET_KEY')

# jwt algorithm
JWT_ALGORITHM = 'HS256'

# jwt expire time 
JWT_EXPIRE_TIME = 14

# bcrypt rounds
BCRYPT_ROUNDS = 12

