import sys
import os

# Garante que os imports funcionem independente de onde o script for executado
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.connection import inicializar_banco
from views.menu import tela_inicial, menu_principal


def main():
    inicializar_banco()
    usuario = tela_inicial()
    if usuario:
        menu_principal(usuario)


if __name__ == '__main__':
    main()
