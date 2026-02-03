#!/usr/bin/env python3
"""
Gerador de ícones PWA para EBSERH TI Study App
Cria ícones em múltiplos tamanhos a partir de um ícone base
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Cria um ícone quadrado com o tamanho especificado"""
    # Criar imagem com fundo azul
    img = Image.new('RGB', (size, size), color='#3498db')
    draw = ImageDraw.Draw(img)
    
    # Tentar usar fonte padrão, se não disponível usar fonte bitmap
    try:
        # Tenta carregar uma fonte TrueType
        font_size = max(size // 8, 8)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Usa fonte padrão se Arial não estiver disponível
        font = ImageFont.load_default()
    
    # Desenhar ícone de graduação (chapéu)
    margin = size // 8
    cap_width = size - 2 * margin
    cap_height = cap_width // 3
    
    # Base do chapéu
    draw.rectangle([margin, size - margin - cap_height//2, size - margin, size - margin], 
                   fill='#2c3e50')
    
    # Topo do chapéu (quadrado)
    top_size = cap_width * 2 // 3
    top_x = (size - top_size) // 2
    top_y = size - margin - cap_height - top_size // 2
    draw.rectangle([top_x, top_y, top_x + top_size, top_y + top_size], 
                   fill='#2c3e50')
    
    # Texto "EBSERH" (se tamanho for grande suficiente)
    if size >= 96:
        text = "EBSERH"
        try:
            text_font_size = max(size // 12, 6)
            text_font = ImageFont.truetype("arial.ttf", text_font_size)
            bbox = draw.textbbox((0, 0), text, font=text_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (size - text_width) // 2
            text_y = margin
            draw.text((text_x, text_y), text, fill='white', font=text_font)
        except:
            pass
    
    # Adicionar texto "TI" (se tamanho for grande suficiente)
    if size >= 128:
        text = "TI"
        try:
            ti_font_size = max(size // 10, 8)
            ti_font = ImageFont.truetype("arial.ttf", ti_font_size, weight="bold")
            bbox = draw.textbbox((0, 0), text, font=ti_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (size - text_width) // 2
            text_y = top_y - text_height - 5
            draw.text((text_x, text_y), text, fill='white', font=ti_font)
        except:
            pass
    
    # Salvar imagem
    img.save(output_path, 'PNG')
    print(f"Icone {size}x{size} criado: {output_path}")

def generate_all_icons():
    """Gera todos os ícones necessários para PWA"""
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    icons_dir = "static/icons"
    
    # Criar diretório se não existir
    os.makedirs(icons_dir, exist_ok=True)
    
    print("Gerando icones PWA para EBSERH TI Study App...")
    
    for size in sizes:
        output_path = os.path.join(icons_dir, f"icon-{size}x{size}.png")
        create_icon(size, output_path)
    
    print(f"\n{len(sizes)} icones gerados com sucesso!")
    print(f"Local: {icons_dir}/")
    
    # Criar favicon.ico (16x16, 32x32, 48x48)
    print("\nCriando favicon.ico...")
    favicon_sizes = [16, 32, 48]
    favicon_images = []
    
    for size in favicon_sizes:
        temp_path = os.path.join(icons_dir, f"temp-{size}.png")
        create_icon(size, temp_path)
        img = Image.open(temp_path)
        favicon_images.append(img)
        os.remove(temp_path)
    
    favicon_path = os.path.join("static", "favicon.ico")
    favicon_images[0].save(favicon_path, format='ICO', sizes=[(16,16), (32,32), (48,48)])
    print(f"Favicon criado: {favicon_path}")
    
    # Limpar imagens temporárias
    for img in favicon_images:
        img.close()

if __name__ == "__main__":
    try:
        generate_all_icons()
        print("\nIcones PWA prontos para uso!")
        print("\nProximos passos:")
        print("1. Atualize base.html com as meta tags PWA")
        print("2. Configure o servidor para servir os arquivos estaticos")
        print("3. Teste a instalacao do PWA")
    except Exception as e:
        print(f"Erro ao gerar icones: {e}")
        print("Certifique-se de que o Pillow esta instalado: pip install Pillow")
