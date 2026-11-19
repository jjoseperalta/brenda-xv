import base64
import json
import subprocess
from pathlib import Path
from urllib.parse import quote

COLUMNAS = [
    "ID",
    "Nombre",
    "Pases",
    "Estado_RSVP",
    "Asistencia",
    "Acompanante(s)",
    "Fecha",
    "URL",
]


def generar_url_invitacion(
    codigo: str,
    nombre: str,
    pases: int,
    url_base: str = "https://jjoseperalta.github.io/brenda-xv/index.html",
) -> str:
    payload = {
        "id": codigo.strip().upper(),
        "n": nombre.strip(),
        "p": int(pases),
    }
    json_str = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    b64_token = (
        base64.urlsafe_b64encode(json_str.encode("utf-8"))
        .decode("utf-8")
        .rstrip("=")
    )
    base_limpia = url_base.strip().rstrip("?")
    return f"{base_limpia}?i={quote(b64_token)}"


def generar_tsv_sheets(
    invitados: list[tuple[str, str, int, str]],
    incluir_encabezados: bool = False,
) -> str:
    lineas = []
    if incluir_encabezados:
        lineas.append("\t".join(COLUMNAS))

    for codigo, nombre, pases, url_base in invitados:
        fila = [
            codigo.strip().upper(),
            nombre.strip(),
            str(int(pases)),
            "Pendiente",
            "-",
            "-",
            "-",
            generar_url_invitacion(codigo, nombre, pases, url_base),
        ]
        lineas.append("\t".join(fila))

    return "\n".join(lineas)


def copiar_portapapeles_windows(texto: str) -> None:
    subprocess.run(["clip"], input=texto.encode("utf-16le"), check=True)


if __name__ == "__main__":
    url_gh = "https://jjoseperalta.github.io/brenda-xv/index.html"

    invitados = [
        ("INV-100", "Carlos Mendoza", 5, url_gh),
        ("INV-100", "Lucía Fernández", 6, url_gh),
        ("INV-100", "Lupita Pérez", 7, url_gh),
        ("INV-100", "Justina Biber", 8, url_gh),
    ]

    tsv = generar_tsv_sheets(invitados, incluir_encabezados=False)
    Path("invitados_sheets.tsv").write_text(tsv, encoding="utf-8")
    copiar_portapapeles_windows(tsv)

    print("Listo: copiado al portapapeles y guardado en 'invitados_sheets.tsv'.")