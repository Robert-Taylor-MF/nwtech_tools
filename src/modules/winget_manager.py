import subprocess
import json
import requests

class WingetManager:
    def __init__(self):
        self.software_catalog = {
            "Navegadores": [
                {"name": "Google Chrome", "id": "Google.Chrome"},
                {"name": "Mozilla Firefox", "id": "Mozilla.Firefox"},
                {"name": "Microsoft Edge", "id": "Microsoft.Edge"},
                {"name": "Brave", "id": "Brave.Brave"}
            ],
            "Comunicação": [
                {"name": "WhatsApp", "id": "WhatsApp.WhatsApp"},
                {"name": "Discord", "id": "Discord.Discord"},
                {"name": "Zoom", "id": "Zoom.Zoom"},
                {"name": "Microsoft Teams", "id": "Microsoft.Teams"}
            ],
            "Office": [
                {"name": "LibreOffice", "id": "TheDocumentFoundation.LibreOffice"},
                {"name": "Adobe Reader", "id": "Adobe.Acrobat.Reader.64-bit"},
                {"name": "Notepad++", "id": "Notepad++.Notepad++"}
            ],
            "Multimídia": [
                {"name": "VLC Media Player", "id": "VideoLAN.VLC"},
                {"name": "Spotify", "id": "Spotify.Spotify"},
                {"name": "OBS Studio", "id": "OBSProject.OBSStudio"}
            ],
            "Utilitários": [
                {"name": "7-Zip", "id": "7zip.7zip"},
                {"name": "WinRAR", "id": "RARLab.WinRAR"},
                {"name": "CCleaner", "id": "Piriform.CCleaner"}
            ],
            "Segurança": [
                {"name": "Malwarebytes", "id": "Malwarebytes.Malwarebytes"},
                {"name": "Avast", "id": "Avast.Avast"}
            ]
        }
        
        self.installation_profiles = {
            "Básico": ["Google.Chrome", "7zip.7zip", "VideoLAN.VLC", "Adobe.Acrobat.Reader.64-bit"],
            "Escritório": ["Google.Chrome", "TheDocumentFoundation.LibreOffice", "Adobe.Acrobat.Reader.64-bit", "Zoom.Zoom"],
            "Gamer": ["Google.Chrome", "Discord.Discord", "7zip.7zip", "OBSProject.OBSStudio"],
            "Desenvolvedor": ["Google.Chrome", "Notepad++.Notepad++", "7zip.7zip", "Microsoft.VisualStudioCode"]
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
            
            cmd = ["winget", "install", "--id", package_id, "--accept-package-agreements", "--accept-source-agreements"]
            
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
            success, message = self.install_package(package_id, silent=True, progress_callback=progress_callback)
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
