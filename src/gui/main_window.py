import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from src.modules.backup_manager import BackupManager
from src.modules.winget_manager import WingetManager

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TechAssistApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("NWTECH TOOLS - Ferramenta Profissional de Assistência Técnica")
        self.geometry("1200x700")
        
        self.backup_manager = BackupManager()
        self.winget_manager = WingetManager()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Menu lateral
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="TechAssist",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.pack(pady=20)
        
        # Botões do menu
        self.btn_backup = ctk.CTkButton(
            self.sidebar,
            text="Backup & Restore",
            command=self.show_backup_frame,
            height=40
        )
        self.btn_backup.pack(pady=10, padx=20)
        
        self.btn_winget = ctk.CTkButton(
            self.sidebar,
            text="Winget Manager",
            command=self.show_winget_frame,
            height=40
        )
        self.btn_winget.pack(pady=10, padx=20)
        
        self.btn_tools = ctk.CTkButton(
            self.sidebar,
            text="Ferramentas",
            command=self.show_tools_frame,
            height=40
        )
        self.btn_tools.pack(pady=10, padx=20)
        
        self.btn_report = ctk.CTkButton(
            self.sidebar,
            text="Relatório",
            command=self.show_report_frame,
            height=40
        )
        self.btn_report.pack(pady=10, padx=20)
        
        # Área principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Frame de backup (inicial)
        self.create_backup_frame()
    
    def create_backup_frame(self):
        self.clear_main_frame()
        
        title = ctk.CTkLabel(
            self.main_frame,
            text="Backup & Restore",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        # Frame de backup
        backup_frame = ctk.CTkFrame(self.main_frame)
        backup_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            backup_frame,
            text="Criar Backup",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        self.backup_dest_label = ctk.CTkLabel(
            backup_frame,
            text="Nenhum destino selecionado"
        )
        self.backup_dest_label.pack(pady=5)
        
        ctk.CTkButton(
            backup_frame,
            text="Selecionar Destino do Backup",
            command=self.select_backup_destination
        ).pack(pady=5)
        
        self.include_browsers_var = ctk.CTkCheckBox(
            backup_frame,
            text="Incluir dados dos navegadores"
        )
        self.include_browsers_var.pack(pady=5)
        self.include_browsers_var.select()
        
        ctk.CTkButton(
            backup_frame,
            text="Iniciar Backup",
            command=self.start_backup,
            fg_color="green",
            hover_color="darkgreen",
            height=40
        ).pack(pady=10)
        
        # Frame de restore
        restore_frame = ctk.CTkFrame(self.main_frame)
        restore_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            restore_frame,
            text="Restaurar Backup",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        self.restore_source_label = ctk.CTkLabel(
            restore_frame,
            text="Nenhuma pasta selecionada"
        )
        self.restore_source_label.pack(pady=5)
        
        ctk.CTkButton(
            restore_frame,
            text="Selecionar Pasta do Backup",
            command=self.select_restore_source
        ).pack(pady=5)
        
        ctk.CTkButton(
            restore_frame,
            text="Restaurar Arquivos",
            command=self.start_restore,
            fg_color="orange",
            hover_color="darkorange",
            height=40
        ).pack(pady=10)
        
        # Log
        self.log_textbox = ctk.CTkTextbox(self.main_frame, height=200)
        self.log_textbox.pack(fill="both", expand=True, padx=20, pady=10)
    
    def create_winget_frame(self):
        self.clear_main_frame()
        
        title = ctk.CTkLabel(
            self.main_frame,
            text="Gerenciador Winget",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        # Verificar se Winget está disponível
        if not self.winget_manager.check_winget_available():
            error_label = ctk.CTkLabel(
                self.main_frame,
                text="⚠️ Winget não está disponível no sistema",
                text_color="red",
                font=ctk.CTkFont(size=16)
            )
            error_label.pack(pady=20)
            return
        
        # Perfis de instalação
        profiles_frame = ctk.CTkFrame(self.main_frame)
        profiles_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            profiles_frame,
            text="Perfis de Instalação Rápida",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        profile_buttons = ctk.CTkFrame(profiles_frame)
        profile_buttons.pack(pady=10)
        
        for profile in self.winget_manager.installation_profiles.keys():
            ctk.CTkButton(
                profile_buttons,
                text=profile,
                command=lambda p=profile: self.install_profile(p),
                width=150
            ).pack(side="left", padx=5)
        
        # Catálogo de programas
        catalog_frame = ctk.CTkScrollableFrame(self.main_frame, height=400)
        catalog_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        for category, programs in self.winget_manager.software_catalog.items():
            category_label = ctk.CTkLabel(
                catalog_frame,
                text=category,
                font=ctk.CTkFont(size=16, weight="bold")
            )
            category_label.pack(anchor="w", pady=5)
            
            for program in programs:
                prog_frame = ctk.CTkFrame(catalog_frame)
                prog_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    prog_frame,
                    text=program["name"],
                    width=200,
                    anchor="w"
                ).pack(side="left", padx=10)
                
                ctk.CTkButton(
                    prog_frame,
                    text="Instalar",
                    command=lambda pid=program["id"]: self.install_single_package(pid),
                    width=100
                ).pack(side="right", padx=10)
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_backup_frame(self):
        self.create_backup_frame()
    
    def show_winget_frame(self):
        self.create_winget_frame()
    
    def show_tools_frame(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(
            self.main_frame,
            text="Ferramentas de Diagnóstico (Em desenvolvimento)",
            font=ctk.CTkFont(size=24)
        )
        label.pack(pady=50)
    
    def show_report_frame(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(
            self.main_frame,
            text="Gerador de Relatórios (Em desenvolvimento)",
            font=ctk.CTkFont(size=24)
        )
        label.pack(pady=50)
    
    def select_backup_destination(self):
        folder = filedialog.askdirectory(title="Selecione o destino do backup")
        if folder:
            self.backup_destination = folder
            self.backup_dest_label.configure(text=f"Destino: {folder}")
    
    def select_restore_source(self):
        folder = filedialog.askdirectory(title="Selecione a pasta do backup")
        if folder:
            self.restore_source = folder
            self.restore_source_label.configure(text=f"Origem: {folder}")
    
    def log_message(self, message):
        """Adiciona mensagem ao log de forma thread-safe"""
        def _insert():
            try:
                if self.log_textbox.winfo_exists():
                    self.log_textbox.insert("end", f"{message}\n")
                    self.log_textbox.see("end")
            except:
                pass
            
        # Usa after para executar na thread principal
        self.after(0, _insert)
    
    def start_backup(self):
        """Inicia o processo de backup"""
        if not hasattr(self, 'backup_destination'):
            messagebox.showerror("Erro", "Selecione um destino para o backup")
            return

        def backup_thread():
            self.after(0, lambda: self.log_message("🔄 Iniciando backup..."))

            def progress(item, status):
                self.after(0, lambda i=item, s=status: 
                          self.log_message(f"  → {i}: {s}"))

            try:
                include_browsers = self.include_browsers_var.get() == 1
                backup_folder, log = self.backup_manager.create_backup(
                    self.backup_destination,
                    include_browsers=include_browsers,
                    progress_callback=progress
                )

                self.after(0, lambda bf=backup_folder, l=log: self._show_backup_success(bf, l))

            except Exception as e:
                self.after(0, lambda e=e: self._show_backup_error(e))

        threading.Thread(target=backup_thread, daemon=True).start()
        
    def _show_backup_success(self, backup_folder, log):
        """Mostra sucesso do backup (executado na thread principal)"""
        self.log_message(f"✅ Backup concluído: {backup_folder}")
        self.log_message(f"📊 Total de arquivos: {len(log['files_backed_up'])}")
        self.log_message(f"📦 Tamanho total: {log['total_size'] / (1024**3):.2f} GB")
        messagebox.showinfo("Sucesso", f"Backup criado com sucesso!\n{backup_folder}")

    def _show_backup_error(self, error):
        """Mostra erro do backup (executado na thread principal)"""
        self.log_message(f"❌ Erro no backup: {str(error)}")
        messagebox.showerror("Erro", f"Falha no backup: {str(error)}")
    
    def start_restore(self):
        """Inicia restauração do backup"""
        if not hasattr(self, 'restore_source'):
            messagebox.showerror("Erro", "Selecione a pasta do backup")
            return

        confirm = messagebox.askyesno(
            "Confirmar Restauração",
            "ATENÇÃO: Esta operação irá substituir os arquivos atuais.\nDeseja continuar?"
        )

        if not confirm:
            return

        def restore_thread():
            self.after(0, lambda: self.log_message("🔄 Iniciando restauração..."))

            def progress(item, status):
                self.after(0, lambda i=item, s=status: 
                          self.log_message(f"  → {i}: {s}"))

            try:
                success, result = self.backup_manager.restore_backup(
                    self.restore_source,
                    progress_callback=progress
                )

                if success:
                    self.after(0, lambda r=result: self._show_restore_success(r))
                else:
                    self.after(0, lambda r=result: self._show_restore_error(r))

            except Exception as e:
                self.after(0, lambda e=e: self._show_restore_error(str(e)))

        threading.Thread(target=restore_thread, daemon=True).start()
    
    def _show_restore_success(self, result):
        """Mostra sucesso da restauração"""
        self.log_message(f"✅ Restauração concluída!")
        self.log_message(f"📊 Itens restaurados: {len(result['restored'])}")
        messagebox.showinfo("Sucesso", "Arquivos restaurados com sucesso!")

    def _show_restore_error(self, error):
        """Mostra erro da restauração"""
        self.log_message(f"❌ Erro: {error}")
        messagebox.showerror("Erro", str(error))
        
        def install_profile(self, profile_name):
            """Instala um perfil completo"""
            self.log_message(f"🔄 Instalando perfil: {profile_name}")
    
            def install_thread():
                def progress(package_id, status):
                    self.after(0, lambda p=package_id, s=status: 
                              self.log_message(f"  → {p}: {s}"))
    
                results = self.winget_manager.install_profile(
                    profile_name, 
                    progress_callback=progress
                )
    
                success_count = sum(1 for r in results if r["success"])
                self.after(0, lambda: self.log_message(
                    f"✅ Perfil instalado: {success_count}/{len(results)} pacotes"
                ))
    
            threading.Thread(target=install_thread, daemon=True).start()
    
    def install_single_package(self, package_id):
        """Instala um único pacote"""
        self.log_message(f"🔄 Instalando: {package_id}")

        def install_thread():
            def progress(pid, status):
                # Usa self.after para atualizar na thread principal
                self.after(0, lambda: self.log_message(f"  → {pid}: {status}"))

            success, message = self.winget_manager.install_package(
                package_id, 
                progress_callback=progress
            )

            if success:
                self.after(0, lambda: self.log_message(f"✅ Instalado: {package_id}"))
            else:
                self.after(0, lambda: self.log_message(f"❌ Erro: {message}"))

        threading.Thread(target=install_thread, daemon=True).start()
