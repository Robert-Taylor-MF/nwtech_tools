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
        """Instala um perfil completo com progresso"""
        packages = self.winget_manager.installation_profiles.get(profile_name, [])
        total_packages = len(packages)
        
        if total_packages == 0:
            self.log_message(f"❌ Perfil {profile_name} não encontrado")
            return
        
        # Atualiza interface se existir
        if hasattr(self, 'current_install_label'):
            self.current_install_label.configure(text=f"Instalando perfil: {profile_name}")
            self.install_progress.set(0)
            self.progress_label.configure(text=f"0/{total_packages} pacotes instalados")
        
        self.log_message(f"🔄 Instalando perfil: {profile_name} ({total_packages} pacotes)")
        
        def install_thread():
            installed = 0
            
            for i, package_id in enumerate(packages, 1):
                # Atualiza progresso se existir
                if hasattr(self, 'install_progress'):
                    progress_value = i / total_packages
                    self.after(0, lambda pv=progress_value: self.install_progress.set(pv))
                    self.after(0, lambda i=i, t=total_packages: 
                              self.progress_label.configure(text=f"{i}/{t} pacotes"))
                
                def progress(pid, status):
                    self.after(0, lambda p=pid, s=status: 
                              self.log_message(f"  → {p}: {s}"))
                
                success, message = self.winget_manager.install_package(
                    package_id, 
                    progress_callback=progress
                )
                
                if success:
                    installed += 1
            
            # Finalização
            if hasattr(self, 'current_install_label'):
                self.after(0, lambda: self.current_install_label.configure(
                    text=f"✅ Perfil {profile_name} instalado!"
                ))
                self.after(0, lambda i=installed, t=total_packages: 
                          self.progress_label.configure(text=f"✅ {i}/{t} pacotes instalados com sucesso"))
            
            self.after(0, lambda: self.log_message(
                f"✅ Perfil {profile_name} concluído: {installed}/{total_packages} pacotes"
            ))
            
            # Reset após 5 segundos (se existir)
            if hasattr(self, 'current_install_label'):
                self.after(5000, lambda: self.current_install_label.configure(
                    text="Nenhuma instalação em andamento"
                ))
                self.after(5000, lambda: self.install_progress.set(0))
        
        threading.Thread(target=install_thread, daemon=True).start()
        
    def install_single_package(self, package_id, package_name=None):
        """Instala um único pacote com feedback visual"""
        # Se não passar o nome, usa o ID
        if package_name is None:
            package_name = package_id

        # Verifica se os widgets de progresso existem
        if hasattr(self, 'current_install_label'):
            self.current_install_label.configure(text=f"Instalando: {package_name}")
            self.install_progress.set(0)
            self.progress_label.configure(text="Iniciando instalação...")

        self.log_message(f"🔄 Instalando: {package_name}")

        def install_thread():
            # Atualiza barra de progresso se existir
            if hasattr(self, 'install_progress'):
                self.after(0, lambda: self.install_progress.set(0.3))
                self.after(0, lambda: self.progress_label.configure(text="Baixando..."))

            def progress(pid, status):
                if "sucesso" in status.lower():
                    if hasattr(self, 'install_progress'):
                        self.after(0, lambda: self.install_progress.set(1.0))
                        self.after(0, lambda: self.progress_label.configure(text="✅ Concluído!"))
                elif "erro" in status.lower():
                    if hasattr(self, 'install_progress'):
                        self.after(0, lambda: self.install_progress.set(0))
                        self.after(0, lambda: self.progress_label.configure(text="❌ Erro na instalação"))
                else:
                    if hasattr(self, 'install_progress'):
                        self.after(0, lambda: self.install_progress.set(0.6))
                        self.after(0, lambda: self.progress_label.configure(text="Instalando..."))

                self.after(0, lambda p=pid, s=status: self.log_message(f"  → {p}: {s}"))

            success, message = self.winget_manager.install_package(
                package_id, 
                progress_callback=progress
            )

            if success:
                if hasattr(self, 'current_install_label'):
                    self.after(0, lambda: self.current_install_label.configure(
                        text=f"✅ {package_name} instalado com sucesso!"
                    ))
                self.after(0, lambda: self.log_message(f"✅ Instalado: {package_name}"))
            else:
                if hasattr(self, 'current_install_label'):
                    self.after(0, lambda: self.current_install_label.configure(
                        text=f"❌ Falha ao instalar {package_name}"
                    ))
                self.after(0, lambda: self.log_message(f"❌ Erro: {message}"))

            # Reset após 3 segundos (se existir)
            if hasattr(self, 'current_install_label'):
                self.after(3000, lambda: self.current_install_label.configure(
                    text="Nenhuma instalação em andamento"
                ))
                self.after(3000, lambda: self.install_progress.set(0))

        threading.Thread(target=install_thread, daemon=True).start()
            
def create_winget_frame(self):
    self.clear_main_frame()
    
    title = ctk.CTkLabel(
        self.main_frame,
        text="Gerenciador Winget - NWTECH TOOLS",
        font=ctk.CTkFont(size=28, weight="bold")
    )
    title.pack(pady=20)
    
    # Verificar se Winget está disponível
    if not self.winget_manager.check_winget_available():
        error_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        error_frame.pack(pady=20)
        
        error_label = ctk.CTkLabel(
            error_frame,
            text="⚠️ Winget não está disponível no sistema",
            text_color="red",
            font=ctk.CTkFont(size=16)
        )
        error_label.pack(pady=10)
        
        help_label = ctk.CTkLabel(
            error_frame,
            text="Instale o Winget através da Microsoft Store (App Installer)",
            font=ctk.CTkFont(size=12)
        )
        help_label.pack(pady=5)
        return
    
    # Frame de status de instalação
    self.install_status_frame = ctk.CTkFrame(self.main_frame)
    self.install_status_frame.pack(fill="x", padx=20, pady=10)
    
    self.current_install_label = ctk.CTkLabel(
        self.install_status_frame,
        text="Nenhuma instalação em andamento",
        font=ctk.CTkFont(size=14)
    )
    self.current_install_label.pack(pady=5)
    
    # Barra de progresso geral
    self.install_progress = ctk.CTkProgressBar(
        self.install_status_frame,
        width=600,
        height=25,
        corner_radius=10,
        mode="determinate"
    )
    self.install_progress.pack(pady=10)
    self.install_progress.set(0)
    
    # Label de progresso (X/Y pacotes)
    self.progress_label = ctk.CTkLabel(
        self.install_status_frame,
        text="0/0 pacotes instalados",
        font=ctk.CTkFont(size=12)
    )
    self.progress_label.pack(pady=5)
    
    # Perfis de instalação
    profiles_frame = ctk.CTkFrame(self.main_frame)
    profiles_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkLabel(
        profiles_frame,
        text="⚡ Perfis de Instalação Rápida",
        font=ctk.CTkFont(size=18, weight="bold")
    ).pack(pady=10)
    
    profiles_desc = ctk.CTkLabel(
        profiles_frame,
        text="Instale conjuntos completos de programas com um clique",
        font=ctk.CTkFont(size=12),
        text_color="gray"
    )
    profiles_desc.pack(pady=5)
    
    # Grid de botões de perfil
    profile_buttons_frame = ctk.CTkFrame(profiles_frame, fg_color="transparent")
    profile_buttons_frame.pack(pady=10, padx=20)
    
    profiles_info = {
        "Básico": ("🏠", "Navegador, compactador, mídia e PDF"),
        "Escritório": ("💼", "Office, videoconferência e produtividade"),
        "Gamer": ("🎮", "Discord, OBS, launchers e utilitários"),
        "Desenvolvedor": ("👨‍💻", "IDEs, Git, ferramentas de desenvolvimento"),
        "Designer": ("🎨", "Edição de imagem, vídeo e design gráfico"),
        "Segurança": ("🛡️", "Antivírus, VPN e ferramentas de privacidade")
    }
    
    row = 0
    col = 0
    for profile, (emoji, desc) in profiles_info.items():
        profile_card = ctk.CTkFrame(profile_buttons_frame, width=280, height=120)
        profile_card.grid(row=row, column=col, padx=10, pady=10)
        
        ctk.CTkLabel(
            profile_card,
            text=f"{emoji} {profile}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        ctk.CTkLabel(
            profile_card,
            text=desc,
            font=ctk.CTkFont(size=11),
            text_color="gray",
            wraplength=250
        ).pack(pady=5)
        
        ctk.CTkButton(
            profile_card,
            text="Instalar Perfil",
            command=lambda p=profile: self.install_profile(p),
            width=200,
            height=35,
            fg_color="#2B5278",
            hover_color="#1F3A57"
        ).pack(pady=5)
        
        col += 1
        if col > 2:
            col = 0
            row += 1
    
    # Catálogo de programas com abas
    catalog_frame = ctk.CTkFrame(self.main_frame)
    catalog_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    ctk.CTkLabel(
        catalog_frame,
        text="📦 Catálogo de Programas",
        font=ctk.CTkFont(size=18, weight="bold")
    ).pack(pady=10, anchor="w", padx=20)
    
    # Tabview para categorias
    self.catalog_tabview = ctk.CTkTabview(catalog_frame, height=400)
    self.catalog_tabview.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Criar abas para cada categoria
    for category, programs in self.winget_manager.software_catalog.items():
        tab = self.catalog_tabview.add(category)
        
        # Scrollable frame para a categoria
        scroll_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        
        for program in programs:
            prog_frame = ctk.CTkFrame(scroll_frame, height=50)
            prog_frame.pack(fill="x", pady=3, padx=5)
            
            # Nome do programa
            ctk.CTkLabel(
                prog_frame,
                text=program["name"],
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w"
            ).pack(side="left", padx=15)
            
            # ID do programa (pequeno)
            ctk.CTkLabel(
                prog_frame,
                text=program["id"],
                font=ctk.CTkFont(size=10),
                text_color="gray",
                anchor="w"
            ).pack(side="left", padx=5)
            
            # Botão de instalação - AQUI ESTÁ A CORREÇÃO PRINCIPAL
            install_btn = ctk.CTkButton(
                prog_frame,
                text="📥 Instalar",
                command=lambda pid=program["id"], pname=program["name"]: 
                    self.install_single_package(pid, pname),  # ← DOIS ARGUMENTOS
                width=120,
                height=35
            )
            install_btn.pack(side="right", padx=10)
