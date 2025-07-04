import sys
import subprocess

def create_migration(message: str):
    """Cria uma nova migração com uma mensagem."""
    command = ["alembic", "revision", "--autogenerate", "-m", message]
    subprocess.run(command, check=True)

def upgrade_database():
    """Aplica as migrações pendentes."""
    command = ["alembic", "upgrade", "head"]
    subprocess.run(command, check=True)

def main():
    if len(sys.argv) < 2:
        print("Uso: python manage.py [create|upgrade] [mensagem]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("Você precisa fornecer uma mensagem: python manage.py create 'mensagem'")
            sys.exit(1)
        message = sys.argv[2]
        create_migration(message)
    elif command == "upgrade":
        upgrade_database()
    else:
        print(f"Comando desconhecido: {command}")
        print("Comandos disponíveis: create, upgrade")
        sys.exit(1)

if __name__ == "__main__":
    main()
