import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from core.essenciais import TipoEquipamento


class GeradorGraficos:

    @staticmethod
    def gerar_grafico_estado_equipamentos(quantidade_funcionando, quantidade_manutencao, quantidade_defeituoso):
        # 1) dados
        df = pd.DataFrame({
            "Estado": ["Funcionando", "Defeituoso", "Em manutenção"],
            "Quantidade": [quantidade_funcionando, quantidade_defeituoso, quantidade_manutencao],
        })

        # 2) mapa de cores
        cores = {
            "Funcionando": "#2FCF6A",
            "Defeituoso": "#F76A6D",
            "Em manutenção": "#FFEB5A"
        }

        # 3) figura (pie/donut)
        fig = px.pie(
            df,
            values="Quantidade",
            hole=0.40,
            color="Estado",
            color_discrete_map=cores
        )

        # 4) traces (mantendo borda branca, hover e sem texto interno)
        fig.update_traces(
            textinfo="none",
            hovertemplate="%{customdata[0]}: %{percent:.1%} (%{value})<extra></extra>",
            marker=dict(line=dict(color="rgba(248, 249, 250, 1)", width=6)),
            sort=False,
            customdata=df[["Estado"]]
        )

        # 5) layout base (título, margens aumentadas na parte inferior para a legenda)
        fig.update_layout(
            title=dict(
                text="Estado dos Equipamentos",
                x=0.03,
                y=0.92,
                xanchor="left",
                font=dict(size=15, family="Open Sans", color="#365C3B", weight='bold'),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            autosize=True,
            margin=dict(t=50, b=60, l=0, r=0),  # margens menores e razoáveis
            showlegend=False
        )

        # 6) posicionar o donut mais centralizado (deixando espaço suficiente lateralmente)
        # ajustar [x0, x1] e [y0, y1] se quiser mudar proporção

        # 7) gerar anotações (legendas) **embaixo** do gráfico (centralizadas)
        total = df["Quantidade"].sum()
        annotations = []  # lista que vamos passar para fig.update_layout(annotations=...)

        # coordenadas em paper (0..1)
        # centro X onde a legenda será centralizada
        x_center = 0.5
        # deslocamentos para a coluna da label (esq) e da value (dir)
        x_label = 0.0   # ajuste para espaçar label à esquerda do centro
        x_value = 1   # ajuste para posicionar value à direita do centro
        # posição Y inicial (embaixo do domain do donut) e espaçamento vertical entre linhas
        y_start = 0.1   # primeira linha (mais em cima)
        y_step = 0.15   # distância entre linhas

        for i, row in df.iterrows():
            estado = row["Estado"]
            qtd = int(row["Quantidade"])
            percent = qtd / total * 100
            y_pos = y_start - i * y_step - 0.34

            # anotação esquerda: bolinha colorida + texto do estado
            annotations.append(dict(
                x=0.5,
                y=y_pos,
                xref="paper",
                yref="paper",
                text=(
                    f"<span style='color:{cores[estado]};'>&#9679;</span>"
                    f"&nbsp;<span style='color:#111;font-weight:400'>{estado}</span>"
                    f"&nbsp;<span style='color:#111;font-weight:400'>— {qtd}</span>"
                ),
                font=dict(family="Open Sans", size=11, color="#333"),
                showarrow=False,
                align="center",
                xanchor="center",
                yanchor="bottom"
            ))

        # combina com eventuais anotações existentes (preserva se houver)
        fig.update_layout(annotations=annotations)

        # 8) gerar HTML e retornar
        html_out = fig.to_html(full_html=False, config={'responsive': True})
        return html_out


    @staticmethod
    def gerar_grafico_estado_salas(quantidade_liberada, quantidade_manutencao, quantidade_inapta):
        # 1) dados
        df = pd.DataFrame({
            "Estado": ["Liberada", "Inapta", "Em manutenção"],
            "Quantidade": [quantidade_liberada, quantidade_inapta, quantidade_manutencao],
        })

        # 2) mapa de cores
        cores = {
            "Liberada": "#2FCF6A",
            "Inapta": "#F76A6D",
            "Em manutenção": "#FFEB5A"
        }

        # 3) figura (pie/donut)
        fig = px.pie(
            df,
            values="Quantidade",
            hole=0.40,
            color="Estado",
            color_discrete_map=cores
        )

        # 4) traces (mantendo borda branca, hover e sem texto interno)
        fig.update_traces(
            textinfo="none",
            hovertemplate="%{customdata[0]}: %{percent:.1%} (%{value})<extra></extra>",
            marker=dict(line=dict(color="rgba(248, 249, 250, 1)", width=6)),
            sort=False,
            customdata=df[["Estado"]]
        )

        # 5) layout base (título, margens aumentadas na parte inferior para a legenda)
        fig.update_layout(
            title=dict(
                text="Estado das Salas",
                x=0.03,
                y=0.92,
                xanchor="left",
                font=dict(size=15, family="Open Sans", color="#365C3B", weight="bold"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            autosize=True,
            margin=dict(t=50, b=60, l=0, r=0),  # margens menores e razoáveis
            showlegend=False
        )

        # 6) posicionar o donut mais centralizado (deixando espaço suficiente lateralmente)
        # ajustar [x0, x1] e [y0, y1] se quiser mudar proporção

        # 7) gerar anotações (legendas) **embaixo** do gráfico (centralizadas)
        total = df["Quantidade"].sum()
        annotations = []  # lista que vamos passar para fig.update_layout(annotations=...)

        # coordenadas em paper (0..1)
        # centro X onde a legenda será centralizada
        x_center = 0.5
        # deslocamentos para a coluna da label (esq) e da value (dir)
        x_label = 0.0  # ajuste para espaçar label à esquerda do centro
        x_value = 1  # ajuste para posicionar value à direita do centro
        # posição Y inicial (embaixo do domain do donut) e espaçamento vertical entre linhas
        y_start = 0.1  # primeira linha (mais em cima)
        y_step = 0.15  # distância entre linhas

        for i, row in df.iterrows():
            estado = row["Estado"]
            qtd = int(row["Quantidade"])
            percent = qtd / total * 100
            y_pos = y_start - i * y_step - 0.34

            # anotação esquerda: bolinha colorida + texto do estado
            annotations.append(dict(
                x=0.5,
                y=y_pos,
                xref="paper",
                yref="paper",
                text=(
                    f"<span style='color:{cores[estado]};'>&#9679;</span>"
                    f"&nbsp;<span style='color:#111;font-weight:400'>{estado}</span>"
                    f"&nbsp;<span style='color:#111;font-weight:400'>— {qtd}</span>"
                ),
                font=dict(family="Open Sans", size=11, color="#333"),
                showarrow=False,
                align="center",
                xanchor="center",
                yanchor="bottom"
            ))

        # combina com eventuais anotações existentes (preserva se houver)
        fig.update_layout(annotations=annotations)

        # 8) gerar HTML e retornar
        html_out = fig.to_html(full_html=False, config={'responsive': True})
        return html_out

    @staticmethod
    def gerar_grafico_saude_local(local, porcentagem):
        # construímos um pie com três fatias:
        # 1) arco preenchido (v)
        # 2) arco restante (100-v)
        # 3) metade invisível (100) -> cria o efeito semicirculo
        values = [porcentagem, 100-porcentagem, 100]
        # cores: arco preenchido, arco restante (desbotado), metade invisível (background)
        colors = ["#2FCF6A", "rgba(254, 231, 190, 1)", "rgba(0,0,0,0)"]

        fig = go.Figure()

        fig.add_trace(go.Pie(
            values=values,
            marker_colors=colors,
            labels= ['Saudavel', 'Restante', ''],
            hole=0.7,  # control the thickness of the arc
            sort=False,
            rotation=270,  # rotate so the visible arc sits on top (half circle)
            direction='clockwise',
            showlegend=False,
            textinfo='none',
            hovertemplate='%{label}<br><b>%{value}%</b><extra></extra>'
        ))

        fig.data[0].domain = {'x': [0.0, 1.0], 'y': [0.0, 1.0]}

        # central number as annotation
        fig.update_layout(
            title=dict(
                x=0.5,
                y=0.923,
                text='Nível de saúde do ' + local,
                font=dict(family="Open Sans", size=15, color="#365C3B", weight="bold"),
            ),
            annotations=[dict(
                text=f"<span style='font-size:20px; font-weight:700; color:#111'>{porcentagem}%</span>",
                x=0.5, y=0.6,
                showarrow=False,
                xanchor='center',
                yanchor='middle',
                xref='paper', yref='paper'

            )],
            margin=dict(t=60, b=40, l=0, r=0),

            height=None,
            width=None,
            paper_bgcolor='rgba(0,0,0,0)'
        )

        # Make it responsive when embedded: let the container control the size via CSS
        return fig.to_html()

    @staticmethod
    def gerar_grafico_reports_por_tipo(equipamentos_reportes):
        valores_matriz = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]

        lista_dias_equipamentos = []

        if equipamentos_reportes:
            equipamento = 0
            controlador = 0
            while controlador < len(equipamentos_reportes):
                map_equipamento_reporte = equipamentos_reportes[controlador]

                if equipamento == 0 and map_equipamento_reporte['tipo_equipamento'] == TipoEquipamento.AR_CONDICIONADO:
                    valores_matriz[0][map_equipamento_reporte['dia']-1] = map_equipamento_reporte['reportes']
                    equipamento = 1
                else:
                    equipamento = 1

                if equipamento == 1 and map_equipamento_reporte['tipo_equipamento'] == TipoEquipamento.COMPUTADOR:
                    valores_matriz[1][map_equipamento_reporte['dia']-1] = map_equipamento_reporte['reportes']
                    equipamento = 2
                else:
                    equipamento = 2


                if equipamento == 2 and map_equipamento_reporte['tipo_equipamento'] == TipoEquipamento.PROJETOR:
                    valores_matriz[2][map_equipamento_reporte['dia']-1] = map_equipamento_reporte['reportes']

                controlador = controlador + 1
                equipamento = 0

        for dia in range(7):  # colunas

            for equipamento in range(3):  # linhas
                lista_dias_equipamentos.append(
                    valores_matriz[equipamento][dia]
                )

        # Exemplo de dados (substitua pelos teus valores reais)
        df = pd.DataFrame({
            "dia": ["Segunda", "Segunda", "Segunda",
                    "Terça", "Terça", "Terça",
                    "Quarta", "Quarta", "Quarta",
                    "Quinta", "Quinta", "Quinta",
                    "Sexta", "Sexta", "Sexta",
                    "Sábado", "Sábado", "Sábado",
                    "Domingo", "Domingo", "Domingo"],
            "tipo": ["Ar-condicionado", "Computador", "Projetores"] * 7,
            "valor": lista_dias_equipamentos
        })

        # Ordem dos dias (garante a sequência correta)
        dias_ordem = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

        # Cores (azul, verde, roxo semelhantes à imagem)
        cores = {
            "Computador": "#1f77b4",  # azul
            "Ar-condicionado": "#2fcf6a",  # verde
            "Projetores": "#8a5adf"  # roxo
        }

        fig = px.bar(
            df,
            x="dia",
            y="valor",
            color="tipo",
            color_discrete_map=cores,
            category_orders={"dia": dias_ordem, "tipo": ["Ar-condicionado", "Computador", "Projetores"]},
            barmode="group",
            labels={"dia": "", "valor": ""},  # remove labels desnecessários
            height=320
        )

        # Aparência e layout
        fig.update_layout(
            title=dict(
                text="Reports por tipo de equipamento",
                x=0.02,
                xanchor="left",
                font=dict(family="Open Sans", size=16, color="#365C3B", weight="bold"),
            ),
            legend=dict(
                orientation="h",
                y=-0.15,
                x=0.5,
                xanchor="center",
                font=dict(family="Open Sans", size=12),
                bgcolor="rgba(0,0,0,0)",
            ),
            autosize=True,
            margin=dict(t=60, b=30, l=0, r=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            bargap=0.25,  # espaço entre grupos
            bargroupgap=0.12,
            font=dict(family="Open Sans", color="#37474f"),
        )

        # Grid horizontal leve
        fig.update_yaxes(showgrid=True, gridcolor="rgba(155,155,155,0.12)", zeroline=False, tick0=0)
        fig.update_xaxes(tickangle=0)

        # Hover custom (opcional)
        fig.update_traces(
            hovertemplate="%{x}<br>%{legendgroup}: %{y}<extra></extra>"
        )

        # Retorna HTML pronto para injetar no template Django
        html = fig.to_html(full_html=False, config={'responsive': True})
        return html


    @staticmethod
    def gerar_grafico_indice_manutencoes():
        # Dados de exemplo — substitua pelos reais
        df = pd.DataFrame({
            "Mês": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dec"],
            "Índice": [8, 5, 30, 15, 12, 14, 18, 5, 10, 12, 25, 15]
        })

        fig = px.line(
            df,
            x="Mês",
            y="Índice",
            line_shape="spline",  # curva suave
        )

        # Personalização visual
        fig.update_traces(
            line=dict(color="#3B5B76", width=2.5),
            hovertemplate="%{x}<br>Índice: %{y}<extra></extra>",
            mode="lines"
        )

        fig.update_layout(
            title=dict(
                text="Índice de manutenção dos equipamentos do prédio",
                x=0.02,
                y=0.93,
                xanchor="left",
                font=dict(family="Open Sans", size=15, color="#365C3B", weight="bold"),
            ),
            margin=dict(t=50, b=40, l=30, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            autosize=True,
            font=dict(family="Open Sans", size=12, color="#333"),
        )

        # Eixo X
        fig.update_xaxes(
            showgrid=False,
            tickmode="array",
            tickvals=df["Mês"],
            tickfont=dict(size=11, color="#7a7a7a")
        )

        # Eixo Y
        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.08)",
            zeroline=False,
            ticksuffix="",
            tickfont=dict(size=11, color="#7a7a7a")
        )

        # Exporta HTML responsivo
        html = fig.to_html(full_html=False, config={'responsive': True})
        return html
