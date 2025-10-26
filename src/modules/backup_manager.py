import os
import shutil
import json
import hashlib
from datetime import datetime
from pathlib import Path
import stat

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
        
        # Pastas/arquivos a ignorar
        self.ignore_patterns = [
            'node_modules',
            '__pycache__',
            '.git',
            'Temp',
            'Cache',
            'cache',
            'tmp'
        ]
    
    def _should_ignore(self, path):
        """Verifica se o caminho deve ser ignorado"""
        path_lower = path.lower()
        return any(pattern.lower() in path_lower for pattern in self.ignore_patterns)
    
    def _copy_with_retry(self, src, dst, max_retries=3):
        """Copia arquivo com retry e tratamento de erros"""
        for attempt in range(max_retries):
            try:
                # Garante que o diretório de destino existe
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                
                # Tenta copiar
                shutil.copy2(src, dst)
                return True, None
                
            except PermissionError as e:
                # Tenta mudar permissões
                try:
                    os.chmod(src, stat.S_IREAD | stat.S_IWRITE)
                    shutil.copy2(src, dst)
                    return True, None
                except:
                    if attempt == max_retries - 1:
                        return False, f"Permissão negada: {os.path.basename(src)}"
                    
            except FileNotFoundError:
                return False, f"Arquivo não encontrado: {os.path.basename(src)}"
                
            except Exception as e:
                if attempt == max_retries - 1:
                    return False, f"Erro ao copiar {os.path.basename(src)}: {str(e)}"
        
        return False, "Falha após múltiplas tentativas"
    
    def create_backup(self, destination, include_browsers=True, progress_callback=None):
        """Cria backup completo dos dados do usuário"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(destination, f"NWTECH_Backup_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)
        
        backup_log = {
            "timestamp": timestamp,
            "files_backed_up": [],
            "files_skipped": [],
            "errors": [],
            "total_size": 0,
            "total_files": 0,
            "skipped_files": 0
        }
        
        # Backup de pastas do usuário
        for name, source_path in self.backup_paths.items():
            if not os.path.exists(source_path):
                backup_log["errors"].append(f"{name}: Pasta não encontrada")
                if progress_callback:
                    progress_callback(name, "pasta não encontrada")
                continue
            
            dest_path = os.path.join(backup_folder, name)
            os.makedirs(dest_path, exist_ok=True)
            
            if progress_callback:
                progress_callback(name, "copiando...")
            
            files_copied = 0
            files_skipped = 0
            folder_size = 0
            
            # Percorre recursivamente
            for root, dirs, files in os.walk(source_path):
                # Remove diretórios a ignorar
                dirs[:] = [d for d in dirs if not self._should_ignore(os.path.join(root, d))]
                
                for file in files:
                    src_file = os.path.join(root, file)
                    
                    # Ignora arquivos específicos
                    if self._should_ignore(src_file):
                        files_skipped += 1
                        continue
                    
                    # Calcula caminho relativo
                    rel_path = os.path.relpath(src_file, source_path)
                    dst_file = os.path.join(dest_path, rel_path)
                    
                    # Tenta copiar
                    success, error = self._copy_with_retry(src_file, dst_file)
                    
                    if success:
                        files_copied += 1
                        try:
                            folder_size += os.path.getsize(dst_file)
                        except:
                            pass
                    else:
                        files_skipped += 1
                        backup_log["files_skipped"].append(f"{name}/{rel_path}: {error}")
            
            backup_log["files_backed_up"].append({
                "folder": name,
                "files_copied": files_copied,
                "files_skipped": files_skipped,
                "size": folder_size,
                "status": "concluído"
            })
            backup_log["total_size"] += folder_size
            backup_log["total_files"] += files_copied
            backup_log["skipped_files"] += files_skipped
            
            if progress_callback:
                progress_callback(name, f"concluído ({files_copied} arquivos)")
        
        # Backup de navegadores (somente favoritos e senhas)
        if include_browsers:
            browser_backup = os.path.join(backup_folder, "Navegadores")
            os.makedirs(browser_backup, exist_ok=True)
            
            for browser, path in self.browser_paths.items():
                if not os.path.exists(path):
                    continue
                
                if progress_callback:
                    progress_callback(f"Navegador {browser}", "copiando...")
                
                dest = os.path.join(browser_backup, browser)
                
                # Copia apenas arquivos importantes (favoritos, senhas)
                important_files = ['Bookmarks', 'Preferences', 'Login Data', 'Cookies']
                files_copied = 0
                
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if any(imp in file for imp in important_files):
                            src_file = os.path.join(root, file)
                            rel_path = os.path.relpath(src_file, path)
                            dst_file = os.path.join(dest, rel_path)
                            
                            success, error = self._copy_with_retry(src_file, dst_file)
                            if success:
                                files_copied += 1
                
                if files_copied > 0:
                    backup_log["files_backed_up"].append({
                        "folder": f"Navegador_{browser}",
                        "files_copied": files_copied,
                        "status": "concluído"
                    })
                    
                    if progress_callback:
                        progress_callback(f"Navegador {browser}", f"concluído ({files_copied} arquivos)")
        
        # Salvar log do backup
        log_file = os.path.join(backup_folder, "backup_log.json")
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(backup_log, f, indent=4, ensure_ascii=False)
        
        # Criar arquivo README
        readme_file = os.path.join(backup_folder, "README.txt")
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("NWTECH TOOLS - BACKUP AUTOMÁTICO\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Data do backup: {timestamp}\n\n")
            f.write(f"Total de arquivos copiados: {backup_log['total_files']}\n")
            f.write(f"Arquivos ignorados: {backup_log['skipped_files']}\n")
            f.write(f"Tamanho total: {backup_log['total_size'] / (1024**3):.2f} GB\n\n")
            f.write("Para restaurar este backup, use o NWTECH TOOLS.\n")
        
        return backup_folder, backup_log
    
    def restore_backup(self, backup_folder, progress_callback=None):
        """Restaura backup para as pastas originais"""
        if not os.path.exists(backup_folder):
            raise FileNotFoundError("Pasta de backup não encontrada")
        
        restored_items = []
        errors = []
        total_restored = 0
        
        # Restaurar cada pasta
        for name, original_path in self.backup_paths.items():
            backup_path = os.path.join(backup_folder, name)
            
            if not os.path.exists(backup_path):
                continue
            
            if progress_callback:
                progress_callback(name, "restaurando...")
            
            files_restored = 0
            
            # Cria pasta de destino se não existir
            os.makedirs(original_path, exist_ok=True)
            
            # Copia arquivos recursivamente
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    src_file = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file, backup_path)
                    dst_file = os.path.join(original_path, rel_path)
                    
                    success, error = self._copy_with_retry(src_file, dst_file)
                    
                    if success:
                        files_restored += 1
                    else:
                        errors.append(f"{name}/{rel_path}: {error}")
            
            if files_restored > 0:
                restored_items.append(f"{name} ({files_restored} arquivos)")
                total_restored += files_restored
                
                if progress_callback:
                    progress_callback(name, f"restaurado ({files_restored} arquivos)")
        
        return True, {
            "restored": restored_items,
            "errors": errors,
            "total_files": total_restored
        }
