# 🔧 NWTECH TOOLS - Ferramenta Profissional de Assistência Técnica

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Ferramenta completa para técnicos de informática, com backup automático, gerenciador visual do Winget, ferramentas de diagnóstico e geração de relatórios profissionais.

## ✨ Funcionalidades

### 🗂️ Backup & Restore Inteligente
- Backup automático de documentos, desktop, downloads, fotos, vídeos e músicas
- Backup de dados de navegadores (Chrome, Firefox, Edge)
- Validação de integridade com checksums MD5
- Restauração completa pós-formatação
- Logs detalhados de todas as operações

### 📦 Gerenciador Visual do Winget
- Interface gráfica moderna para o Windows Package Manager
- Catálogo organizado por categorias
- Perfis de instalação pré-configurados (Básico, Escritório, Gamer, Desenvolvedor)
- Instalação em lote de múltiplos programas
- Instalação silenciosa sem interação do usuário

### 🛠️ Ferramentas de Diagnóstico (Em Desenvolvimento)
- Integração com HWiNFO64, CPU-Z, GPU-Z
- Testes de hardware (RAM, CPU, GPU, disco)
- Limpeza e otimização do sistema

### 📄 Gerador de Relatórios (Em Desenvolvimento)
- Relatórios profissionais de serviço
- Histórico de clientes
- Exportação em PDF

## 🚀 Instalação

### Requisitos
- Windows 10/11
- Python 3.10 ou superior
- Winget (Windows Package Manager)

### Passo a Passo

1. Clone o repositório:
git clone https://github.com/seu-usuario/tech-assist.git
cd tech-assist

2. Crie um ambiente virtual:
python -m venv venv
venv\Scripts\activate

3. Instale as dependências:
pip install -r requirements.txt

4. Execute o programa:
python src/main.py

## 📦 Criar Executável

Para criar um arquivo .exe standalone:

pip install pyinstaller
pyinstaller --onefile --windowed --name NWTECHTOOLS src/main.py

O executável estará em `dist/NWTECHTOOLS.exe`

## 🎯 Uso

1. **Backup**: Selecione o destino e clique em "Iniciar Backup"
2. **Restore**: Selecione a pasta do backup e confirme a restauração
3. **Winget**: Escolha programas individualmente ou instale um perfil completo
4. **Ferramentas**: Acesse utilitários de diagnóstico e manutenção

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

Robert Taylor - [@Robert-Taylor-MF](https://github.com/Robert-Taylor-MF)

## 📧 Contato

Para suporte ou dúvidas: robertylhon@gmail.com

## ⭐ Agradecimentos

- Comunidade Python
- Desenvolvedores do CustomTkinter
- Todos os contribuidores do projeto

---
