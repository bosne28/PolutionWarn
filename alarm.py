import pandas as pd
import numpy as np
from tkinter import Tk, Text, Button, Scrollbar
import matplotlib.pyplot as plt
import winsound
from matplotlib.backends.backend_pdf import PdfPages


# Variabile globale
indexSim = 0
df_final = None
pauza = False  # Control pentru pauza
dateSim = np.empty((0, 4), dtype=object)  # numpy pentru stocarea datelor


# Citirea datelor
def readData():
    global df_final  # Indica faptul ca modifici variabila globala
    dfPM1 = pd.read_csv(r"C:\Users\bosne\Desktop\Python AI\Carei Satu Mare\Urad PM1.csv")
    dfPM10 = pd.read_csv(r"C:\Users\bosne\Desktop\Python AI\Carei Satu Mare\Urad PM10.csv")
    dfPM25 = pd.read_csv(r"C:\Users\bosne\Desktop\Python AI\Carei Satu Mare\Urad PM25.csv")
    #concateneaza toate DataFrame-urile
    df_concat = pd.concat([dfPM1, dfPM10, dfPM25], axis=1)
    #Elimina coloanele duplicate si creeaza o copie completa
    df_final = df_concat.loc[:, ~df_concat.columns.duplicated()].copy()
    #convertire timp UNIX
    df_final['time'] = pd.to_datetime(df_final['time'], unit='s')


# Afisarea si stocarea datelor curente
def simRead():
    global indexSim, pauza, dateSim
    if not pauza:  # Continua doar daca simularea nu este intrerupta
        if indexSim < len(df_final):
            nowTime = df_final["time"].iloc[indexSim]
            nowPM1 = df_final["pm1"].iloc[indexSim]
            nowPM10 = df_final["pm10"].iloc[indexSim]
            nowPM25 = df_final["pm25"].iloc[indexSim]

            # Afisare in text box
            textbox.config(state="normal")
            textnou = f"Time: {nowTime}, PM1: {round(nowPM1, 1)}, PM10: {round(nowPM10, 1)}, PM2.5: {round(nowPM25, 1)}\n"
            start_index = textbox.index("end-1c linestart")
            textbox.insert("end", textnou)
            # tinem textboxul scrollat
            textbox.yview_pickplace("end")
            # highlight si alarma pentru valori prea ridicate
            if nowPM1 > 100:
                textbox.tag_add("highlight_red", f"{start_index}+27c", f"{start_index}+37c")
                winsound.Beep(1000, 300)
            elif nowPM1>50:
                    textbox.tag_add("highlight_yellow", f"{start_index}+27c", f"{start_index}+37c")
            if nowPM10 > 120:
                textbox.tag_add("highlight_red", f"{start_index}+38c", f"{start_index}+49c")
                winsound.Beep(1000, 300)
            elif nowPM10>100:
                textbox.tag_add("highlight_yellow", f"{start_index}+38c", f"{start_index}+49c")
            if nowPM25 > 100:
                textbox.tag_add("highlight_red", f"{start_index}+51c", f"{start_index}+60c")
                winsound.Beep(1000, 300)
            elif nowPM25>50:
                textbox.tag_add("highlight_yellow", f"{start_index}+51c", f"{start_index}+60c")


            textbox.config(state="disabled")

            # Stocare in array NumPy
            new_entry = np.array([[nowTime, nowPM1, nowPM10, nowPM25]], dtype=object)
            dateSim = np.vstack([dateSim, new_entry])
            indexSim += 1
        # viteza simulare
        fereastra.after(10, simRead)


# incepere simularii
def startSim():
    global pauza
    pauza = False  # Reia simularea daca este intrerupta
    button_start.config(state="disabled")  # Dezactiveaza butonul de start
    button_pauza.config(state="normal")  # Activeaza butonul de pauza
    simRead()
    button_plot.config(state="disabled")

# Pauza simulare
def pauseSim():
    global pauza
    pauza = True  # intrerupe simularea
    button_start.config(state="normal")  # Activeaza butonul de start
    button_pauza.config(state="disabled")  # Dezactiveaza butonul de pauza
    button_plot.config(state="normal")



# Reprezentarea grafica a datelor stocate
def plotData():
    if dateSim.size > 0:
        times = dateSim[:, 0]
        pm1_values = dateSim[:, 1].astype(float)
        pm10_values = dateSim[:, 2].astype(float)
        pm25_values = dateSim[:, 3].astype(float)

        plt.figure(figsize=(10, 6))
        plt.plot(times, pm1_values, label="PM1")
        plt.plot(times, pm10_values, label="PM10")
        plt.plot(times, pm25_values, label="PM2.5")

        plt.xlabel("Timp")
        plt.ylabel("Concentratie (μg/m³)")
        plt.title("Evolutia concentratiilor de PM1, PM10 si PM2.5")
        plt.legend()
        plt.grid()
        plt.tight_layout()

        plt.show()
        button_saveplot.config(state="normal")
    else:
        print("Nu exista date de afisat in acest moment.")


def savePlot():
    times = dateSim[:, 0]
    pm1_values = dateSim[:, 1].astype(float)
    pm10_values = dateSim[:, 2].astype(float)
    pm25_values = dateSim[:, 3].astype(float)

    plt.figure(figsize=(10, 6))
    plt.plot(times, pm1_values, label="PM1")
    plt.plot(times, pm10_values, label="PM10")
    plt.plot(times, pm25_values, label="PM2.5")

    plt.xlabel("Timp")
    plt.ylabel("Concentratie (μg/m³)")
    plt.title("Evolutia concentratiilor de PM1, PM10 si PM2.5")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    locatiePDF = r"C:\Users\bosne\Desktop\grafic_poluanti.pdf"
    with PdfPages(locatiePDF) as pdf:
        pdf.savefig()


# Citirea datelor
readData()

# crearea ferestrei Tkinter
fereastra = Tk()
fereastra.title("Analiza poluanti")
fereastra.geometry("800x600")

# crearea unui text box pentru afisare
textbox = Text(fereastra, wrap="word", width=90, height=25)
textbox.pack(pady=10)

#configuram taguri pentru evidentiere in textbox
textbox.tag_configure("highlight_yellow", background="yellow")
textbox.tag_configure("highlight_red", background="red")
# Crearea butoanelor
button_start = Button(fereastra, text="Porneste simularea", command=startSim)
button_start.pack(pady=10)

button_pauza = Button(fereastra, text="Pune pe pauza", command=pauseSim, state="disabled")
button_pauza.pack(pady=10)

button_plot = Button(fereastra, text="Reprezinta grafic", command=plotData, state="disabled")
button_plot.pack(pady=10)

button_saveplot = Button(fereastra, text="Salveaza grafic", command=savePlot, state="disabled")
button_saveplot.pack(pady=10)

# Afisare fereastra
fereastra.mainloop()
