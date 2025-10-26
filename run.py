#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NWTECH TOOLS - Ferramenta Profissional de Assistência Técnica
Arquivo principal de execução
"""

import sys
import os

# Garante que o diretório src está no path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from src.gui.main_window import TechAssistApp

def main():
    """Função principal da aplicação"""
    print("Iniciando TechAssist...")
    app = TechAssistApp()
    app.mainloop()

if __name__ == "__main__":
    main()
