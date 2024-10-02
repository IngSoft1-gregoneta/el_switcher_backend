from config.repositorymanager import Base, engine

# Eliminar todas las tablas
Base.metadata.drop_all(bind=engine)

# Recrear todas las tablas con la nueva estructura
Base.metadata.create_all(bind=engine)