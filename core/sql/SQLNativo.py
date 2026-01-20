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
                FROM salas,
                     manutencoes,
                     reportes,
                     equipamentos,
                     setores,
                     predios;
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
                
                e.serial, e.estado_atual, e.tipo, s.localizacao AS sala, e.fabricante, e.data_aquisicao,
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
            
            serial,
            estado_atual,
            manutencoes_realizadas,
            reportes_abertos,
            tipo,
            sala,
            fabricante,
            data_aquisicao,
            manutencoes_preventivas,
            data_ultima_manutencao,
            ultima_manutencao,
            manutencoes_nesse_mes,
            
            ROUND((AVG(manutencoes_no_mes) * 100)/5, 0) AS recomendacao_substituicao,
            
            ROUND(AVG(dias_entre_falhas), 0) AS tempo_medio_entre_falhas,
            
            CASE 
                WHEN (AVG(manutencoes_no_mes) * 100)/5 >= 10 AND AVG(manutencoes_no_mes * 100)/5 <= 29 THEN 'baixo'
                WHEN (AVG(manutencoes_no_mes) * 100)/5 >= 30 AND AVG(manutencoes_no_mes * 100)/5 <= 55 THEN 'mediano'
                WHEN (AVG(manutencoes_no_mes) * 100)/5 >= 56 AND AVG(manutencoes_no_mes * 100)/5 <= 100 THEN 'alto'
                
            END AS tedencias_a_falhas	
            
            FROM indicadores_manutencoes, ultima_manutencao, dias_entre_falhas, falhas_no_mes, equipamento, reportes_abertos, manutencoes_preventivas
            
            GROUP BY ultima_manutencao, manutencoes_nesse_mes, serial, estado_atual, manutencoes_realizadas, reportes_abertos, tipo, sala, fabricante, data_ultima_manutencao, data_aquisicao, manutencoes_preventivas;
            ''', [equipamento_id, equipamento_id, equipamento_id, equipamento_id, equipamento_id, equipamento_id, equipamento_id])

            colunas = [col[0] for col in cursor.description]
            resultados = [
                dict(zip(colunas, row))
                for row in cursor.fetchall()
            ]

        return resultados

