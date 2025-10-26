import os
import shutil
import json
import hashlib
from datetime import datetime
from pathlib import Path
import zipfile

class BackupManager:
    def __init__(self):
        self.backup_paths = {
            "Desktop": os.path.expanduser("~/Desktop"),
            "Documents": os.path.expanduser("~/Documents"),
            "Downloads": os.path.expanduser("~/Downloads"),
            "Pictures": os.path.expanduser("~/Pictures"),
            "Videos": os.path.expanduser("~/Videos"),
            "Music": os.path.expanduser("~/Music")
        }
        
        self.browser_paths = {
            "Chrome": os.path.expanduser("~/AppData/Local/Google/Chrome/User Data"),
            "Edge": os.path.expanduser("~/AppData/Local/Microsoft/Edge/User Data"),
            "Firefox": os.path.expanduser("~/AppData/Roaming/Mozilla/Firefox")
        }
    
    def create_backup(self, destination, include_browsers=True, progress_callback=None):
        """Cria backup completo dos dados do usuário"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(destination, f"Backup_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)
        
        backup_log = {
            "timestamp": timestamp,
            "files_backed_up": [],
            "errors": [],
            "total_size": 0
        }
        
        # Backup de pastas do usuário
        for name, path in self.backup_paths.items():
            if os.path.exists(path):
                dest_path = os.path.join(backup_folder, name)
                try:
                    shutil.copytree(path, dest_path, dirs_exist_ok=True)
                    size = self._get_folder_size(dest_path)
                    backup_log["files_backed_up"].append({
                        "folder": name,
                        "size": size,
                        "status": "success"
                    })
                    backup_log["total_size"] += size
                    
                    if progress_callback:
                        progress_callback(name, "concluído")
                        
                except Exception as e:
                    backup_log["errors"].append(f"{name}: {str(e)}")
                    if progress_callback:
                        progress_callback(name, f"erro: {str(e)}")
        
        # Backup de navegadores
        if include_browsers:
            browser_backup = os.path.join(backup_folder, "Browsers")
            os.makedirs(browser_backup, exist_ok=True)
            
            for browser, path in self.browser_paths.items():
                if os.path.exists(path):
                    dest = os.path.join(browser_backup, browser)
                    try:
                        shutil.copytree(path, dest, dirs_exist_ok=True)
                        backup_log["files_backed_up"].append({
                            "folder": f"Browser_{browser}",
                            "status": "success"
                        })
                    except Exception as e:
                        backup_log["errors"].append(f"{browser}: {str(e)}")
        
        # Salvar log do backup
        log_file = os.path.join(backup_folder, "backup_log.json")
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(backup_log, f, indent=4, ensure_ascii=False)
        
        # Criar arquivo de verificação (checksum)
        self._create_checksum_file(backup_folder)
        
        return backup_folder, backup_log
    
    def _get_folder_size(self, folder_path):
        """Calcula tamanho total de uma pasta"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        return total_size
    
    def _create_checksum_file(self, backup_folder):
        """Cria arquivo com checksums para validação"""
        checksum_file = os.path.join(backup_folder, "checksums.txt")
        
        with open(checksum_file, 'w') as f:
            for root, dirs, files in os.walk(backup_folder):
                for file in files:
                    if file != "checksums.txt":
                        filepath = os.path.join(root, file)
                        try:
                            file_hash = self._calculate_md5(filepath)
                            relative_path = os.path.relpath(filepath, backup_folder)
                            f.write(f"{file_hash}  {relative_path}\n")
                        except:
                            pass
    
    def _calculate_md5(self, filepath):
        """Calcula hash MD5 de um arquivo"""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def restore_backup(self, backup_folder, progress_callback=None):
        """Restaura backup para as pastas originais"""
        if not os.path.exists(backup_folder):
            raise FileNotFoundError("Pasta de backup não encontrada")
        
        # Verificar integridade primeiro
        if not self._verify_backup_integrity(backup_folder):
            return False, "Falha na verificação de integridade"
        
        restored_items = []
        errors = []
        
        # Restaurar cada pasta
        for name, original_path in self.backup_paths.items():
            backup_path = os.path.join(backup_folder, name)
            
            if os.path.exists(backup_path):
                try:
                    if os.path.exists(original_path):
                        shutil.rmtree(original_path)
                    
                    shutil.copytree(backup_path, original_path)
                    restored_items.append(name)
                    
                    if progress_callback:
                        progress_callback(name, "restaurado")
                        
                except Exception as e:
                    errors.append(f"{name}: {str(e)}")
                    if progress_callback:
                        progress_callback(name, f"erro: {str(e)}")
        
        return True, {"restored": restored_items, "errors": errors}
    
    def _verify_backup_integrity(self, backup_folder):
        """Verifica integridade do backup usando checksums"""
        checksum_file = os.path.join(backup_folder, "checksums.txt")
        
        if not os.path.exists(checksum_file):
            return True  # Se não há arquivo de checksum, assume OK
        
        with open(checksum_file, 'r') as f:
            for line in f:
                if line.strip():
                    stored_hash, filepath = line.strip().split('  ', 1)
                    full_path = os.path.join(backup_folder, filepath)
                    
                    if os.path.exists(full_path):
                        current_hash = self._calculate_md5(full_path)
                        if current_hash != stored_hash:
                            return False
        
        return True
