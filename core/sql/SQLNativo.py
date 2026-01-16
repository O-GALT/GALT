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
                )

                SELECT
                    predio_id,
                    predio,
                    total_setores,
                    total_salas,
                    total_equipamentos
                FROM locais_predios,
                     setores,
                     salas,
                     equipamentos;
                """,
                [predio_id, predio_id, predio_id],
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
