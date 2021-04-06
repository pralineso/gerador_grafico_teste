import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import seaborn as sns
sns.set(rc={'figure.figsize':(12, 6)})

st.set_option('deprecation.showPyplotGlobalUse', False)

#A função plotTimeseriesVariable recebe os pramentros nos seguintes formatos:
#   d_id = int
#   variable = string 
#   start_time  = dateTime
#   end_time = dateTime
# e gera os um grafico com base na variable especificada

def plotTimeseriesVariable(d_id, variable, start_time, end_time, base):
    d_id = int(d_id)
    ax = base[base['device_id'] == d_id][variable].loc[start_time : end_time].plot(marker='.')
    ax.xaxis.set_major_locator(mdates.HourLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m-%H:%M'))
    plt.xlabel('')
    plt.title('Gráfico: Tempo por {}'.format(variable))
    ax.legend( loc=3)
    st.pyplot()

def plotDiffEnergy(d_id, min_tempo, max_tempo, base):
    ax = base[base['device_id'] == d_id][['act_pow', 'exp_pow']].loc[min_tempo : max_tempo].plot(marker='.')
    ax.xaxis.set_major_locator(mdates.HourLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m-%H:%M'))
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    plt.ylim(0, 3000)
    plt.xlabel('')
    plt.title('Energia aferida x Energia esperada (device_id {})'.format(d_id), size=14)
    ax.legend( ('energia aferida', 'energia esperada'), loc=3)
    st.pyplot()


def plotTotalSumEnergy(dados, min_tempo, max_tempo):
    #lista com todas as datas diferentes 
    #dados['date_time'].describe()
    lista_datas_distintas = list(pd.to_datetime(dados['date_time'].unique()))

    # gerando lista com as somas de cada id com base na data
    lista_act = []
    lista_exp = []

    for i in lista_datas_distintas:
        act = round(dados[dados['date_time'] == i]['act_pow'].sum(),2)
        exp = round(dados[dados['date_time'] == i]['exp_pow'].sum(),2)

        lista_act.append(act)
        lista_exp.append(exp)


    #defindo a base_total 
    base_total = pd.DataFrame(lista_datas_distintas, columns = ['date_time'])
    base_total['act_pow'] = lista_act
    base_total['exp_pow'] = lista_exp


    # indexando date_time

    base_total = base_total.set_index('date_time')

    # Grafico com a soma do act_pow e exp_pow para cada data do csv
    ax = base_total[['act_pow', 'exp_pow']].loc[min_tempo : max_tempo].plot(marker='.')
    ax.xaxis.set_major_locator(mdates.HourLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m-%H:%M'))
    plt.ylim(0, 5000)
    plt.xlabel('')
    plt.title('Energia aferida x Energia esperada (Total)', size=14)
    ax.legend(('energia aferida', 'energia esperada'), loc=3)
    st.pyplot()
    

def main():
    st.title('Gerador de Gráficos')
    st.markdown('O gerador de graficos automatico é uma aplicação refente a um teste, no qual dado uma tabela com os dados referentes a geração de energia de algumas turbinas, um gráfico será plotado para acompanhamento/analises do desenvolvimento das turbinas.')
    st.markdown('Essa aplicação recebe uma tabela com os campos id, device_id, sample_time, wind_speed, act_pow e exp_pow no formato csv .')
    st.markdown('Tal aplicação esta dividida em duas partes, no qual a primeira o usuario deve especificar qual a coluna que deseja analisar para que o gráfico com eixo X equivalente ao sample_time e o eixo Y equivalente a variavel fornecida seja plotado. A segunda parte gera automaticamente um grafico para cada ID  de turbina presente na tabela fornecida referente a energia aferida e a energia esperada, alem de um grafico com a soma de todos os IDs da energia aferida e da energia esperada.')

    #dropdown
    option = st.selectbox(
    'Qual a base (csv) você deseja utilizar?',
    ('Usar o CSV de teste', 'Usar outro CSV'))

    if option == 'Usar o CSV de teste':
        file = 'dados.csv'
    elif option == 'Usar outro CSV':
        #st.markdown('Faça o upload da base:')
        file = st.file_uploader('', type = 'csv')
    else:
        st.write('Selecione uma opção')

    
    if file is not None:
        st.subheader('Analisando os dados')
        dados = pd.read_csv(file)

        st.markdown('Número de linhas: ' + str(dados.shape[0]))

        st.markdown('Número de colunas:' + str(dados.shape[1]))

        if dados.shape[1] != 6:
            st.markdown('A base possui mais de 5 colunas, possivel base fora do formato')
        else:
            st.markdown('Primeiras linhas da base:')
            st.dataframe(dados.head(3))

            st.markdown('Algumas informações importantes sobre a base:')
            st.dataframe(dados.info())

            st.markdown('Alterando o tipo de dados da coluna sample_time de object paara datetime:')
            st.subheader('Nessa caso foi criado uma nova coluna (date_time)')
            dados['date_time'] = pd.to_datetime(dados['sampĺe_time'])
            st.markdown(dados.info())

            st.markdown('Gerando a base com as colunas principais:')
            base = pd.DataFrame(dados, columns=['device_id', 'date_time', 'wind_speed', 'act_pow', 'exp_pow'])
            st.dataframe(base.head(3))


            st.markdown('Indexando tabela com base no date_time:')
            base = base.set_index('date_time')
            st.dataframe(base.head(3))

            st.subheader('**Parte 1**')

            st.markdown('Com o arquivo dados.csv em mãos (vide anexo), desenvolva uma função em Python que receba os parâmetros:')
            st.markdown(' - device_id: o id do dispositivo;')
            st.markdown(' - variable: que representa qual variável da tabela que queremos analisar (wind_speed, act_pow ou exp_pow)')
            st.markdown(' - start_time: início do período de análise;')
            st.markdown(' - end_time: fim do período de análise;')

            id_input = st.text_input("Digite o id", '758')
            variable_input = st.text_input("Digite a varivel da tabela que deseja analisar", 'wind_speed')
            start_time_input = st.text_input("Digite o Início do período de análise (aaa-mm-dd hh:mm:ss)", '2020-07-27 01:50:00')
            end_time_input = st.text_input("Digite o Fim período de análise (aaa-mm-dd hh:mm:ss)", '2020-07-27 13:10:00')

            if st.button('Gerar Gráfico'):
                plotTimeseriesVariable(id_input, variable_input, start_time_input, end_time_input, base)

            st.subheader('**Parte 2**')

            st.markdown('Sabendo que a coluna **act_pow** representa a potência média da turbina aferida nos últimos 10 minutos e **exp_pow** representa a potência esperada dada a curva de potência, ambos em kW, plote um gráfico de sua escolha que exponha, de forma intuitiva, a diferença entre a **energia aferida e a energia esperada acumulada** para o período presente em dados.csv.')

            st.markdown('Nesse caso será plotado um grafico para cada id e um com a soma total do act_pow e exp_pow doS ids para cada data do csv')

            st.markdown('**Setando a menor e a maior data da base**')

            min_tempo = pd.to_datetime(dados['date_time'].min())
            st.markdown('Menor data:' + str(min_tempo))
            max_tempo = pd.to_datetime(dados['date_time'].max())
            st.markdown('Maior data:' + str(min_tempo))

            st.markdown('Verificando qtd de IDs diferentes')
            lista_de_ids = list(base['device_id'].unique())
            st.markdown('Existe um total de **' + str(len(lista_de_ids)) + '** id(s) diferentes na base')
            st.markdown('Lista com os IDs:')
            st.markdown(lista_de_ids)

            st.markdown('Plotando grafico para cada ID')

            #if st.button('Gerar Gráficos'):
            for i in lista_de_ids:
                plotDiffEnergy(i, min_tempo, max_tempo, base)


            st.markdown('Plotando gráfico  com a soma total dos IDs')

            #if st.button('Gerar Gráfico'):
            plotTotalSumEnergy(dados, min_tempo, max_tempo)
        


if __name__ == '__main__':
    main()