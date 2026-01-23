from django.db import connection


class SQLNativo:

    @staticmethod
    def carregar_nome_salas_equipamentos_setores_predio(predio_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                WITH

                setores AS (
                    SELECT
                        COUNT(s.setor_id) AS total_setores
                    FROM locais_setores s
                    INNER JOIN locais_predios p USING (predio_id)
                    WHERE p.predio_id = %s
                ),

                salas AS (
                    SELECT
                        COUNT(s.sala_id) AS total_salas
                    FROM locais_salas s
                    INNER JOIN locais_setores se USING (setor_id)
                    INNER JOIN locais_predios p USING (predio_id)
                    WHERE p.predio_id = %s
                ),

                equipamentos AS (
                    SELECT
                        COUNT(e.equipamento_id) AS total_equipamentos
                    FROM ativos_equipamentos e
                    INNER JOIN locais_salas s USING (sala_id)
                    INNER JOIN locais_setores se USING (setor_id)
                    INNER JOIN locais_predios p USING (predio_id)
                    WHERE p.predio_id = %s
                ),

                predios AS (
                    SELECT
                        predio_id, predio
                    FROM locais_predios WHERE predio_id = %s
                )
                    
                SELECT
                    predio_id,
                    predio,
                    total_setores,
                    total_salas,
                    total_equipamentos
                FROM predios,
                     setores,
                     salas,
                     equipamentos;
                """,
                [predio_id, predio_id, predio_id, predio_id],
            )

            colunas = [col[0] for col in cursor.description]
            resultados = [
                dict(zip(colunas, row))
                for row in cursor.fetchall()
            ]

        return resultados

    @staticmethod
    def carregar_indicadores_predio(predio_id):
        """
        Retorna os dados consolidados para os cards e gráficos do dashboard do prédio.

        Inclui:
        - Quantidade total de setores
        - Quantidade total de equipamentos
        - Quantidade total de salas
        - Total de reportes abertos
        - Manutenções agendadas para hoje
        - Manutenções pendentes
        - Saúde geral do prédio (baseada no estado dos equipamentos)
        - Estado das salas (liberadas, em manutenção, inaptas)
        - Estado dos equipamentos (funcionando, manutenção, defeituosos)

        Fonte: SQL nativo com CTEs para agregação de dados por prédio.
        """

        with connection.cursor() as cursor:
            cursor.execute(
                """
                WITH

                reportes AS (
                    SELECT
                        COUNT(*) AS reportes_abertos
                    FROM suporte_reportes r
                    INNER JOIN ativos_equipamentos e USING (equipamento_id)
                    INNER JOIN locais_salas s USING (sala_id)
                    INNER JOIN locais_setores se USING (setor_id)
                    INNER JOIN locais_predios p USING (predio_id)
                    WHERE p.predio_id = %s
                ),

                predios AS (
                    SELECT
                        predio_id,
                        predio
                        FROM locais_predios p
                    WHERE p.predio_id = %s
                ),
                    
                salas AS (
                    SELECT
                        COUNT(*) FILTER (WHERE s.estado_atual = 'LIBERADA')   AS salas_liberada,
                        COUNT(*) FILTER (WHERE s.estado_atual = 'MANUTENCAO') AS salas_manutencao,
                        COUNT(*) FILTER (WHERE s.estado_atual = 'INAPTA')     AS salas_inapta
                    FROM locais_salas s
                    INNER JOIN locais_setores se USING (setor_id)
                    INNER JOIN locais_predios p USING (predio_id)
                    WHERE p.predio_id = %s
                ),

                equipamentos AS (
                    SELECT
                        COUNT(*) FILTER (WHERE e.estado_atual = 'FUNCIONANDO') AS equipamentos_funcionando,
                        COUNT(*) FILTER (WHERE e.estado_atual = 'MANUTENCAO')   AS equipamentos_manutencao,
                        COUNT(*) FILTER (WHERE e.estado_atual = 'DEFEITUOSO')   AS equipamentos_defeituoso,
                        COUNT(*)                                              AS total_equipamentos
                    FROM ativos_equipamentos e
                    INNER JOIN locais_salas s USING (sala_id)
                    INNER JOIN locais_setores se USING (setor_id)
                    INNER JOIN locais_predios p USING (predio_id)
                    WHERE p.predio_id = %s
                ),

                setores AS (
                    SELECT
                        COUNT(*) AS total_setores
                    FROM locais_setores s
                    INNER JOIN locais_predios p USING (predio_id)
                    WHERE p.predio_id = %s
                ),

                manutencoes AS (
                    SELECT
                        COUNT(*) FILTER (WHERE a.data = CURRENT_DATE)
                            AS manutencoes_hoje,
                        COUNT(*) FILTER (WHERE a.estado_atual = 'ESPERANDO_CONFIRMACAO')
                            AS manutencoes_pendentes
                    FROM agendas_agendamentos a
                    INNER JOIN locais_salas s USING (sala_id)
                    INNER JOIN locais_setores se USING (setor_id)
                    INNER JOIN locais_predios p USING (predio_id)
                    WHERE p.predio_id = %s
                )
    
                SELECT
                    predio_id,
                    predio,
                    reportes_abertos,
                    manutencoes_hoje,
                    total_setores,
                    (
                        salas_liberada +
                        salas_manutencao +
                        salas_inapta
                    ) AS total_salas,
                    total_equipamentos,
                    manutencoes_pendentes,
                    CASE
                        WHEN total_equipamentos = 0 THEN 100
                        ELSE ROUND(
                            (
                                (equipamentos_funcionando * 1.0) +
                                (equipamentos_manutencao * 0.5)
                            ) / total_equipamentos * 100.0,
                            0
                        )
                    END AS saude_predio,
                    salas_liberada,
                    salas_manutencao,
                    salas_inapta,
                    equipamentos_funcionando,
                    equipamentos_manutencao,
                    equipamentos_defeituoso
                FROM predios 
                    INNER JOIN salas ON TRUE
                    INNER JOIN manutencoes ON TRUE
                    INNER JOIN reportes ON TRUE
                    INNER JOIN equipamentos ON TRUE
                    INNER JOIN setores ON TRUE
                """,
                [predio_id, predio_id, predio_id, predio_id, predio_id, predio_id],
            )

            colunas = [col[0] for col in cursor.description]
            resultados = [
                dict(zip(colunas, row))
                for row in cursor.fetchall()
            ]

        return resultados

    @staticmethod
    def listar_equipamentos_mais_defeituosos_predio(predio_id):
        with connection.cursor() as cursor:
            cursor.execute('''
                        WITH manutencoes_por_mes AS (
            
                SELECT
                    e.equipamento_id,
                    EXTRACT(MONTH FROM a.data) AS mes,
                    COUNT(*) AS manutencoes_no_mes
            
                FROM ativos_historicomanutencoes a
                INNER JOIN ativos_equipamentos e USING (equipamento_id)
                INNER JOIN locais_salas s USING (sala_id)
                INNER JOIN locais_setores se USING (setor_id)
                INNER JOIN locais_predios p USING (predio_id)
            
                WHERE p.predio_id = %s
                GROUP BY e.equipamento_id, mes
            )
            
            SELECT
                e.equipamento_id,
                e.serial,
            
                SUM(mpm.manutencoes_no_mes) AS manutencoes,
            
                ROUND((AVG(mpm.manutencoes_no_mes) * 100) / 5, 0) AS necessidade_substituicao
            
            FROM manutencoes_por_mes mpm
            INNER JOIN ativos_equipamentos e USING (equipamento_id)
            
            GROUP BY e.equipamento_id, e.serial
            ORDER BY manutencoes DESC;
            ''', [predio_id])

            colunas = [col[0] for col in cursor.description]
            resultados = [
                dict(zip(colunas, row))
                for row in cursor.fetchall()
            ]

        return resultados


    @staticmethod
    def carregar_indicadores_equipamento(equipamento_id):
        with connection.cursor() as cursor:
            cursor.execute('''
                        WITH 
            
            equipamento AS (
                SELECT
                
                e.serial, e.estado_atual, e.tipo, s.localizacao AS sala, s.sala_id, e.fabricante, e.data_aquisicao,
                (
                    SELECT h.data FROM ativos_historicomanutencoes h
                    WHERE h.equipamento_id = e.equipamento_id
                    ORDER BY h.data DESC
                    LIMIT 1
                ) AS data_ultima_manutencao
                
                FROM ativos_equipamentos e 
                INNER JOIN locais_salas s USING(sala_id)
                WHERE e.equipamento_id = %s
            
            ),
            
            manutencoes_preventivas AS (
                SELECT
                
                COUNT(*) AS manutencoes_preventivas
                
                FROM agendas_agendamentos a
                INNER JOIN locais_salas s USING(sala_id)
                INNER JOIN ativos_equipamentos e USING(sala_id)
                WHERE a.estado_atual = 'A_SER_REALIZADO'
                AND e.equipamento_id = %s
            
            ),
            reportes_abertos AS (
                SELECT
                
                COUNT(*) AS reportes_abertos
                
                FROM suporte_reportes r
                INNER JOIN ativos_equipamentos e USING(equipamento_id)
                WHERE e.equipamento_id = %s
                AND r.estado_atual = 'ABERTO'
            
            ),
            
            ultima_manutencao AS (
                    SELECT 
                    
                    CURRENT_DATE - (
                        SELECT data FROM ativos_historicomanutencoes
                        WHERE equipamento_id = e.equipamento_id
                        ORDER BY data DESC
                        LIMIT 1
                    ) AS ultima_manutencao
                
                FROM ativos_historicomanutencoes a
                INNER JOIN ativos_equipamentos e USING(equipamento_id)
                WHERE e.equipamento_id = %s
                GROUP BY e.equipamento_id
            ),
            
            falhas_no_mes AS (
                SELECT 
                
                EXTRACT('month' FROM a.data) AS mes,
                COUNT(*) AS manutencoes_no_mes
                
                FROM ativos_historicomanutencoes a
                INNER JOIN ativos_equipamentos e USING(equipamento_id)
                WHERE e.equipamento_id = %s
                GROUP BY mes
                
            ),
            
            dias_entre_falhas AS (
                SELECT
                
                a.data - LAG(a.data) OVER (ORDER BY a.data) AS dias_entre_falhas
                
                FROM ativos_historicomanutencoes a
                INNER JOIN ativos_equipamentos e USING(equipamento_id)
                WHERE e.equipamento_id = %s
            ),
            
            
            indicadores_manutencoes AS (
                SELECT 
                
                COUNT(a.historico_manutencoes_id) 
                FILTER (WHERE a.data >= DATE_TRUNC('month', CURRENT_DATE) AND a.data < CURRENT_DATE + INTERVAL '1 month') AS
                manutencoes_nesse_mes,
                
                COUNT(a.historico_manutencoes_id) AS manutencoes_realizadas
                
                
                FROM ativos_historicomanutencoes a
                INNER JOIN ativos_equipamentos e USING(equipamento_id)
                WHERE e.equipamento_id = %s
            )
            
            
            SELECT 
            
            e.serial,
            e.estado_atual,
            e.sala_id,
            COALESCE(im.manutencoes_realizadas, 0) AS manutencoes_realizadas,
            COALESCE(re.reportes_abertos, 0) AS reportes_abertos,
            e.tipo,
            e.sala,
            e.fabricante,
            e.data_aquisicao,
            COALESCE(mp.manutencoes_preventivas, 0) AS manutencoes_preventivas, 
            COALESCE(e.data_ultima_manutencao, NULL) AS data_ultima_manutencao,
            COALESCE(ul.ultima_manutencao, NULL) AS ultima_manutencao,
            COALESCE(im.manutencoes_nesse_mes,0) AS manutencoes_nesse_mes,
            
            CASE 
                WHEN COALESCE(AVG(fa.manutencoes_no_mes), 0) = 0 THEN 0
                ELSE
                    ROUND((AVG(fa.manutencoes_no_mes) * 100)/5, 0)
            END AS recomendacao_substituicao,
                
            CASE 
                WHEN COALESCE(AVG(df.dias_entre_falhas), 0) = 0 THEN 0
                ELSE                    
                    ROUND(AVG(df.dias_entre_falhas), 0)
            END AS tempo_medio_entre_falhas,
            
            CASE 
                WHEN COALESCE(AVG(fa.manutencoes_no_mes), 0) = 0 THEN 'sem medida'
                WHEN (AVG(fa.manutencoes_no_mes) * 100)/5 >= 10 AND AVG(fa.manutencoes_no_mes * 100)/5 <= 29 THEN 'baixo'
                WHEN (AVG(fa.manutencoes_no_mes) * 100)/5 >= 30 AND AVG(fa.manutencoes_no_mes * 100)/5 <= 55 THEN 'mediano'
                WHEN (AVG(fa.manutencoes_no_mes) * 100)/5 >= 56 AND AVG(fa.manutencoes_no_mes * 100)/5 <= 100 THEN 'alto'
                
            END AS tedencias_a_falhas	
            
            FROM equipamento e
                LEFT JOIN indicadores_manutencoes im ON true
                LEFT JOIN ultima_manutencao ul ON true
                LEFT JOIN dias_entre_falhas df ON true
                LEFT JOIN falhas_no_mes fa ON true
                LEFT JOIN reportes_abertos re ON true
                LEFT JOIN manutencoes_preventivas mp ON true
            
            GROUP BY ultima_manutencao, manutencoes_nesse_mes, serial, estado_atual, manutencoes_realizadas, reportes_abertos, tipo, sala, fabricante, data_ultima_manutencao, data_aquisicao, manutencoes_preventivas, sala_id;
            ''', [equipamento_id, equipamento_id, equipamento_id, equipamento_id, equipamento_id, equipamento_id, equipamento_id])

            colunas = [col[0] for col in cursor.description]
            resultados = [
                dict(zip(colunas, row))
                for row in cursor.fetchall()
            ]

        return resultados


    @staticmethod
    def carregar_indicadores_sala(sala_id):
        with connection.cursor() as cursor:
            cursor.execute('''
            SELECT 
                s.localizacao,
                s.estado_atual,
                COALESCE((
                    SELECT u.email_escolar FROM contas_usuarios u
                    
                    
                    INNER JOIN contas_tecnicosti t ON t.usuario_id = u.id
                    INNER JOIN agendas_tecnicostiagendamentos at ON at.tecnico_id = t.usuario_id
                    INNER JOIN agendas_agendamentos a USING(agendamento_id)
                    INNER JOIN locais_salas s USING(sala_id)
                    WHERE s.sala_id = %s
                    ORDER BY a.data DESC
                    LIMIT 1
                ), 'Sem agendamentos cadastrados') AS responsavel_manutencao,
                
                COUNT(*) FILTER (WHERE e.tipo = 'COMPUTADOR') AS computadores,
                COUNT(*) FILTER (WHERE e.tipo = 'PROJETOR') AS projetores,
                COUNT(*) FILTER (WHERE e.tipo = 'AR_CONDICIONADO') AS ar_condicionados
                
                
                FROM locais_salas s
                LEFT JOIN ativos_equipamentos e USING(sala_id)
                
                WHERE s.sala_id = %s
                GROUP BY s.localizacao, s.estado_atual;
            ''', [sala_id, sala_id])

            colunas = [col[0] for col in cursor.description]
            resultados = [
                dict(zip(colunas, row))
                for row in cursor.fetchall()
            ]

        return resultados


    @staticmethod
    def carregar_indicadores_setor(setor_id):
        with connection.cursor() as cursor:
            cursor.execute('''
                                WITH
                    
                    setores AS (
                        SELECT s.setor FROM locais_setores s
                        WHERE s.setor_id = %s
                    ),
                    
                    manutencoes AS (
                        SELECT
                    
                        COUNT(*) FILTER(WHERE a.data = CURRENT_DATE) AS manutencoes_hoje,
                        COUNT(*) AS manutencoes_agendadas,
                    
                        COUNT(*) FILTER (
                            WHERE a.data >= DATE_TRUNC('month', CURRENT_DATE) 
                            AND a.data < DATE_TRUNC('month', CURRENT_DATE + INTERVAL '1 month')
                            AND a.estado_atual = 'FEITO'
                        ) AS manutencoes_mes_atual,
                        COUNT(*) FILTER (
                            WHERE a.data >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
                            AND a.data < DATE_TRUNC('month', CURRENT_DATE)
                            AND a.estado_atual = 'FEITO'
                        ) AS manutencoes_mes_passado
                    
                        FROM agendas_agendamentos a
                        INNER JOIN locais_salas s USING(sala_id)
                        INNER JOIN locais_setores se USING(setor_id)
                        WHERE se.setor_id = %s
                    ),
                    
                    equipamentos AS (
                        SELECT
                    
                        COUNT(*) FILTER (WHERE e.estado_atual = 'FUNCIONANDO') AS equipamentos_funcionando,
                        COUNT(*) FILTER (WHERE e.estado_atual = 'MANUTENCAO') AS equipamentos_manutencao,
                        COUNT(*) FILTER (WHERE e.estado_atual = 'DEFEITUOSO') AS equipamentos_defeituosos,
                        COUNT(*) AS equipamentos_total
                    
                        FROM ativos_equipamentos e
                        INNER JOIN locais_salas s USING(sala_id)
                        INNER JOIN locais_setores se USING(setor_id)
                        WHERE se.setor_id = %s
                    ),
                    
                    salas AS (
                        SELECT
                        COUNT(*) FILTER (WHERE s.estado_atual = 'LIBERADA') AS salas_funcionando,
                        COUNT(*) FILTER (WHERE s.estado_atual = 'MANUTENCAO') AS salas_manutencao,
                        COUNT(*) FILTER (WHERE s.estado_atual = 'INAPTA') AS salas_inaptas,
                        COUNT(*) AS salas_total
                    
                        FROM locais_salas s
                        INNER JOIN locais_setores se USING(setor_id)
                        WHERE se.setor_id = %s
                    ),
                    
                    reportes AS (
                        SELECT COUNT(*) AS reportes_total
                        FROM suporte_reportes r
                        INNER JOIN ativos_equipamentos e USING(equipamento_id)
                        INNER JOIN locais_salas s USING(sala_id)
                        INNER JOIN locais_setores se USING(setor_id)
                        WHERE se.setor_id = %s
                    )
                    
                    SELECT 
                        s.setor,
                        manutencoes.manutencoes_hoje,
                        manutencoes.manutencoes_agendadas,
                        reportes.reportes_total,
                    
                        CASE 
                            WHEN equipamentos.equipamentos_total = 0 THEN 100
                            ELSE ROUND(((equipamentos.equipamentos_funcionando * 1.0) + (equipamentos.equipamentos_manutencao * 0.5)) / equipamentos.equipamentos_total * 100.0, 0)
                        END AS nivel_de_saude_setor,
                    
                    
                        CASE
                    
                        WHEN manutencoes.manutencoes_mes_passado = 0 THEN 100
                    
                        ELSE ROUND((manutencoes.manutencoes_mes_atual - manutencoes.manutencoes_mes_passado) / manutencoes.manutencoes_mes_passado * 100.0, 0)
                        END AS produtividade_setor,
                    
                        equipamentos.equipamentos_funcionando,
                        equipamentos.equipamentos_manutencao,
                        equipamentos.equipamentos_defeituosos,
                        equipamentos.equipamentos_total,
                        
                        salas.salas_funcionando,
                        salas.salas_manutencao,
                        salas.salas_inaptas,
                        salas.salas_total
                    
                        FROM setores s
                        INNER JOIN manutencoes ON TRUE
                        INNER JOIN equipamentos ON TRUE 
                        INNER JOIN salas ON TRUE
                        INNER JOIN reportes ON TRUE;
            ''', [setor_id, setor_id, setor_id, setor_id, setor_id])

            colunas = [col[0] for col in cursor.description]
            resultados = [
                dict(zip(colunas, row))
                for row in cursor.fetchall()
            ]
        return resultados