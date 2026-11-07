#!/usr/bin/env python3
"""
ExplorEstable — explorador de archivos multiplataforma (Windows, macOS, Linux).

Es de SOLO LECTURA: no copia, mueve, renombra ni borra nada, y no reemplaza
al explorador de archivos de tu sistema. Solo usa la biblioteca estándar.
Uso:  python explorestable.py [carpeta]
"""
import os, sys, locale, subprocess, datetime, tkinter as tk
from tkinter import ttk, messagebox

KEYS = "up home refresh system hidden search name type size modified folder file items error".split()
L = {  # idioma: textos en el mismo orden que KEYS, separados por |
    "Español":   "Subir|Inicio|Actualizar|Abrir en el sistema|Mostrar ocultos|Buscar…|Nombre|Tipo|Tamaño|Modificado|Carpeta|Archivo|elementos|Error",
    "English":   "Up|Home|Refresh|Open in system|Show hidden|Search…|Name|Type|Size|Modified|Folder|File|items|Error",
    "Français":  "Monter|Accueil|Actualiser|Ouvrir dans le système|Afficher cachés|Rechercher…|Nom|Type|Taille|Modifié|Dossier|Fichier|éléments|Erreur",
    "Deutsch":   "Hoch|Start|Aktualisieren|Im System öffnen|Versteckte zeigen|Suchen…|Name|Typ|Größe|Geändert|Ordner|Datei|Elemente|Fehler",
    "Português": "Subir|Início|Atualizar|Abrir no sistema|Mostrar ocultos|Pesquisar…|Nome|Tipo|Tamanho|Modificado|Pasta|Arquivo|itens|Erro",
    "Italiano":  "Su|Home|Aggiorna|Apri nel sistema|Mostra nascosti|Cerca…|Nome|Tipo|Dimensione|Modificato|Cartella|File|elementi|Errore",
    "中文":       "上一级|主目录|刷新|在系统中打开|显示隐藏文件|搜索…|名称|类型|大小|修改时间|文件夹|文件|项|错误",
    "日本語":     "上へ|ホーム|更新|システムで開く|隠しファイルを表示|検索…|名前|種類|サイズ|更新日時|フォルダ|ファイル|項目|エラー",
    "Русский":   "Вверх|Домой|Обновить|Открыть в системе|Показать скрытые|Поиск…|Имя|Тип|Размер|Изменён|Папка|Файл|элементов|Ошибка",
    "한국어":      "위로|홈|새로고침|시스템에서 열기|숨김 표시|검색…|이름|유형|크기|수정한 날짜|폴더|파일|항목|오류",
}
LANGS = {n: dict(zip(KEYS, s.split("|"))) for n, s in L.items()}
CODES = dict(zip(L, "es en fr de pt it zh ja ru ko".split()))


def system_lang():
    try:
        code = (locale.getlocale()[0] or "en")[:2].lower()
    except Exception:
        code = "en"
    return next((n for n, c in CODES.items() if c == code), "English")


def open_with_system(path):
    """Abre un archivo o carpeta con la aplicación predeterminada del SO."""
    if sys.platform.startswith("win"):
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def human(n):
    if n < 1024:
        return f"{n} B"
    for u in ("KB", "MB", "GB", "TB"):
        n /= 1024
        if n < 1024:
            return f"{n:.1f} {u}"
    return f"{n / 1024:.1f} PB"


class ExplorEstable(tk.Tk):
    def __init__(self, start=None):
        super().__init__()
        self.title("ExplorEstable")
        self.geometry("920x580")
        self.minsize(640, 360)
        self.lang = tk.StringVar(value=system_lang())
        self.hidden = tk.BooleanVar(value=False)
        self.query = tk.StringVar()
        self.addr = tk.StringVar()
        self.sort = ("name", False)  # (columna, descendente)
        self.paths = {}
        self.path = os.path.abspath(start or os.path.expanduser("~"))
        self.build()
        self.apply_lang()
        self.load(self.path)

    def t(self, key):
        return LANGS[self.lang.get()][key]

    # ---------- interfaz ----------
    def build(self):
        bar = ttk.Frame(self, padding=(8, 8, 8, 2))
        bar.pack(fill="x")
        self.b_up = ttk.Button(bar, command=self.go_up)
        self.b_home = ttk.Button(bar, command=lambda: self.load(os.path.expanduser("~")))
        self.b_ref = ttk.Button(bar, command=lambda: self.load(self.path))
        for b in (self.b_up, self.b_home, self.b_ref):
            b.pack(side="left", padx=(0, 4))
        entry = ttk.Entry(bar, textvariable=self.addr)
        entry.pack(side="left", fill="x", expand=True, padx=4)
        entry.bind("<Return>", lambda e: self.load(self.addr.get()))
        cb = ttk.Combobox(bar, textvariable=self.lang, values=list(L), state="readonly", width=11)
        cb.pack(side="right")
        cb.bind("<<ComboboxSelected>>", lambda e: (self.apply_lang(), self.load(self.path)))

        bar2 = ttk.Frame(self, padding=(8, 2, 8, 6))
        bar2.pack(fill="x")
        self.search = ttk.Entry(bar2, textvariable=self.query, width=28)
        self.search.pack(side="left")
        self.query.trace_add("write", lambda *a: self.load(self.path))
        self.c_hidden = ttk.Checkbutton(bar2, variable=self.hidden, command=lambda: self.load(self.path))
        self.c_hidden.pack(side="left", padx=10)
        self.b_sys = ttk.Button(bar2, command=lambda: self.safe_open(self.path))
        self.b_sys.pack(side="right")

        cols = ("name", "type", "size", "modified")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", selectmode="browse")
        for c, w in zip(cols, (420, 110, 90, 160)):
            self.tree.column(c, width=w, anchor="e" if c == "size" else "w")
            self.tree.heading(c, command=lambda c=c: self.set_sort(c))
        sb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.status = ttk.Label(self, anchor="w", padding=(8, 3))
        self.status.pack(side="bottom", fill="x")
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, side="left")
        self.tree.bind("<Double-1>", self.activate)
        self.tree.bind("<Return>", self.activate)
        self.bind("<BackSpace>", lambda e: self.go_up() if self.focus_get() is self.tree else None)
        self.bind("<F5>", lambda e: self.load(self.path))

    def apply_lang(self):
        self.b_up.config(text="⬆ " + self.t("up"))
        self.b_home.config(text="⌂ " + self.t("home"))
        self.b_ref.config(text="⟳ " + self.t("refresh"))
        self.b_sys.config(text=self.t("system"))
        self.c_hidden.config(text=self.t("hidden"))
        for c in ("name", "type", "size", "modified"):
            self.tree.heading(c, text=self.t(c))

    # ---------- lógica ----------
    def set_sort(self, col):
        self.sort = (col, not self.sort[1] if self.sort[0] == col else False)
        self.load(self.path)

    def go_up(self):
        self.load(os.path.dirname(self.path))

    def safe_open(self, path):
        try:
            open_with_system(path)
        except Exception as e:
            messagebox.showerror(self.t("error"), str(e))

    def activate(self, _=None):
        sel = self.tree.selection()
        if not sel:
            return
        path, is_dir = self.paths[sel[0]]
        self.load(path) if is_dir else self.safe_open(path)

    def load(self, path):
        path = os.path.abspath(os.path.expanduser(path))
        try:
            entries = list(os.scandir(path))
        except Exception as e:
            messagebox.showerror(self.t("error"), str(e))
            self.addr.set(self.path)
            return
        self.path = path
        self.addr.set(path)
        q = self.query.get().strip().lower()
        rows = []
        for e in entries:
            try:
                is_dir = e.is_dir()
                st = e.stat()
            except OSError:
                continue
            hidden = e.name.startswith(".") or bool(getattr(st, "st_file_attributes", 0) & 2)
            if (hidden and not self.hidden.get()) or (q and q not in e.name.lower()):
                continue
            rows.append((e.name, is_dir, st.st_size, st.st_mtime, e.path))

        col, desc = self.sort
        keys = {
            "name": lambda r: r[0].lower(),
            "type": lambda r: os.path.splitext(r[0])[1].lower(),
            "size": lambda r: r[2],
            "modified": lambda r: r[3],
        }
        rows.sort(key=keys[col], reverse=desc)
        rows.sort(key=lambda r: not r[1])  # carpetas primero (orden estable)

        self.tree.delete(*self.tree.get_children())
        self.paths.clear()
        for name, is_dir, size, mtime, full in rows:
            kind = self.t("folder") if is_dir else (os.path.splitext(name)[1][1:].upper() or self.t("file"))
            when = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            icon = "📁 " if is_dir else "📄 "
            iid = self.tree.insert("", "end", values=(icon + name, kind, "" if is_dir else human(size), when))
            self.paths[iid] = (full, is_dir)
        self.status.config(text=f"{len(rows)} {self.t('items')}  —  {path}")


if __name__ == "__main__":
    try:
        ExplorEstable(sys.argv[1] if len(sys.argv) > 1 else None).mainloop()
    except tk.TclError as e:
        sys.exit(f"No se pudo abrir la ventana gráfica: {e}")
