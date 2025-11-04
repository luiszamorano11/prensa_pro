
import fitz #importar módelulo de PDF
print ("el lector de pdf está instalado y funcionando")






def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text



# Cargar y extraer texto del PDF
pdf_path = "nov3.pdf"  # Cambia esto por el nombre de tu archivo PDF
texto = extract_text_from_pdf(pdf_path)
print(texto)  # Aquí ves el texto extraído

pdf_path = "nov3.pdf"  # Cambia esto si tu archivo se llama diferente

texto = extract_text_from_pdf(pdf_path)  # Usamos la función que definiste en Celda 21,10

print(texto[:1000])  # Mostramos los primeros 1000 caracteres del texto






pdf_path = "nov3.pdf"
doc = fitz.open(pdf_path)

page = doc.load_page(2)  # página 3
texto_dict = page.get_text("dict")
blocks = texto_dict["blocks"]

print(f"Spans detectados en página 3:\n")

for block in blocks:
    if block['type'] != 0:
        continue
    for line in block['lines']:
        for span in line['spans']:
            texto = span['text'].strip()
            if texto:
                print(f"Texto: '{texto}'")
                print(f"Fuente: {span['font']}")
                print(f"Tamaño: {span['size']}")
                print(f"Número de caracteres: {len(texto)}")
                print("---")


def detectar_titulos(pdf_path):
    doc = fitz.open(pdf_path)
    titulos = []
    textos_excluidos = {"Uso General", "Información"}  # Agrega más si aparecen

    for page_num in range(2, doc.page_count):  # desde página 3
        page = doc.load_page(page_num)
        texto_dict = page.get_text("dict")
        blocks = texto_dict["blocks"]

        for block in blocks:
            if block['type'] != 0:
                continue

            lines = block["lines"]
            for line in lines:
                spans = line["spans"]
                for span in spans:
                    texto = span['text'].strip()
                    font = span['font']
                    size = span['size']
                    es_negrita = "bold" in font.lower()

                    if (
                        texto
                        and es_negrita
                        and size >= 13
                        and len(texto) >= 40
                        and texto not in textos_excluidos
                    ):
                        titulos.append((texto, page_num + 1))
                        break
                else:
                    continue
                break
            else:
                continue
            break

    return titulos

titulos_detectados = detectar_titulos(pdf_path)

for idx, (titulo, pagina) in enumerate(titulos_detectados, 1):
    print(f"{idx}. {titulo} - Página {pagina}")


def extraer_noticias_completas(pdf_path, titulos_detectados):
    doc = fitz.open(pdf_path)
    noticias = []

    for i, (titulo, pagina_inicio) in enumerate(titulos_detectados):
        # Calcular la página final de esta noticia
        if i + 1 < len(titulos_detectados):
            pagina_siguiente = titulos_detectados[i + 1][1]
            pagina_fin = pagina_siguiente - 1
        else:
            pagina_fin = doc.page_count  # última noticia llega hasta el final

        # Extraer texto de todas las páginas correspondientes
        texto = ""
        for num in range(pagina_inicio - 1, pagina_fin):
            page = doc.load_page(num)
            texto += page.get_text()

        noticias.append({
            "titulo": titulo,
            "pagina_inicio": pagina_inicio,
            "pagina_fin": pagina_fin,
            "paginas": list(range(pagina_inicio, pagina_fin + 1)),
            "texto": texto.strip()
        })

    return noticias

noticias = extraer_noticias_completas(pdf_path, titulos_detectados)

for i, noticia in enumerate(noticias, 1):
    print(f"Noticia {i}")
    print(f"Título: {noticia['titulo']}")
    print(f"Páginas: {noticia['paginas']}")
    print(f"Texto (primeros 300 caracteres):\n{noticia['texto'][:300]}")
    print("-" * 80)

#elección de las noticias a resumir 
selección = input ("Escribe los números de las noticias que quieres resumir (separados por comas): ")
indices = [int(n.strip()) - 1 for n in selección.split(",") if n.strip().isdigit()]

#Obtener los textos de las noticias seleccionadas
noticias_seleccionadas = [noticias[i] for i in indices if 0 <= i < len(noticias)]


from summary_claude import resumir_con_claude

import json

resumenes_para_word = []

print("\n=== Resúmenes generados ===\n")
for i, noticia in enumerate(noticias_seleccionadas, 1):
    print(f"▶ Resumiendo noticia {i}: {noticia['titulo']}")
    resumen = resumir_con_claude(noticia["texto"])
    print(f"\n📝 Resumen {i}:\n{resumen}")
    print("-" * 80)

    resumenes_para_word.append({
        "titulo": noticia["titulo"],
        "resumen": resumen
    })

# Guardar los resúmenes en un archivo temporal
with open("resumenes_aprobados.json", "w", encoding="utf-8") as f:
    json.dump(resumenes_para_word, f, ensure_ascii=False, indent=2)

print("Resúmenes guardados en 'resumenes_aprobados.json'")


