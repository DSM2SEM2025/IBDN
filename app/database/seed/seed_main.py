"""
Seed Main Module
Executa todos os scripts de seed do banco de dados IBDN em sequência.
Este script é o ponto de entrada principal para popular o banco de dados.
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.seed.seed_permissions_profiles import run_seed_permissions_profiles, verificar_estrutura
from app.database.seed.seed_usuarios import run_seed_usuarios, verificar_usuarios
from app.database.seed.seed_empresas import run_seed_empresas, verificar_empresas
from app.database.seed.seed_complementos import run_seed_complementos, verificar_complementos
from app.database.seed.seed_notificacoes import run_seed_notificacoes, verificar_notificacoes
from app.database.seed.seed_base import setup_logging


def run_all_seeds():
    """
    Executa todos os seeds em sequência (Fase 1 + Fase 2 + Fase 3).
    
    Returns:
        True se todos os seeds forem executados com sucesso
    """
    logger = setup_logging('seed_main')
    
    print("\n" + "=" * 70)
    print(" " * 15 + "SEED COMPLETO - IBDN")
    print("=" * 70 + "\n")
    
    results = {
        "permissions_profiles": {"sucesso": False},
        "usuarios": {"sucesso": False},
        "empresas": {"sucesso": False},
        "complementos": {"sucesso": False},
        "notificacoes": {"sucesso": False}
    }
    
    # ============================================================
    # FASE 1: Permissões e Perfis
    # ============================================================
    print("\n" + "=" * 70)
    print(">>> FASE 1: PERMISSÕES E PERFIS")
    print("=" * 70)
    
    try:
        results["permissions_profiles"] = run_seed_permissions_profiles(logger)
        if results["permissions_profiles"].get("sucesso"):
            verificar_estrutura(logger)
            print("\n[FASE 1 CONCLUÍDA COM SUCESSO]")
        else:
            print(f"\n[ERRO NA FASE 1]: {results['permissions_profiles'].get('erro')}")
    except Exception as e:
        logger.error(f"Erro durante FASE 1: {e}")
        results["permissions_profiles"] = {"sucesso": False, "erro": str(e)}
    
    # ============================================================
    # FASE 2: Usuários
    # ============================================================
    print("\n" + "=" * 70)
    print(">>> FASE 2: USUARIOS")
    print("=" * 70)
    
    try:
        results["usuarios"] = run_seed_usuarios(logger)
        if results["usuarios"].get("sucesso"):
            stats = verificar_usuarios(logger)
            print(f"\n[ESTATÍSTICAS]")
            print(f"  Total de usuários: {stats['total']}")
            print(f"  Por perfil: {stats['por_perfil']}")
            print(f"  Ativos: {stats['por_ativo'].get('ativos', 0)}")
            print(f"  Inativos: {stats['por_ativo'].get('inativos', 0)}")
            print("\n[FASE 2 - USUARIOS CONCLUÍDA COM SUCESSO]")
        else:
            print(f"\n[ERRO NA FASE 2 - USUARIOS]: {results['usuarios'].get('erro')}")
    except Exception as e:
        logger.error(f"Erro durante FASE 2 - Usuários: {e}")
        results["usuarios"] = {"sucesso": False, "erro": str(e)}
    
    # ============================================================
    # FASE 2: Empresas
    # ============================================================
    print("\n" + "=" * 70)
    print(">>> FASE 2: EMPRESAS")
    print("=" * 70)
    
    try:
        results["empresas"] = run_seed_empresas(logger)
        if results["empresas"].get("sucesso"):
            stats = verificar_empresas(logger)
            print(f"\n[ESTATÍSTICAS]")
            print(f"  Total de empresas: {stats['total']}")
            print(f"  Ativas: {stats['por_ativo'].get('ativas', 0)}")
            print(f"  Inativas: {stats['por_ativo'].get('inativas', 0)}")
            print("\n[FASE 2 - EMPRESAS CONCLUÍDA COM SUCESSO]")
        else:
            print(f"\n[ERRO NA FASE 2 - EMPRESAS]: {results['empresas'].get('erro')}")
    except Exception as e:
        logger.error(f"Erro durante FASE 2 - Empresas: {e}")
        results["empresas"] = {"sucesso": False, "erro": str(e)}
    
    # ============================================================
    # FASE 3A: Complementos (enderecos, empresa_ramo, empresa_selo)
    # ============================================================
    print("\n" + "=" * 70)
    print(">>> FASE 3A: COMPLEMENTOS")
    print("=" * 70)
    
    try:
        results["complementos"] = run_seed_complementos(logger)
        if results["complementos"].get("sucesso"):
            stats = verificar_complementos(logger)
            print(f"\n[ESTATÍSTICAS]")
            print(f"  Total de endereços: {stats['enderecos_total']}")
            print(f"  Endereços por faixa: {stats['enderecos_por_faixa']}")
            print(f"  Total empresa_selo: {stats['empresa_ramo_total']}")
            print(f"  Selos por status: {stats['selos_por_status']}")
            print(f"  Empresas com selos ativos: {stats['empresas_com_selos_ativos']}")
            print("\n[FASE 3A - COMPLEMENTOS CONCLUÍDA COM SUCESSO]")
        else:
            print(f"\n[ERRO NA FASE 3A - COMPLEMENTOS]: {results['complementos'].get('erro')}")
    except Exception as e:
        logger.error(f"Erro durante FASE 3A - Complementos: {e}")
        results["complementos"] = {"sucesso": False, "erro": str(e)}
    
    # ============================================================
    # FASE 3B: Notificações
    # ============================================================
    print("\n" + "=" * 70)
    print(">>> FASE 3B: NOTIFICAÇÕES")
    print("=" * 70)
    
    try:
        results["notificacoes"] = run_seed_notificacoes(logger)
        if results["notificacoes"].get("sucesso"):
            stats = verificar_notificacoes(logger)
            print(f"\n[ESTATÍSTICAS]")
            print(f"  Total de notificações: {stats['total']}")
            print(f"  Por tipo: {stats['por_tipo']}")
            print(f"  Lidas/Não lidas: {stats['por_lida']}")
            print(f"  Últimos 30 dias: {stats['ultimos_30_dias']}")
            print(f"  Empresas com notificações: {stats['empresas_com_notificacoes']}")
            print(f"  Média por empresa: {stats['media_por_empresa']}")
            print("\n[FASE 3B - NOTIFICAÇÕES CONCLUÍDA COM SUCESSO]")
        else:
            print(f"\n[ERRO NA FASE 3B - NOTIFICAÇÕES]: {results['notificacoes'].get('erro')}")
    except Exception as e:
        logger.error(f"Erro durante FASE 3B - Notificações: {e}")
        results["notificacoes"] = {"sucesso": False, "erro": str(e)}
    
    # ============================================================
    # RESUMO FINAL
    # ============================================================
    print("\n" + "=" * 70)
    print(" " * 20 + "RESUMO FINAL")
    print("=" * 70)
    
    # Usuários
    usuarios_criados = results["usuarios"].get("criados", 0)
    usuarios_total = results["usuarios"].get("total", 0)
    print(f"\n>>> USUARIOS")
    print(f"   Criados nesta execução: {usuarios_criados}")
    print(f"   Total no banco: {usuarios_total}")
    
    # Empresas
    empresas_criadas = results["empresas"].get("criadas", 0)
    empresas_total = results["empresas"].get("total", 0)
    print(f"\n>>> EMPRESAS")
    print(f"   Criadas nesta execução: {empresas_criadas}")
    print(f"   Total no banco: {empresas_total}")
    
    # Complementos
    enderecos_total = results["complementos"].get("enderecos_criados", 0)
    selos_criados = results["complementos"].get("selos_criados", 0)
    print(f"\n>>> COMPLEMENTOS (Fase 3A)")
    print(f"   Endereços criados: {enderecos_total}")
    print(f"   Selos criados: {selos_criados}")
    
    # Notificações
    notificacoes_criadas = results["notificacoes"].get("criadas", 0)
    notificacoes_total = results["notificacoes"].get("total", 0)
    print(f"\n>>> NOTIFICAÇÕES (Fase 3B)")
    print(f"   Criadas nesta execução: {notificacoes_criadas}")
    print(f"   Total no banco: {notificacoes_total}")
    
    # Verifica se todos os seeds foram bem-sucedidos
    todos_ok = all(r.get("sucesso") for r in results.values())
    
    print("\n" + "=" * 70)
    if todos_ok:
        print(" " * 20 + "SEED COMPLETO COM SUCESSO!")
    else:
        print(" " * 15 + "SEED COMPLETO COM ERROS PARCIAIS")
    print("=" * 70 + "\n")
    
    return todos_ok


if __name__ == "__main__":
    sucesso = run_all_seeds()
    exit(0 if sucesso else 1)
