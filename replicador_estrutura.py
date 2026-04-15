#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replicador de Estrutura de Pastas
- Replica somente a árvore de diretórios de uma pasta de origem
- Não copia arquivos
- Destino padrão: pasta Downloads do usuário
- Pode ser executado por linha de comando ou de forma interativa
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from pathlib import Path
from typing import Tuple


def get_downloads_dir() -> Path:
    """Tenta localizar a pasta Downloads do usuário de forma simples e confiável."""
    home = Path.home()

    candidates = [
        home / 'Downloads',
        home / 'downloads',
    ]

    userprofile = os.environ.get('USERPROFILE')
    if userprofile:
        candidates.insert(0, Path(userprofile) / 'Downloads')

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate

    fallback = home / 'Downloads'
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def normalize_path(value: str) -> Path:
    value = value.strip().strip('"').strip("'")
    return Path(value).expanduser()


def validate_source(source: Path) -> Path:
    if not source.exists():
        raise FileNotFoundError(f'A pasta de origem não existe: {source}')
    if not source.is_dir():
        raise NotADirectoryError(f'O caminho de origem não é uma pasta: {source}')
    return source.resolve()


def count_structure(source: Path) -> Tuple[int, int]:
    folder_count = 0
    file_count = 0
    for _, dirs, files in os.walk(source):
        folder_count += len(dirs)
        file_count += len(files)
    return folder_count, file_count


def build_output_root(source: Path, destination_base: Path, output_name: str | None = None) -> Path:
    timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    if output_name:
        final_name = output_name
    else:
        final_name = f'ESTRUTURA_VAZIA_{source.name}_{timestamp}'
    return destination_base / final_name


def replicate_structure(source: Path, final_output_root: Path, keep_root_folder: bool = True) -> Tuple[int, int, Path]:
    source = source.resolve()
    final_output_root.mkdir(parents=True, exist_ok=True)

    target_base = final_output_root / source.name if keep_root_folder else final_output_root
    target_base.mkdir(parents=True, exist_ok=True)

    created_dirs = 1 if keep_root_folder else 0
    skipped_files = 0

    for current_root, dirs, files in os.walk(source):
        current_root_path = Path(current_root)
        rel = current_root_path.relative_to(source)
        destination_current = target_base / rel
        destination_current.mkdir(parents=True, exist_ok=True)

        for directory in dirs:
            (destination_current / directory).mkdir(parents=True, exist_ok=True)
            created_dirs += 1

        skipped_files += len(files)

    return created_dirs, skipped_files, target_base


def write_report(report_path: Path, source: Path, destination: Path, created_dirs: int, skipped_files: int, scanned_subfolders: int, scanned_files: int, keep_root_folder: bool):
    report = f"""RELATÓRIO DE REPLICAÇÃO DE ESTRUTURA DE PASTAS
================================================
Data/Hora.........: {dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Origem............: {source}
Destino final.....: {destination}
Mantém pasta raiz.: {'Sim' if keep_root_folder else 'Não'}
Subpastas lidas...: {scanned_subfolders}
Arquivos lidos....: {scanned_files}
Pastas criadas....: {created_dirs}
Arquivos copiados.: 0
Arquivos ignorados: {skipped_files}

Observação:
Este processo recriou apenas a organização das pastas.
Nenhum arquivo da origem foi copiado.
"""
    report_path.write_text(report, encoding='utf-8')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Replica a estrutura de pastas de uma origem para um destino, sem copiar arquivos.'
    )
    parser.add_argument('origem', nargs='?', help='Caminho da pasta de origem')
    parser.add_argument('--destino', help='Pasta base de destino. Padrão: Downloads do usuário')
    parser.add_argument('--nome-saida', help='Nome da pasta de saída criada no destino')
    parser.add_argument('--sem-raiz', action='store_true', help='Não recriar a pasta raiz da origem dentro da saída')
    return parser.parse_args()


def main() -> int:
    print('\n=== REPLICADOR DE ESTRUTURA DE PASTAS ===')
    print('Este script copia apenas a organização das pastas, sem copiar arquivos.\n')

    args = parse_args()

    try:
        if args.origem:
            source = normalize_path(args.origem)
        else:
            source = normalize_path(input('Informe o caminho completo da pasta de origem: ').strip())
        source = validate_source(source)

        if args.destino:
            destination_base = normalize_path(args.destino)
        else:
            manual_destination = input('Informe a pasta base de destino (pressione ENTER para usar Downloads): ').strip()
            destination_base = normalize_path(manual_destination) if manual_destination else get_downloads_dir()

        destination_base.mkdir(parents=True, exist_ok=True)
        destination_base = destination_base.resolve()

        output_name = args.nome_saida
        if output_name is None:
            typed_name = input('Nome da pasta de saída (ENTER para gerar automático): ').strip()
            output_name = typed_name or None

        keep_root_folder = not args.sem_raiz

        print('\nLendo estrutura da origem...')
        scanned_subfolders, scanned_files = count_structure(source)

        final_output_root = build_output_root(source, destination_base, output_name)

        print(f'Origem................: {source}')
        print(f'Destino base..........: {destination_base}')
        print(f'Pasta de saída........: {final_output_root.name}')
        print(f'Subpastas encontradas.: {scanned_subfolders}')
        print(f'Arquivos encontrados..: {scanned_files}')
        print('Replicando estrutura...\n')

        created_dirs, skipped_files, actual_destination = replicate_structure(
            source=source,
            final_output_root=final_output_root,
            keep_root_folder=keep_root_folder,
        )

        report_path = final_output_root / 'relatorio_replicacao.txt'
        write_report(
            report_path=report_path,
            source=source,
            destination=actual_destination,
            created_dirs=created_dirs,
            skipped_files=skipped_files,
            scanned_subfolders=scanned_subfolders,
            scanned_files=scanned_files,
            keep_root_folder=keep_root_folder,
        )

        print('Processo concluído com sucesso!')
        print(f'Estrutura criada em...: {actual_destination}')
        print(f'Relatório.............: {report_path}')
        print('Nenhum arquivo foi copiado. Somente as pastas foram recriadas.\n')
        return 0

    except KeyboardInterrupt:
        print('\nOperação cancelada pelo usuário.')
        return 130
    except Exception as exc:
        print(f'\nERRO: {exc}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
