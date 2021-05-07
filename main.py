from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import psycopg2
import pandas as pd
import re
from configparser import ConfigParser
import json


selecct = ("""select distinct
                                                       a.metadata_json ->> '31' as cnpj,
                                                       a.metadata_json ->> '12' as nota,
                                                       a.metadata_json ->> '13' as serie,
                                                       CASE
                                                           WHEN (a.metadata_json ->> '11'::text) = '1'::text THEN 'DISPONIVEL'::text
                                                           WHEN (a.metadata_json ->> '11'::text) = '2'::text THEN 'NÃO DISPONIVEL'::text
                                                           ELSE ''::text
                                                       END AS "STATUS DIGITALIZACAO",
                                                       CASE
                                                           WHEN (a.metadata_json ->> '10'::text) = '3'::text THEN 'DISPONIVEL'::text
                                                           WHEN (a.metadata_json ->> '10'::text) = '4'::text THEN 'NÃO DISPONIVEL'::text
                                                           ELSE ''::text
                                                       END AS "STATUS INTEGRACAO",
                                                       a.metadata_json ->> '20' as emissao,
                                                       a.metadata_json ->> '17' as processamento,
                                                       a.metadata_json ->> '45' as transportadora,
                                                       a.metadata_json ->> '74' as protocolo,
                                                       a.metadata_json ->> '75' as caixa,
                                                       a.metadata_json ->> '78' as local,
                                                       a.metadata_json ->> '79' AS cod_origem,
                                                       CASE
                                                           WHEN (a.metadata_json ->> '79'::text) = '17'::text THEN 'ACHE'::text
                                                           WHEN (a.metadata_json ->> '79'::text) = '18'::text THEN 'ATLAS'::text
                                                           WHEN (a.metadata_json ->> '79'::text) = '19'::text THEN 'EXPRESSO JUNDIAI'::text
                                                           WHEN (a.metadata_json ->> '79'::text) = '22'::text THEN 'ACHE LEGADO'::text
                                                           WHEN (a.metadata_json ->> '79'::text) = '25'::text THEN 'RV IMOLA'::text
                                                           WHEN (a.metadata_json ->> '79'::text) = '26'::text THEN 'SOLISTICA'::text
                                                           ELSE ''::text
                                                       END AS "INDEXADO POR",
                                                       right(a.metadata_json ->> '20',4) || substring(a.metadata_json ->> '20',4,2) || left(a.metadata_json ->> '20',2) as "ORDEM"   -- emissão
                                                from document a
                                                where a.document_type_id = 3
                                                  and right(a.metadata_json ->> '20',4) || substring(a.metadata_json ->> '20',4,2) || left(a.metadata_json ->> '20',2) >= '%s'
                                                  and right(a.metadata_json ->> '20',4) || substring(a.metadata_json ->> '20',4,2) || left(a.metadata_json ->> '20',2) <= '%s'
                                                order by right(a.metadata_json ->> '20',4) || substring(a.metadata_json ->> '20',4,2) || left(a.metadata_json ->> '20',2)""")


config5 = {'select': selecct}

pd.options.display.max_seq_items = None

with open('config.json', 'r') as f:
    config5 = json.load(f)

with open('config.json', 'w') as f:
    json.dump(config5, f)

config = ConfigParser()
config.read('config.ini')
try:
    config.add_section('main')
    config.set('main', 'user', '********')
    config.set('main', 'password', '********')
    config.set('main', 'host', '********')
    config.set('main', 'port', '********')
    config.set('main', 'database', '********')
except:
    print('arquivo de config.ini criado com sucesso!')

userDB = str(config.get('main', 'user'))
passDB = str(config.get('main', 'password'))
hostDB = str(config.get('main', 'host'))
portDB = str(config.get('main', 'port'))
database = str(config.get('main', 'database'))

with open('config.ini', 'w') as f:
    config.write(f)

connection = psycopg2.connect(user=userDB,
                              password=passDB,
                              host=hostDB,
                              port=portDB,
                              database=database)
cursor = connection.cursor()

try:
    root = Tk()
    root.geometry("928x581+882+90")
    root.minsize(120, 1)
    root.maxsize(1924, 1061)
    root.resizable(1, 1)
    root.title("New Toplevel")
    root.configure(background="#d9d9d9")

    my_notebook = ttk.Notebook(root)
    my_notebook.place(relx=0.011, rely=0.0, relheight=0.993, relwidth=0.983)

    my_frame1 = Frame(my_notebook, width=500, height=500)
    my_frame2 = Frame(my_notebook, width=500, height=500)

    my_frame1.pack(fill="both", expand=1)
    my_frame2.pack(fill="both", expand=1)

    my_notebook.add(my_frame1, text="Select Tab")
    my_notebook.add(my_frame2, text="Config Tab")
    TSeparator1 = ttk.Separator(my_frame1)
    TSeparator1.place(relx=-0.011, rely=0.733, relwidth=0.989)

    TFrame1 = ttk.Frame(my_frame1)
    TFrame1.place(relx=0.7, rely=0.755, relheight=0.211, relwidth=0.284)
    TFrame1.configure(relief='groove')
    TFrame1.configure(borderwidth="2")
    TFrame1.configure(relief="groove")

    text = Text(my_frame1)
    # text.pack(expand=YES, fill=BOTH)
    ScrollBar = Scrollbar(root)
    ScrollBar.config(command=text.yview)
    text.config(yscrollcommand=ScrollBar.set)
    ScrollBar.pack(side=RIGHT, fill=Y)
    text.place(relx=0.001, rely=0.001, height=398, width=890)

    dataF = Entry(my_frame1)
    dataF.place(relx=0.710, rely=0.79, relheight=0.041, relwidth=0.148)
    dataF.insert(0, '30/03/2021')

    dataL = Entry(my_frame1)
    dataL.place(relx=0.710, rely=0.85, relheight=0.041, relwidth=0.148)
    dataL.insert(0, '31/03/2021')

    label1 = Label(my_frame1, text="Data Inicial")
    label1.place(relx=0.870, rely=0.79)

    label2 = Label(my_frame1, text="Data Final")
    label2.place(relx=0.870, rely=0.85)

    TFrame2 = ttk.Frame(my_frame2)
    TFrame2.place(relx=0.01, rely=0.04, relheight=0.311, relwidth=0.280)
    TFrame2.configure(relief='groove')
    TFrame2.configure(borderwidth="2")
    TFrame2.configure(relief="groove")

    userL = Label(TFrame2, text=("User = "))
    userL.place(relx=0.070, rely=0.040)

    userC = Entry(TFrame2)
    userC.place(relx=0.230, rely=0.040)
    userC.insert(0, userDB)

    passL = Label(TFrame2, text=("Pass = "))
    passL.place(relx=0.070, rely=0.140)

    passC = Entry(TFrame2)
    passC.place(relx=0.230, rely=0.140)
    passC.insert(0, passDB)

    hostL = Label(TFrame2, text=("Host = "))
    hostL.place(relx=0.070, rely=0.240)

    hostC = Entry(TFrame2)
    hostC.place(relx=0.230, rely=0.240)
    hostC.insert(0, hostDB)

    portL = Label(TFrame2, text=("Port = "))
    portL.place(relx=0.070, rely=0.340)

    portC = Entry(TFrame2)
    portC.place(relx=0.230, rely=0.340)
    portC.insert(0, portDB)

    dbL = Label(TFrame2, text=("Db = "))
    dbL.place(relx=0.070, rely=0.440)

    dbC = Entry(TFrame2)
    dbC.place(relx=0.230, rely=0.440)
    dbC.insert(0, database)

    TFrame3 = ttk.Frame(my_frame2)
    TFrame3.place(relx=0.300, rely=0.780, relheight=0.211, relwidth=0.660)
    TFrame3.configure(relief='groove')
    TFrame3.configure(borderwidth="2")
    TFrame3.configure(relief="groove")

    selecttext = Text(my_frame2)
    # text.pack(expand=YES, fill=BOTH)
    ScrollBar = Scrollbar(root)
    ScrollBar.config(command=selecttext.yview)
    selecttext.config(yscrollcommand=ScrollBar.set)
    ScrollBar.pack(side=RIGHT, fill=Y)
    selecttext.place(relx=0.300, rely=0.040, height=398, width=590)

    try:
        def btnClickFunction():
            global df,tratada,dfmain
            print("\n" * 2)
            start_date = dataF.get()
            end_date = dataL.get()
            # variavel do textbox(DATA DE INICIO)
            # CONVERTENDO DATA PARA QUERY
            def data_fomart(dt):
                return re.sub(r'(\d{1,2})/(\d{1,2})/(\d{4})', '\\3\\2\\1', dt)

            dataFormatada1 = data_fomart(start_date)
            dataFormatada2 = data_fomart(end_date)
            try:
                postgreSQL_select_Query = """select distinct
                                                       a.metadata_json ->> '31' as cnpj,
                                                       a.metadata_json ->> '12' as nota,
                                                       a.metadata_json ->> '13' as serie,
                                                       CASE
                                                           WHEN (a.metadata_json ->> '11'::text) = '1'::text THEN 'DISPONIVEL'::text
                                                           WHEN (a.metadata_json ->> '11'::text) = '2'::text THEN 'NÃO DISPONIVEL'::text
                                                           ELSE ''::text
                                                       END AS "STATUS DIGITALIZACAO",
                                                       CASE
                                                           WHEN (a.metadata_json ->> '10'::text) = '3'::text THEN 'DISPONIVEL'::text
                                                           WHEN (a.metadata_json ->> '10'::text) = '4'::text THEN 'NÃO DISPONIVEL'::text
                                                           ELSE ''::text
                                                       END AS "STATUS INTEGRACAO",
                                                       a.metadata_json ->> '20' as emissao,
                                                       a.metadata_json ->> '17' as processamento,
                                                       a.metadata_json ->> '45' as transportadora,
                                                       a.metadata_json ->> '74' as protocolo,
                                                       a.metadata_json ->> '75' as caixa,
                                                       a.metadata_json ->> '78' as local,
                                                       a.metadata_json ->> '79' AS cod_origem,
                                                       CASE
                                                           WHEN (a.metadata_json ->> '79'::text) = '17'::text THEN 'ACHE'::text
                                                           WHEN (a.metadata_json ->> '79'::text) = '18'::text THEN 'ATLAS'::text
                                                           WHEN (a.metadata_json ->> '79'::text) = '19'::text THEN 'EXPRESSO JUNDIAI'::text
                                                           WHEN (a.metadata_json ->> '79'::text) = '22'::text THEN 'ACHE LEGADO'::text
                                                           WHEN (a.metadata_json ->> '79'::text) = '25'::text THEN 'RV IMOLA'::text
                                                           WHEN (a.metadata_json ->> '79'::text) = '26'::text THEN 'SOLISTICA'::text
                                                           ELSE ''::text
                                                       END AS "INDEXADO POR",
                                                       right(a.metadata_json ->> '20',4) || substring(a.metadata_json ->> '20',4,2) || left(a.metadata_json ->> '20',2) as "ORDEM"   -- emissão
                                                from document a
                                                where a.document_type_id = 3
                                                  and right(a.metadata_json ->> '20',4) || substring(a.metadata_json ->> '20',4,2) || left(a.metadata_json ->> '20',2) >= '%s'
                                                  and right(a.metadata_json ->> '20',4) || substring(a.metadata_json ->> '20',4,2) || left(a.metadata_json ->> '20',2) <= '%s'
                                                order by right(a.metadata_json ->> '20',4) || substring(a.metadata_json ->> '20',4,2) || left(a.metadata_json ->> '20',2)""" % (
                        dataFormatada1, dataFormatada2)
                df = pd.read_sql(postgreSQL_select_Query, connection)




                tratada = config.get('Select') % (dataFormatada1, dataFormatada2)


            except:
                ...

            ######################
            # filtro by date
            func = df[df.emissao.between(start_date, end_date)]
            # pritando no textbox
            text.delete('1.0', END)
            text.insert(INSERT, func)
            text.insert(INSERT, '\nData Inicial:'+str(dataFormatada1)+'\nData Final:'+str(dataFormatada2)+'\n')

        def saveGUI2():
            saveG = Tk()
            saveG.geometry("250x80+1200+210")
            saveG.minsize(120, 1)
            saveG.maxsize(200, 200)
            saveG.resizable(0, 0)
            saveG.title("Save")
            saveG.configure(background="#d9d9d9")

            saveLabel = Label(saveG, text='Exportar para CSV')
            saveLabel.place(relx=0.25, rely=0.1)

            def saveAS():
                try:
                    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
                    df2.to_csv(export_file_path, index=False, header=True)
                    saveG.quit()
                except:
                    text.delete('1.0', END)
                    text.insert(INSERT, 'ERROR: \nData not defined')
            def quitS():
                ...

            saveguiB = Button(saveG, text="Yes", command=saveAS).place(relx=0.01, rely=0.55, height=24, width=87)
            quitB = Button(saveG, text="No", command=quitS).place(relx=0.55, rely=0.55, height=24, width=87)

            saveG.mainloop()


        def selectsaves():
            config5['select'] = selecttext.get('1.0', END)
            with open('config.json', 'w') as f:
                json.dump(config5, f)
        def select():
            with open('config.json', 'r') as f:
                config5 = json.load(f)
            selecttext.delete('1.0', END)
            #text.insert(INSERT, config1.get('Select'))
            selecttext.insert(INSERT, config5.get('select'))

        def alterarconfig():
            config.set('main', 'user', userC.get())
            config.set('main', 'password', passC.get())
            config.set('main', 'host', hostC.get())
            config.set('main', 'port', portC.get())
            config.set('main', 'database', dbC.get())
            with open('config.ini', 'w') as f:
                config.write(f)
        def select1():
            global df2
            tratada2 = config5.get('select')

            df2 = pd.read_sql(tratada2, connection)
            selectsave1 = df2

            saveGUI2()


            text.delete('1.0', END)
            text.insert(INSERT, selectsave1)


        def testselect():

            datx = """select distinct
                                                   a.metadata_json ->> '31' as cnpj,
                                                   a.metadata_json ->> '12' as nota,
                                                   a.metadata_json ->> '13' as serie,
                                                   CASE
                                                       WHEN (a.metadata_json ->> '11'::text) = '1'::text THEN 'DISPONIVEL'::text
                                                       WHEN (a.metadata_json ->> '11'::text) = '2'::text THEN 'NÃO DISPONIVEL'::text
                                                       ELSE ''::text
                                                   END AS "STATUS DIGITALIZACAO",
                                                   CASE
                                                       WHEN (a.metadata_json ->> '10'::text) = '3'::text THEN 'DISPONIVEL'::text
                                                       WHEN (a.metadata_json ->> '10'::text) = '4'::text THEN 'NÃO DISPONIVEL'::text
                                                       ELSE ''::text
                                                   END AS "STATUS INTEGRACAO",
                                                   a.metadata_json ->> '20' as emissao,
                                                   a.metadata_json ->> '17' as processamento,
                                                   a.metadata_json ->> '45' as transportadora,
                                                   a.metadata_json ->> '74' as protocolo,
                                                   a.metadata_json ->> '75' as caixa,
                                                   a.metadata_json ->> '78' as local,
                                                   a.metadata_json ->> '79' AS cod_origem,
                                                   CASE
                                                       WHEN (a.metadata_json ->> '79'::text) = '17'::text THEN 'ACHE'::text
                                                       WHEN (a.metadata_json ->> '79'::text) = '18'::text THEN 'ATLAS'::text
                                                       WHEN (a.metadata_json ->> '79'::text) = '19'::text THEN 'EXPRESSO JUNDIAI'::text
                                                       WHEN (a.metadata_json ->> '79'::text) = '22'::text THEN 'ACHE LEGADO'::text
                                                       WHEN (a.metadata_json ->> '79'::text) = '25'::text THEN 'RV IMOLA'::text
                                                       WHEN (a.metadata_json ->> '79'::text) = '26'::text THEN 'SOLISTICA'::text
                                                       ELSE ''::text
                                                   END AS "INDEXADO POR",
                                                   right(a.metadata_json ->> '20',4) || substring(a.metadata_json ->> '20',4,2) || left(a.metadata_json ->> '20',2) as "ORDEM"   -- emissão
                                            from document a
                                            where a.document_type_id = 3
                                              and right(a.metadata_json ->> '20',4) || substring(a.metadata_json ->> '20',4,2) || left(a.metadata_json ->> '20',2) >= '20210325'
                                              and right(a.metadata_json ->> '20',4) || substring(a.metadata_json ->> '20',4,2) || left(a.metadata_json ->> '20',2) <= '20210326'
                                            order by right(a.metadata_json ->> '20',4) || substring(a.metadata_json ->> '20',4,2) || left(a.metadata_json ->> '20',2)"""

            xf = pd.DataFrame(df, columns=['cnpj', 'nota', 'serie', 'STATUS DIGITALIZACAO', 'STATUS INTEGRACAO',
       'emissao', 'processamento', 'transportadora', 'protocolo', 'caixa',
       'local', 'cod_origem', 'INDEXADO POR', 'ORDEM'])
            text.delete('1.0', END)
            text.insert(INSERT, xf)

        def salvardiretorio():
            try:
                export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
                df.to_csv(export_file_path, index=False, header=True)
            except:
                text.delete('1.0', END)
                text.insert(INSERT, 'ERROR: \nData not defined')
    except:
        ...


    my_button = Button(my_frame1, text="Salvar", command=salvardiretorio).place(relx=0.009, rely=0.750, height=24, width=87)

    my_button6 = Button(my_frame1, text="Select 1", command=select1).place(relx=0.110, rely=0.750, height=24, width=87)

    my_button6 = Button(my_frame1, text="Select 2", command=testselect).place(relx=0.210, rely=0.750, height=24, width=87)

    my_button2 = Button(my_frame2, text="Select", command=select).place(relx=0.310, rely=0.810, height=24, width=87)

    my_button5 = Button(my_frame2, text="Select Save", command=selectsaves).place(relx=0.410, rely=0.810, height=24, width=87)

    my_button3 = Button(my_frame1, text="Buscar", command=btnClickFunction).place(relx=0.710, rely=0.910, height=24, width=87)

    my_button4 = Button(my_frame2, text="Alterar", command=alterarconfig).place(relx=0.030, rely=0.250, height=24, width=87)


    TSeparator1 = ttk.Separator(my_frame1)
    TSeparator1.place(relx=0.009, rely=0.733, relwidth=0.979)

    root.mainloop()
except:
    ...
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
