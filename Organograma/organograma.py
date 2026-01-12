####################################################
###     gerador de organograma institucional     ###
####################################################
### Prof. Filipo Mor                             ###
####################################################
### github.com/ProfessorFilipo                   ###
####################################################

import tkinter as tk
from tkinter import messagebox, simpledialog


class OrgNode:
    """Classe para representar cada membro da organização."""

    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.children = []


class OrgChartApp:
    """Aplicação principal do Organograma usando Tkinter."""

    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Organograma Profissional")
        self.root.geometry("1100x750")

        # Variável para gerenciar o conflito entre clique simples e duplo
        self._click_timer = None

        # Dados iniciais
        self.root_member = OrgNode("Ana Silva", "CEO & Fundadora")
        dir_op = OrgNode("Carlos Santos", "Diretor de Operações")
        dir_mkt = OrgNode("Beatriz Costa", "Diretora de Marketing")

        self.root_member.children = [dir_op, dir_mkt]
        dir_op.children = [OrgNode("Mariana Lima", "Gerente de Projetos")]

        # Configuração da UI
        self.setup_ui()
        self.draw_chart()

    def setup_ui(self):
        """Configura os elementos da interface."""
        control_frame = tk.Frame(self.root, bg="#f8fafc", pady=15)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        title_label = tk.Label(
            control_frame,
            text="Estrutura Organizacional",
            font=("Segoe UI", 18, "bold"),
            bg="#f8fafc",
            fg="#0f172a"
        )
        title_label.pack(side=tk.LEFT, padx=30)

        self.canvas_frame = tk.Frame(self.root, bg="white")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        footer = tk.Label(
            self.root,
            text="• Clique: Adicionar Subordinado  • Clique Duplo: Editar  • Botão Direito: Remover",
            bg="#f1f5f9",
            fg="#475569",
            font=("Segoe UI", 10),
            pady=8
        )
        footer.pack(side=tk.BOTTOM, fill=tk.X)

    def draw_chart(self):
        """Redesenha o organograma do zero."""
        self.canvas.delete("all")
        # Largura inicial do buffer proporcional ao número de filhos da raiz para evitar sobreposição
        initial_buffer = max(500, len(self.root_member.children) * 200)
        self._draw_node(self.root_member, 550, 60, initial_buffer)

        # Garante que o scroll region englobe tudo e força atualização
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _draw_node(self, node, x, y, width_buffer):
        """Desenha o card do colaborador e suas conexões."""
        node_w = 190
        node_h = 70

        rect_color = "#f0f9ff" if node == self.root_member else "#ffffff"
        border_color = "#0ea5e9" if node == self.root_member else "#cbd5e1"

        tag = f"node_{id(node)}"

        # Sombra leve
        self.canvas.create_rectangle(
            x - node_w / 2 + 3, y + 3, x + node_w / 2 + 3, y + node_h + 3,
            fill="#f1f5f9", outline="", tags=tag
        )

        # Card principal
        self.canvas.create_rectangle(
            x - node_w / 2, y, x + node_w / 2, y + node_h,
            fill=rect_color, outline=border_color, width=2, tags=tag
        )

        self.canvas.create_text(
            x, y + 25, text=node.name if node.name else "Sem Nome",
            font=("Segoe UI", 10, "bold"), fill="#1e293b", tags=tag, width=170, justify="center"
        )
        self.canvas.create_text(
            x, y + 50, text=node.role.upper() if node.role else "CARGO",
            font=("Segoe UI", 8), fill="#64748b", tags=tag, width=170, justify="center"
        )

        # Eventos
        self.canvas.tag_bind(tag, "<Button-1>", lambda e, n=node: self.on_single_click(n))
        self.canvas.tag_bind(tag, "<Double-Button-1>", lambda e, n=node: self.on_double_click(n))
        self.canvas.tag_bind(tag, "<Button-3>", lambda e, n=node: self.remove_node(n))

        # Desenho dos Filhos
        if node.children:
            num_children = len(node.children)
            child_y = y + 120

            # Linha vertical saindo do pai
            self.canvas.create_line(x, y + node_h, x, y + node_h + 25, fill="#94a3b8", width=2)

            if num_children > 1:
                left_x = x - width_buffer / 2
                right_x = x + width_buffer / 2
                # Linha horizontal de conexão
                self.canvas.create_line(left_x, y + node_h + 25, right_x, y + node_h + 25, fill="#94a3b8", width=2)

                for i, child in enumerate(node.children):
                    child_x = left_x + (i * width_buffer / (num_children - 1))
                    self.canvas.create_line(child_x, y + node_h + 25, child_x, child_y, fill="#94a3b8", width=2)
                    self._draw_node(child, child_x, child_y, width_buffer / 2)
            else:
                # Apenas um filho: linha reta para baixo
                child_x = x
                self.canvas.create_line(child_x, y + node_h + 25, child_x, child_y, fill="#94a3b8", width=2)
                self._draw_node(node.children[0], child_x, child_y, width_buffer / 1.5)

    def on_single_click(self, node):
        """Gerencia o delay para não conflitar com duplo clique."""
        if self._click_timer:
            self.root.after_cancel(self._click_timer)

        # Usamos 300ms como tempo padrão de clique duplo do sistema
        self._click_timer = self.root.after(300, lambda: self.add_child(node))

    def on_double_click(self, node):
        """Cancela a ação de adicionar e abre a edição."""
        if self._click_timer:
            self.root.after_cancel(self._click_timer)
            self._click_timer = None
        self.edit_node(node)

    def add_child(self, parent_node):
        """Solicita dados e adiciona um subordinado."""
        self._click_timer = None

        name = simpledialog.askstring("Novo Subordinado", f"Nome para subordinado de {parent_node.name}:")
        if name is None: return  # Clicou em cancelar

        role = simpledialog.askstring("Cargo", "Informe o cargo:")
        if role is None: role = "Cargo"

        parent_node.children.append(OrgNode(name if name.strip() else "Novo Colaborador", role))
        self.draw_chart()

    def edit_node(self, node):
        """Edita informações do nodo clicado."""
        new_name = simpledialog.askstring("Editar", "Nome:", initialvalue=node.name)
        if new_name is None: return

        new_role = simpledialog.askstring("Editar", "Cargo:", initialvalue=node.role)
        if new_role is None: return

        node.name = new_name
        node.role = new_role
        self.draw_chart()

    def remove_node(self, node):
        """Remove colaborador e seus descendentes."""
        if node == self.root_member:
            messagebox.showwarning("Aviso", "A raiz da organização não pode ser removida.")
            return

        if messagebox.askyesno("Confirmar", f"Excluir {node.name} e todos os subordinados?"):
            self._delete_from_parent(self.root_member, node)
            self.draw_chart()

    def _delete_from_parent(self, current, target):
        for child in current.children:
            if child == target:
                current.children.remove(child)
                return True
            if self._delete_from_parent(child, target):
                return True
        return False


if __name__ == "__main__":
    root = tk.Tk()
    # Tenta definir um tema mais moderno se disponível
    try:
        root.tk.call('tk_setPalette', 'background', 'white', 'foreground', 'black')
    except:
        pass
    app = OrgChartApp(root)
    root.mainloop()
