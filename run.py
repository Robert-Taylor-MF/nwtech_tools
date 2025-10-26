#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NWTECH TOOLS - Ferramenta Profissional de Assistência Técnica
Arquivo principal de execução
"""

import sys
import os
from tkinter import messagebox

# Garante que o diretório src está no path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """Função principal da aplicação"""
    try:
        # Importa após adicionar ao path
        from src.modules.admin_helper import is_admin
        from src.gui.main_window import TechAssistApp
        
        # Avisa se não estiver como administrador
        if not is_admin():
            print("⚠️ AVISO: Programa não está sendo executado como Administrador")
            print("   Algumas funcionalidades do Winget podem não funcionar corretamente.")
            print("   Recomenda-se executar como Administrador.\n")
        
        print("Iniciando NWTECH TOOLS...")
        app = TechAssistApp()
        app.mainloop()
        
    except Exception as e:
        print(f"Erro ao iniciar o programa: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
