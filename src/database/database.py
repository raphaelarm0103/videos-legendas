from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexão MySQL: atualize as credenciais de acordo com o seu banco de dados
DATABASE_URL = "mysql+pymysql://raphael:raphael123@localhost:3306/legendafacil"

# Criação do motor e sessão
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para definir as classes do ORM
Base = declarative_base()


# Função para criar as tabelas no banco de dados
def create_tables():
    Base.metadata.create_all(bind=engine)
