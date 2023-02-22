import os

from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor, QTextCharFormat
from PyQt5.QtWidgets import QApplication, QInputDialog, QListWidgetItem, QMessageBox


def confirm(titulo, texto):
    m = QMessageBox(window)
    m.setIcon(QMessageBox.Question)
    m.setWindowTitle(titulo)
    m.setText(texto)
    m.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    m.button(QMessageBox.Yes).setText("Sim")
    m.button(QMessageBox.No).setText("Não")
    return m.exec()


def formatar(d, cor):
    estilo = QTextCharFormat()
    estilo.setBackground(QColor(cor))
    t.calendario.setDateTextFormat(QDate.fromString(d, 'yyyy-M-d'), estilo)


def carregar():
    # destaca os dias com compromissos
    for f in os.listdir('.'):
        if f.endswith('.dat'):
            formatar(f.split('.dat')[0], '#FF3131')  # neon red

    get_dia()  # busca o dia atual
    t.lista.clear()  # limpa a lista

    try:
        f = open(str(dia) + '.dat', 'r')  # abre o arquivo da data atual
        compromissos = f.readlines()  # carrega os compromissos do dia
    except FileNotFoundError as e:
        compromissos = []  # não há compromissos neste dia

    # cria a agenda do dia com horários de meia-noite às onze da noite
    for h in range(24):
        compromisso = str(h) + 'h '  # compromisso vazio na hora atual

        # verifica se há compromisso para a hora atual neste dia
        for c in compromissos:
            if c.startswith(compromisso):
                compromisso = c.replace('\n', '')

        # item sem formatação
        # t.lista.addItem(compromisso)

        # item formatado
        item = QListWidgetItem(compromisso)
        if h % 2 == 0:
            item.setBackground(QColor('#eee'))
        t.lista.addItem(item)


def get_dia():
    global dia
    dia = t.calendario.selectedDate().toPyDate()


def sair():
    exit()


def salvar(compromisso, hora):
    f = open(str(dia) + '.dat', 'a')  # append
    f.write(hora + 'h ' + compromisso + '\n')
    f.close()


def editar():
    global window
    hora = t.lista.currentItem().text().split('h ')[0]
    compromisso, ok = QInputDialog.getText(window, 'Editar compromisso', 'Detalhes:')
    if ok:
        salvar(compromisso, hora)
        carregar()


def excluir():
    if confirm('Excluindo compromisso', 'Confirma exclusão?') == QMessageBox.No:
        return

    hora = t.lista.currentItem().text().split('h ')[0]

    f = open(str(dia) + '.dat', 'r+')  # abre o arquivo do dia atual
    compromissos = f.readlines()  # busca a lista de compromissos do dia

    # remove o compromisso da lista
    for i, c in enumerate(compromissos):
        prefixo = str(hora) + 'h '
        if c.startswith(prefixo):
            compromissos.pop(i)
            break

    f.seek(0)  # move para o início do arquivo
    f.truncate()  # exclui o conteúdo do arquivo
    f.writelines(compromissos)  # substitui o conteúdo do arquivo
    f.close()  # fecha o arquivo
    carregar()  # recarrega a lista na tela


def nova():
    if confirm('Nova agenda', 'Confirma exclusão de todos os compromissos?') == QMessageBox.No:
        return

    # exclui todos os arquivos com extensão '.dat'
    for a in os.listdir('.'):
        if a.endswith('.dat'):
            formatar(a.split('.dat')[0], 'white')
            os.remove(a)
    # [os.remove(a) for a in os.listdir('.') if a.endswith('.dat')]
    carregar()


def habilitar_botao_excluir():
    if t.lista.currentItem().text().split('h ')[1]:
        t.excluir.setEnabled(True)


# Inicializando os componentes da janela PyQt5
app = QApplication([])

# inicializando a janela pelo arquivo .ui
Form, Window = uic.loadUiType("main.ui")
t = Form()
window = Window()

# inicializando a janela pelo arquivo .py convertido por "pyuic5 -x main.ui -o main_ui.py"
# t = Ui_MainWindow()
# window = QMainWindow()

t.setupUi(window)  # carrega os componentes

# define os eventos dos botões
t.actionSair.triggered.connect(sair)  # QAction usa triggered ao invés de clicked
t.actionNova.triggered.connect(nova)
t.calendario.clicked.connect(carregar)
t.lista.itemDoubleClicked.connect(editar)
t.lista.itemClicked.connect(habilitar_botao_excluir)
t.lista.itemSelectionChanged.connect(lambda: t.excluir.setEnabled(False))
t.excluir.clicked.connect(excluir)

dia = t.calendario.selectedDate().toPyDate()
carregar()

# apresenta a janela
window.show()
app.exec()
