#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replicador de Estrutura de Pastas - Versão aprimorada
- Faz varredura completa e profunda em todas as subpastas
- Replica SOMENTE a árvore de diretórios
- Não copia arquivos
- Destino padrão: Downloads do usuário
- Gera relatório detalhado com a lista de todas as pastas encontradas/criadas
- Exibe mensagem final clara de conclusão
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from pathlib import Path
from typing import Iterable, List, Tuple


def get_downloads_dir() -> Path:
    home = Path.home()
    candidates = [home / 'Downloads', home / 'downloads']

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


def sanitize_folder_name(name: str) -> str:
    invalid = '<>:"/\\|?*'
    sanitized = ''.join('_' if ch in invalid else ch for ch in name).strip().rstrip('.')
    return sanitized or 'SAIDA_ESTRUTURA'


def collect_all_directories(source: Path) -> List[Path]:
    """Retorna TODAS as pastas abaixo da origem, em profundidade completa."""
    directories: List[Path] = []
    for current_root, dirs, _files in os.walk(source):
        current_root_path = Path(current_root)
        for folder_name in dirs:
            absolute_dir = current_root_path / folder_name
            rel_dir = absolute_dir.relative_to(source)
            directories.append(rel_dir)

    # Ordena por profundidade e nome para criação estável e previsível
    directories.sort(key=lambda p: (len(p.parts), str(p).lower()))
    return directories


def count_files(source: Path) -> int:
    file_count = 0
    for _, _, files in os.walk(source):
        file_count += len(files)
    return file_count


def build_output_root(source: Path, destination_base: Path, output_name: str | None = None) -> Path:
    timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    if output_name:
        final_name = sanitize_folder_name(output_name)
    else:
        final_name = f'ESTRUTURA_VAZIA_{sanitize_folder_name(source.name)}_{timestamp}'
    return destination_base / final_name


def replicate_structure(source: Path, final_output_root: Path, all_dirs: List[Path], keep_root_folder: bool = True) -> Tuple[int, Path, List[Path]]:
    final_output_root.mkdir(parents=True, exist_ok=True)

    target_base = final_output_root / source.name if keep_root_folder else final_output_root
    target_base.mkdir(parents=True, exist_ok=True)

    created_paths: List[Path] = []
    if keep_root_folder:
        created_paths.append(Path(source.name))

    for rel_dir in all_dirs:
        dest_dir = target_base / rel_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        created_paths.append((Path(source.name) / rel_dir) if keep_root_folder else rel_dir)

    return len(created_paths), target_base, created_paths


def write_report(
    report_path: Path,
    source: Path,
    destination: Path,
    created_dirs_count: int,
    scanned_subfolders: int,
    scanned_files: int,
    keep_root_folder: bool,
    created_paths: List[Path],
):
    lines = [
        'RELATÓRIO DE REPLICAÇÃO DE ESTRUTURA DE PASTAS',
        '================================================',
        f'Data/Hora..............: {dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
        f'Origem.................: {source}',
        f'Destino final..........: {destination}',
        f'Mantém pasta raiz......: {"Sim" if keep_root_folder else "Não"}',
        f'Total de subpastas lidas: {scanned_subfolders}',
        f'Total de arquivos lidos.: {scanned_files}',
        f'Total de pastas criadas.: {created_dirs_count}',
        'Arquivos copiados......: 0',
        '',
        'PASTAS CRIADAS',
        '--------------',
    ]

    if created_paths:
        lines.extend(str(path) for path in created_paths)
    else:
        lines.append('(Nenhuma subpasta encontrada; apenas a raiz foi considerada.)')

    lines.extend([
        '',
        'Observação:',
        'Este processo recriou somente a organização das pastas.',
        'Nenhum arquivo da origem foi copiado.',
    ])

    report_path.write_text('\n'.join(lines), encoding='utf-8')


def show_completion_message(message: str) -> None:
    print('\n' + '=' * 70)
    print(message)
    print('=' * 70 + '\n')

    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, message, 'Replicação concluída', 0x40)
        except Exception:
            # Se o ambiente bloquear popup, mantém apenas o console
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Replica todas as pastas de uma origem para um destino, sem copiar arquivos.'
    )
    parser.add_argument('origem', nargs='?', help='Caminho da pasta de origem')
    parser.add_argument('--destino', help='Pasta base de destino. Padrão: Downloads do usuário')
    parser.add_argument('--nome-saida', help='Nome da pasta de saída criada no destino')
    parser.add_argument('--sem-raiz', action='store_true', help='Não recriar a pasta raiz da origem dentro da saída')
    return parser.parse_args()


def main() -> int:
    print('\n=== REPLICADOR DE ESTRUTURA DE PASTAS | VARREDURA COMPLETA ===')
    print('Este script recria TODAS as pastas, inclusive pastas dentro de pastas, sem copiar arquivos.\n')

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

        print('\n[1/3] Fazendo varredura completa da estrutura...')
        all_dirs = collect_all_directories(source)
        scanned_subfolders = len(all_dirs)
        scanned_files = count_files(source)

        final_output_root = build_output_root(source, destination_base, output_name)

        print(f'Origem..................: {source}')
        print(f'Destino base............: {destination_base}')
        print(f'Pasta de saída..........: {final_output_root.name}')
        print(f'Subpastas encontradas...: {scanned_subfolders}')
        print(f'Arquivos encontrados....: {scanned_files}')

        print('\n[2/3] Recriando TODAS as pastas encontradas...')
        created_dirs_count, actual_destination, created_paths = replicate_structure(
            source=source,
            final_output_root=final_output_root,
            all_dirs=all_dirs,
            keep_root_folder=keep_root_folder,
        )

        report_path = final_output_root / 'relatorio_replicacao.txt'
        write_report(
            report_path=report_path,
            source=source,
            destination=actual_destination,
            created_dirs_count=created_dirs_count,
            scanned_subfolders=scanned_subfolders,
            scanned_files=scanned_files,
            keep_root_folder=keep_root_folder,
            created_paths=created_paths,
        )

        print('[3/3] Finalizando e gerando relatório...')

        completion_message = (
            'PROCESSO COMPLETO!\n'
            f'Estrutura recriada com sucesso em: {actual_destination}\n'
            f'Total de pastas criadas: {created_dirs_count}\n'
            f'Relatório gerado em: {report_path}\n'
            'Nenhum arquivo foi copiado.'
        )
        show_completion_message(completion_message)
        return 0

    except KeyboardInterrupt:
        print('\nOperação cancelada pelo usuário.')
        return 130
    except Exception as exc:
        print(f'\nERRO: {exc}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
