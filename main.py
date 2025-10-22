import flet as ft
from alert import AlertManager
from automobile import Automobile
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    input_marca = ft.TextField(label='Marca',width=200)
    input_modello = ft.TextField(label='Modello',width=200)
    input_anno = ft.TextField(label='Anno',width=150)

    #inseriamo il contatore per il numero posti
    posti = ft.Text(value='0',width=30,text_align=ft.TextAlign.CENTER)

    #inserisco i punlsanti per modificare il numero di posti

    def incrementa_posti(e):
        posti.value = str(int(posti.value) + 1)
        page.update()
    def decrementa_posti(e):
        if int(posti.value) > 0:
            posti.value = str(int(posti.value) - 1)
            page.update()

    btn_piu = ft.IconButton(icon=ft.Icons.ADD,icon_color='green',icon_size=21,on_click=incrementa_posti)
    btn_meno = ft.IconButton(icon= ft.Icons.REMOVE,icon_color='red',icon_size=21,on_click=decrementa_posti)
    txtOut = ft.TextField(width=200,disabled=True,value=0,border_color='green',text_align=ft.TextAlign.CENTER)


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto

    def aggiungi_automobile(e):
        marca = input_marca.value.strip()
        modello = input_modello.value.strip()
        anno = input_anno.value.strip()
        numero_posti = posti.value.strip()

        #ora passiamo al controllo dei campi vuoti
        if not marca or not modello or not anno or not numero_posti:
            alert.show_alert('❌ tutti i campi devono essere compilati.')
            return

        #ora eseguiamo un controllo anche sui vallori numerici
        if not anno.isdigit() or not numero_posti.isdigit():
            alert.show_alert('❌  ERRORE: inserisci valori numerici validi per anno e posti')
            return

        try:
            #aggiungiamo l'auto alla struttura dati
            autonoleggio.aggiungi_automobile(marca, modello, int(anno), int(numero_posti))

            #ora bisogna preoccuparsi di pulire i campi
            #dopo l'aggiunga di ogni macchina

            input_marca.value = ''
            input_modello.value = ''
            input_anno.value = ''
            posti.value = '0'

            #SI AGGIORNI LA LISTA CHE VIENE VISUALIZZATA
            aggiorna_lista_auto()
            page.update()

        except Exception as errore:
            alert.show_alert(f'❌ {errore}')

    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    btn_aggiungi_auto = ft.ElevatedButton('aggiungi automobile', on_click=aggiungi_automobile)

    # --- EVENTI ---


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text('Aggiungi nuova auto', size = 30),
        ft.Row(controls=[input_marca,input_modello,input_anno,btn_meno,posti,btn_piu],alignment=ft.MainAxisAlignment.CENTER,
               ),
        btn_aggiungi_auto,

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
