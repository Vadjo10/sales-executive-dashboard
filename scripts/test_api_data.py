#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import httpx

API_BASE = "https://fakestoreapi.com"

ENDPOINTS = {
    "products": "products",
    "categories": "products/categories",
    "users": "users",
    "carts": "carts",
}

LABELS = {
    "products": "Produtos",
    "categories": "Categorias",
    "users": "Usuários",
    "carts": "Carrinhos",
}


def fetch_json(endpoint: str) -> list | dict:
    url = f"{API_BASE}/{endpoint}"
    print(f"\n=== GET {url} ===")
    resp = httpx.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    count = len(data) if isinstance(data, list) else 1
    print(f"Status: {resp.status_code} | Registros: {count}")
    return data


def main():
    for name, endpoint in ENDPOINTS.items():
        data = fetch_json(endpoint)
        output_path = Path("logs") / f"raw_{name}.json"
        output_path.parent.mkdir(exist_ok=True)
        output_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"Arquivo salvo: {output_path}")

    print("\n=== AMOSTRA DOS DADOS (primeiros 2 registros) ===")
    for name in ENDPOINTS:
        file_path = Path("logs") / f"raw_{name}.json"
        if not file_path.exists():
            continue
        data = json.loads(file_path.read_text(encoding="utf-8"))
        sample = data[:2] if isinstance(data, list) else [data]
        print(f"\n--- {LABELS[name]} ---")
        print(json.dumps(sample, indent=2, ensure_ascii=False)[:1000])

    print("\n=== VALIDAÇÃO RÁPIDA ===")
    results = {}
    for name in ENDPOINTS:
        file_path = Path("logs") / f"raw_{name}.json"
        if file_path.exists():
            data = json.loads(file_path.read_text(encoding="utf-8"))
            results[name] = data if isinstance(data, list) else [data]
        else:
            results[name] = []

    for name in ENDPOINTS:
        print(f"{LABELS[name]}: {len(results[name])} registros")

    all_ok = all(len(v) > 0 for v in results.values())

    if all_ok:
        print("\n[OK] TODOS OS DADOS FORAM EXTRAIDOS COM SUCESSO!")
    else:
        print("\n[FAIL] ALGUMAS EXTRACOES FALHARAM OU ESTAO VAZIAS")

    return all_ok


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
