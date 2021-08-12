from reportlab.pdfgen import canvas
import streamlit as st 
import numpy as np 
import os


def GeneratePDF(nome, mes_leitura, leitura, consumo, valor_metro, valor_pagar, mes_vencimento):
    try:
        pdf = canvas.Canvas('{}-{}.pdf'.format(nome, mes_leitura))
        pdf.setTitle(nome)
        pdf.setFont("Helvetica-Bold", 30)
        pdf.drawString(245,780, nome)
        
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(245,720, mes_leitura)
        
        pdf.drawString(245,680, 'Leitura:')
        pdf.drawString(245,650, leitura)
        
        pdf.drawString(245,600, 'Consumo:')
        pdf.drawString(245,570, str(consumo))
        
        pdf.drawString(245,520, 'Valor do metro:')
        pdf.drawString(245,490, 'R$ {}'.format(str(valor_metro)))
        
        pdf.drawString(245,440, 'Valor a ser pago:')
        pdf.drawString(245,410, 'R$ {}'.format(str(valor_pagar)))
        
        
        pdf.drawString(245,360, 'Vencimento:')
        pdf.drawString(245, 320, mes_vencimento)
        pdf.save()

    except Exception as e:
        print(e)


class App:


    def __init__(self):
        self.name = 'Conta Poço'
        self.description = 'Conta fácil o aplicativo mensal.'
        self.users = ['Alcides',  'Osmar']
        self.sidebar = st.sidebar
        self.logo = 'logo.png'

    def menu(self):
        self.sidebar.image(self.logo, width=128)
        self.sidebar.header(self.name)
        self.sidebar.write(self.description)
        


    def calculate(self):

        with st.form('form-energy'):
            
            valor_energia = self.sidebar.number_input('Digite o valor da conta de energia:')

            data_leitura = str(self.sidebar.date_input('Selecione a data de leitura:'))

            data_vencimento = str(self.sidebar.date_input('Selecione a data de vencimento:'))

            st.header('Leitura:')
            st.write('Preencha os campos abaixo:')

            mes_atual = []
            mes_anterior = []

            for i, user in enumerate(self.users):
                i += 1
                st.write(f'**{user}:**')
                anterior = int(st.number_input(f'{i} - Digite o consumo do mês anterior'))
                atual = int(st.number_input(f'{i} - Digite o consumo do mês atual'))

                mes_atual.append(atual)
                mes_anterior.append(anterior)


            mes_atual = np.array(mes_atual)
            mes_anterior = np.array(mes_anterior)

            button = st.form_submit_button(label='Calcular')

            if button:

                consumo = mes_atual - mes_anterior

                consumo_total = np.sum(consumo)

                metro_cubico = round(valor_energia/consumo_total, 2)
                
                st.write('**Consumo:**')
                
                st.write(consumo)
                st.write(f'Valor do metro: R${metro_cubico}')

                i = 0
                for usuario, c in zip(self.users, consumo):

                    pagar = round(c*metro_cubico, 2)

                    st.write(f'{usuario} consumiu **{c} m³** e pagará **R$ {pagar}**')
                    
                    #st.write(usuario, data_leitura, f'{mes_atual[i]}-{mes_anterior[i]}', c, metro_cubico, pagar, data_vencimento)
                    GeneratePDF(usuario, data_leitura, f'{mes_atual[i]}-{mes_anterior[i]}', c, metro_cubico, pagar, data_vencimento)
                   
                    i += 1

                    st.info(f'{usuario}.pdf salvo com sucesso!')



    def run(self):
        self.menu()
        self.calculate()



if __name__ == '__main__':

    app = App()
    app.run()