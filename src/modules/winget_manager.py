import subprocess
import json

class WingetManager:
    def __init__(self):
        self.software_catalog = {
            "Navegadores": [
                {"name": "Google Chrome", "id": "Google.Chrome"},
                {"name": "Mozilla Firefox", "id": "Mozilla.Firefox"},
                {"name": "Microsoft Edge", "id": "Microsoft.Edge"},
                {"name": "Brave Browser", "id": "Brave.Brave"},
                {"name": "Opera GX", "id": "Opera.OperaGX"}
            ],
            "Comunicação": [
                {"name": "WhatsApp Desktop", "id": "WhatsApp.WhatsApp"},
                {"name": "Discord", "id": "Discord.Discord"},
                {"name": "Zoom", "id": "Zoom.Zoom"},
                {"name": "Microsoft Teams", "id": "Microsoft.Teams"},
                {"name": "Slack", "id": "SlackTechnologies.Slack"},
                {"name": "Telegram Desktop", "id": "Telegram.TelegramDesktop"}
            ],
            "Produtividade": [
                {"name": "LibreOffice", "id": "TheDocumentFoundation.LibreOffice"},
                {"name": "Adobe Acrobat Reader", "id": "Adobe.Acrobat.Reader.64-bit"},
                {"name": "Notepad++", "id": "Notepad++.Notepad++"},
                {"name": "Microsoft PowerToys", "id": "Microsoft.PowerToys"},
                {"name": "Notion", "id": "Notion.Notion"},
                {"name": "Obsidian", "id": "Obsidian.Obsidian"}
            ],
            "Multimídia": [
                {"name": "VLC Media Player", "id": "VideoLAN.VLC"},
                {"name": "Spotify", "id": "Spotify.Spotify"},
                {"name": "OBS Studio", "id": "OBSProject.OBSStudio"},
                {"name": "Audacity", "id": "Audacity.Audacity"},
                {"name": "GIMP", "id": "GIMP.GIMP"},
                {"name": "ShareX", "id": "ShareX.ShareX"},
                {"name": "HandBrake", "id": "HandBrake.HandBrake"}
            ],
            "Utilitários": [
                {"name": "7-Zip", "id": "7zip.7zip"},
                {"name": "WinRAR", "id": "RARLab.WinRAR"},
                {"name": "Everything Search", "id": "voidtools.Everything"},
                {"name": "TreeSize Free", "id": "JAM-Software.TreeSize.Free"},
                {"name": "Revo Uninstaller", "id": "RevoUninstaller.RevoUninstaller"},
                {"name": "CCleaner", "id": "Piriform.CCleaner"},
                {"name": "TeraCopy", "id": "CodeSector.TeraCopy"}
            ],
            "Desenvolvimento": [
                {"name": "Visual Studio Code", "id": "Microsoft.VisualStudioCode"},
                {"name": "Git", "id": "Git.Git"},
                {"name": "Python 3.12", "id": "Python.Python.3.12"},
                {"name": "Node.js", "id": "OpenJS.NodeJS"},
                {"name": "GitHub Desktop", "id": "GitHub.GitHubDesktop"},
                {"name": "Postman", "id": "Postman.Postman"},
                {"name": "Docker Desktop", "id": "Docker.DockerDesktop"}
            ],
            "Design": [
                {"name": "Inkscape", "id": "Inkscape.Inkscape"},
                {"name": "Blender", "id": "BlenderFoundation.Blender"},
                {"name": "Krita", "id": "KDE.Krita"},
                {"name": "Figma", "id": "Figma.Figma"},
                {"name": "DaVinci Resolve", "id": "Blackmagic.DaVinciResolve"}
            ],
            "Gaming": [
                {"name": "Steam", "id": "Valve.Steam"},
                {"name": "Epic Games Launcher", "id": "EpicGames.EpicGamesLauncher"},
                {"name": "EA App", "id": "ElectronicArts.EADesktop"},
                {"name": "GOG Galaxy", "id": "GOG.Galaxy"},
                {"name": "Playnite", "id": "Playnite.Playnite"},
                {"name": "MSI Afterburner", "id": "Guru3D.Afterburner"}
            ],
            "Segurança": [
                {"name": "Malwarebytes", "id": "Malwarebytes.Malwarebytes"},
                {"name": "Bitwarden", "id": "Bitwarden.Bitwarden"},
                {"name": "ProtonVPN", "id": "ProtonVPN.ProtonVPN"},
                {"name": "VeraCrypt", "id": "IDRIX.VeraCrypt"},
                {"name": "KeePassXC", "id": "KeePassXCTeam.KeePassXC"}
            ],
            "Manutenção": [
                {"name": "HWiNFO", "id": "REALiX.HWiNFO"},
                {"name": "CrystalDiskInfo", "id": "CrystalDewWorld.CrystalDiskInfo"},
                {"name": "CPU-Z", "id": "CPUID.CPU-Z"},
                {"name": "GPU-Z", "id": "TechPowerUp.GPU-Z"},
                {"name": "Snappy Driver Installer", "id": "Glenn.Delahoy.SnappyDriverInstallerOrigin"}
            ]
        }
        
        # Perfis atualizados com melhores softwares 2025
        self.installation_profiles = {
            "Básico": [
                "Google.Chrome",           # Navegador
                "7zip.7zip",               # Compactador
                "VideoLAN.VLC",            # Player de vídeo
                "Adobe.Acrobat.Reader.64-bit",  # Leitor PDF
                "voidtools.Everything",    # Busca rápida de arquivos
                "Microsoft.PowerToys"      # Utilitários do Windows
            ],
            
            "Escritório": [
                "Google.Chrome",
                "TheDocumentFoundation.LibreOffice",  # Suite Office completa
                "Adobe.Acrobat.Reader.64-bit",
                "Zoom.Zoom",               # Videoconferência
                "Microsoft.Teams",         # Colaboração
                "SlackTechnologies.Slack", # Comunicação
                "Notion.Notion",           # Notas e organização
                "7zip.7zip",
                "Microsoft.PowerToys",
                "Bitwarden.Bitwarden"      # Gerenciador de senhas
            ],
            
            "Gamer": [
                "Google.Chrome",
                "Discord.Discord",         # Chat gamer
                "Valve.Steam",             # Loja de jogos
                "EpicGames.EpicGamesLauncher",
                "OBSProject.OBSStudio",    # Gravação/streaming
                "Spotify.Spotify",
                "7zip.7zip",
                "Guru3D.Afterburner",      # Overclock/monitoramento
                "Playnite.Playnite",       # Biblioteca unificada de jogos
                "ShareX.ShareX"            # Screenshots/GIFs
            ],
            
            "Desenvolvedor": [
                "Google.Chrome",
                "Microsoft.VisualStudioCode",  # Editor de código
                "Git.Git",                 # Controle de versão
                "GitHub.GitHubDesktop",    # Interface Git
                "Python.Python.3.12",      # Python
                "OpenJS.NodeJS",           # Node.js
                "Postman.Postman",         # Teste de APIs
                "Notepad++.Notepad++",     # Editor de texto avançado
                "Docker.DockerDesktop",    # Containers
                "7zip.7zip",
                "voidtools.Everything",
                "Microsoft.PowerToys"
            ],
            
            "Designer": [
                "Google.Chrome",
                "GIMP.GIMP",               # Edição de imagem
                "Inkscape.Inkscape",       # Gráficos vetoriais
                "Krita.Krita",             # Pintura digital
                "BlenderFoundation.Blender", # 3D e animação
                "Blackmagic.DaVinciResolve", # Edição de vídeo
                "OBSProject.OBSStudio",
                "ShareX.ShareX",
                "Figma.Figma",             # Design UI/UX
                "Adobe.Acrobat.Reader.64-bit",
                "7zip.7zip"
            ],
            
            "Segurança": [
                "Google.Chrome",
                "Malwarebytes.Malwarebytes",  # Anti-malware
                "Bitwarden.Bitwarden",     # Gerenciador senhas
                "ProtonVPN.ProtonVPN",     # VPN
                "IDRIX.VeraCrypt",         # Criptografia de disco
                "KeePassXCTeam.KeePassXC", # Senhas offline
                "7zip.7zip",
                "Revo.RevoUninstaller",    # Desinstalador completo
                "voidtools.Everything"
            ]
        }
    
    def check_winget_available(self):
        """Verifica se o Winget está disponível no sistema"""
        try:
            result = subprocess.run(
                ["winget", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def search_package(self, query):
        """Busca pacotes no Winget"""
        try:
            result = subprocess.run(
                ["winget", "search", query],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout
        except Exception as e:
            return f"Erro: {str(e)}"
    
    def install_package(self, package_id, silent=True, progress_callback=None):
        """Instala um pacote usando Winget"""
        try:
            if progress_callback:
                progress_callback(package_id, "iniciando instalação")
            
            cmd = [
                "winget", "install",
                "--id", package_id,
                "--accept-package-agreements",
                "--accept-source-agreements",
                "--disable-interactivity"
            ]
            
            if silent:
                cmd.append("--silent")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                if progress_callback:
                    progress_callback(package_id, "instalado com sucesso")
                return True, "Instalação concluída"
            else:
                if progress_callback:
                    progress_callback(package_id, f"erro: {stderr}")
                return False, stderr
                
        except Exception as e:
            if progress_callback:
                progress_callback(package_id, f"erro: {str(e)}")
            return False, str(e)
    
    def install_multiple(self, package_ids, progress_callback=None):
        """Instala múltiplos pacotes em sequência"""
        results = []
        
        for package_id in package_ids:
            success, message = self.install_package(
                package_id,
                silent=True,
                progress_callback=progress_callback
            )
            results.append({
                "package_id": package_id,
                "success": success,
                "message": message
            })
        
        return results
    
    def install_profile(self, profile_name, progress_callback=None):
        """Instala um perfil pré-configurado"""
        if profile_name not in self.installation_profiles:
            return False, "Perfil não encontrado"
        
        package_ids = self.installation_profiles[profile_name]
        return self.install_multiple(package_ids, progress_callback)
    
    def get_installed_packages(self):
        """Lista todos os pacotes instalados"""
        try:
            result = subprocess.run(
                ["winget", "list"],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout
        except Exception as e:
            return f"Erro: {str(e)}"
