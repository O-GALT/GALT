from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('suporte', '0001_initial'),
        ('ativos', '0001_initial'),
        ('locais', '0001_initial'),
        ('agendas', '0001_initial'),
        ('contas', '0001_initial'),
        ('auditoria', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            /* ==========================================================
               PREDIO
            ========================================================== */
            INSERT INTO locais_predios (predio)
            VALUES ('Predio Principal');


            /* ==========================================================
               SETORES
            ========================================================== */
            INSERT INTO locais_setores (setor, localizacao, predio_id)
            SELECT 'SETOR_ADMINISTRATIVO', 'BLOCO_A', predio_id
            FROM locais_predios WHERE predio = 'Predio Principal';

            INSERT INTO locais_setores (setor, localizacao, predio_id)
            SELECT 'SETOR_LABORATORIOS', 'BLOCO_B', predio_id
            FROM locais_predios WHERE predio = 'Predio Principal';


            /* ==========================================================
               SALAS
            ========================================================== */
            INSERT INTO locais_salas (estado_atual, localizacao, setor_id)
            SELECT 'LIBERADA', 'A101', setor_id
            FROM locais_setores WHERE setor = 'SETOR_ADMINISTRATIVO';

            INSERT INTO locais_salas (estado_atual, localizacao, setor_id)
            SELECT 'MANUTENCAO', 'B201', setor_id
            FROM locais_setores WHERE setor = 'SETOR_LABORATORIOS';
                
            INSERT INTO locais_salas (estado_atual, localizacao, setor_id)
            SELECT 'INAPTA', 'B34', setor_id
            FROM locais_setores WHERE setor = 'SETOR_LABORATORIOS';    
                
            INSERT INTO locais_salas (estado_atual, localizacao, setor_id)
            SELECT 'INAPTA', 'E34', setor_id
            FROM locais_setores WHERE setor = 'SETOR_LABORATORIOS';    


            /* ==========================================================
               EQUIPAMENTOS (~10)
            ========================================================== */
            /* ==========================================================
   EQUIPAMENTOS (~10) — SERIAL UNICO
========================================================== */
            INSERT INTO ativos_equipamentos
            (
                posicao,
                tipo,
                serial,
                estado_atual,
                fabricante,
                data_aquisicao,
                sala_id
            )
            SELECT
                gs AS posicao,
            
                CASE
                    WHEN gs % 3 = 0 THEN 'COMPUTADOR'
                    WHEN gs % 3 = 1 THEN 'PROJETOR'
                    ELSE 'AR_CONDICIONADO'
                END AS tipo,
            
                'EQP2026' || LPAD(gs::text, 6, '0') AS serial,
            
                CASE
                    WHEN gs % 3 = 0 THEN 'FUNCIONANDO'
                    WHEN gs % 3 = 1 THEN 'MANUTENCAO'
                    ELSE 'DEFEITUOSO'
                END AS estado_atual,
            
                'FABRICANTE_' || gs,
            
                CURRENT_DATE - (gs * 15),
            
                CASE
                    WHEN gs <= 5 THEN (
                        SELECT sala_id
                        FROM locais_salas
                        WHERE localizacao = 'A101'
                    )
                    ELSE (
                        SELECT sala_id
                        FROM locais_salas
                        WHERE localizacao = 'B201'
                    )
                END AS sala_id
            
            FROM generate_series(1, 10) gs;



            /* ==========================================================
               HISTORICO DE MANUTENCOES (5–20 POR EQUIPAMENTO)
            ========================================================== */
            INSERT INTO ativos_historicomanutencoes (titulo, data, equipamento_id)
            SELECT
                'Manutenção ' || gs,
                make_date(
                    2025,
                    (gs % 12) + 1,
                    ((gs * 3) % 28) + 1
                ),
                e.equipamento_id
            FROM ativos_equipamentos e
            JOIN generate_series(5, 20) gs ON true;


            /* ==========================================================
               REPORTES (11–15)
            ========================================================== */
            INSERT INTO suporte_reportes
            (titulo, mensagem, estado_atual, data, equipamento_id, usuario_id)
            VALUES
            -- Equipamento 1 (PROJETOR)
            ('Reporte projetor não liga', 'Projetor apresenta falha ao ligar', 'ABERTO',
             NOW() - INTERVAL '1 day', 1, 2),
            
            -- Equipamento 2 (AR_CONDICIONADO)
            ('Ar não resfria', 'Ar condicionado sem refrigeração adequada', 'FECHADO',
             NOW() - INTERVAL '2 days', 2, 4),
            
            -- Equipamento 3 (COMPUTADOR)
            ('Computador lento', 'Computador com desempenho muito lento', 'ABERTO',
             NOW() - INTERVAL '3 days', 3, 2),
            
            -- Equipamento 4 (PROJETOR)
            ('Imagem falhando', 'Projetor piscando durante uso', 'FECHADO',
             NOW() - INTERVAL '4 days', 4, 4),
            
            -- Equipamento 5 (AR_CONDICIONADO)
            ('Vazamento de água', 'Ar condicionado vazando água', 'ABERTO',
             NOW() - INTERVAL '5 days', 5, 2),
            
            -- Equipamento 6 (COMPUTADOR)
            ('PC não liga', 'Computador não responde ao botão power', 'FECHADO',
             NOW() - INTERVAL '6 days', 6, 4),
            
            -- Equipamento 7 (PROJETOR)
            ('Lâmpada fraca', 'Projetor com luminosidade muito baixa', 'ABERTO',
             NOW() - INTERVAL '7 days', 7, 2),
            
            -- Equipamento 8 (AR_CONDICIONADO)
            ('Ruído excessivo', 'Ar condicionado muito barulhento', 'FECHADO',
             NOW() - INTERVAL '8 days', 8, 4),
            
            -- Equipamento 9 (COMPUTADOR)
            ('Tela azul', 'Computador apresentou tela azul', 'ABERTO',
             NOW() - INTERVAL '9 days', 9, 2),
            
            -- Equipamento 10 (PROJETOR)
            ('Superaquecendo', 'Projetor esquenta demais após 10 minutos', 'FECHADO',
             NOW() - INTERVAL '10 days', 10, 4),
            
            -- Repetição com outros dias / equipamentos
            ('Mouse não funciona', 'Problema no mouse do computador', 'ABERTO',
             NOW() - INTERVAL '11 days', 3, 2),
            
            ('Controle não responde', 'Controle remoto do projetor não funciona', 'FECHADO',
             NOW() - INTERVAL '12 days', 1, 4);



                        INSERT INTO agendas_agendamentos
            (inicio, fim, data, estado_atual, sala_id)
            VALUES
            -- HOJE (AGORA)
            ('08:00:00', '10:00:00', CURRENT_DATE, 'FAZENDO',     1),
            ('08:00:00', '10:00:00', CURRENT_DATE, 'FAZENDO',     2),
            ('08:00:00', '10:00:00', CURRENT_DATE, 'INACABADO',   3),
            ('08:00:00', '10:00:00', CURRENT_DATE, 'INACABADO',   4),
            
            -- =========================
            -- AMANHÃ
            -- =========================
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '1 day', 'FEITO', 1),
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '1 day', 'FEITO', 2),
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '1 day', 'FEITO', 3),
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '1 day', 'FEITO', 4),
            
            -- =========================
            -- DAQUI A 2 DIAS
            -- =========================
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '2 days', 'ESPERANDO_CONFIRMACAO', 1),
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '2 days', 'ESPERANDO_CONFIRMACAO', 2),
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '2 days', 'ESPERANDO_CONFIRMACAO', 3),
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '2 days', 'ESPERANDO_CONFIRMACAO', 4),
            
            -- =========================
            -- DAQUI A 3 DIAS
            -- =========================
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '3 days', 'FAZENDO', 1),
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '3 days', 'FAZENDO', 2),
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '3 days', 'FAZENDO', 3),
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '3 days', 'FAZENDO', 4),
            
            -- =========================
            -- DAQUI A 4 DIAS
            -- =========================
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '4 days', 'FEITO', 1),
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '4 days', 'FEITO', 2),
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '4 days', 'FEITO', 3),
            ('08:00:00', '10:00:00', CURRENT_DATE + INTERVAL '4 days', 'FEITO', 4);



            /* ==========================================================
               TECNICOS NOS AGENDAMENTOS (SOLO E DUPLA)
            ========================================================== */
            INSERT INTO agendas_tecnicostiagendamentos (agendamento_id, tecnico_id)
            SELECT a.agendamento_id, t.usuario_id
            FROM agendas_agendamentos a
            JOIN contas_tecnicosti t ON true
            WHERE a.agendamento_id % 2 = 0;

            INSERT INTO agendas_tecnicostiagendamentos (agendamento_id, tecnico_id)
            SELECT a.agendamento_id, MIN(usuario_id)
            FROM contas_tecnicosti
            JOIN agendas_agendamentos a ON a.agendamento_id % 3 = 0
            GROUP BY a.agendamento_id;


                        /* ==========================================================
                           AUDITORIA
                        ========================================================== */
                        INSERT INTO auditoria_auditorialog
            (acao, data, alvo_acao, usuario_id)
            VALUES
            
            /* =========================
               ADMINISTRADOR
            ========================= */
            ('CRIAR_PREDIO',        CURRENT_DATE - 10, 'PREDIO',        1),
            ('ATUALIZAR_PREDIO',    CURRENT_DATE - 9,  'PREDIO',        1),
            ('CRIAR_SETOR',         CURRENT_DATE - 9,  'SETOR',         1),
            ('ATUALIZAR_SETOR',     CURRENT_DATE - 8,  'SETOR',         1),
            ('CRIAR_SALA',          CURRENT_DATE - 8,  'SALA',          1),
            ('ATUALIZAR_SALA',      CURRENT_DATE - 7,  'SALA',          1),
            ('CRIAR_EQUIPAMENTO',   CURRENT_DATE - 7,  'COMPUTADOR',    1),
            ('ATUALIZAR_EQUIPAMENTO',CURRENT_DATE - 6, 'PROJETOR',      1),
            ('CRIAR_USUARIO',       CURRENT_DATE - 6,  'ALUNO',         1),
            ('CRIAR_USUARIO',       CURRENT_DATE - 5,  'TECNICO_TI',    1),
            
            /* =========================
               TÉCNICO DE TI
            ========================= */
            ('CRIAR_AGENDAMENTO',        CURRENT_DATE - 5, 'AGENDAMENTO',        3),
            ('ATUALIZAR_AGENDAMENTO',   CURRENT_DATE - 4, 'AGENDAMENTO',        3),
            ('CRIAR_AGENDAMENTO',        CURRENT_DATE - 3, 'AGENDAMENTO',        3),
            ('TROCAR_EQUIPAMENTO_SALA', CURRENT_DATE - 3, 'AR_CONDICIONADO',    3),
            ('TROCAR_EQUIPAMENTO_SALA', CURRENT_DATE - 2, 'PROJETOR',           3),
            ('ATUALIZAR_AGENDAMENTO',   CURRENT_DATE - 1, 'AGENDAMENTO',        3),
            
            /* =========================
               ALUNO
            ========================= */
            ('ABRIR_REPORTE', CURRENT_DATE - 6, 'REPORTE', 2),
            ('ABRIR_REPORTE', CURRENT_DATE - 4, 'REPORTE', 2),
            ('ABRIR_REPORTE', CURRENT_DATE - 2, 'REPORTE', 2),
            ('ABRIR_REPORTE', CURRENT_DATE,     'REPORTE', 2),
            
            /* =========================
               SERVIDOR
            ========================= */
            ('ABRIR_REPORTE', CURRENT_DATE - 7, 'REPORTE', 4),
            ('ABRIR_REPORTE', CURRENT_DATE - 5, 'REPORTE', 4),
            ('ABRIR_REPORTE', CURRENT_DATE - 3, 'REPORTE', 4),
            ('ABRIR_REPORTE', CURRENT_DATE - 1, 'REPORTE', 4),
            ('ABRIR_REPORTE', CURRENT_DATE,     'REPORTE', 4);

            """,

            reverse_sql="""
            DELETE FROM auditoria_auditorialog;
            DELETE FROM agendas_tecnicostiagendamentos;
            DELETE FROM agendas_agendamentos;
            DELETE FROM suporte_reportes;
            DELETE FROM ativos_historicomanutencoes;
            DELETE FROM ativos_equipamentos WHERE serial LIKE 'EQP2026%';
            DELETE FROM locais_salas;
            DELETE FROM locais_setores;
            DELETE FROM locais_predios;
            """
        ),
    ]
