import zlib
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="Инструмент для распаковки zlib-данных")
    parser.add_argument("input", help="Путь к сжатому файлу")
    parser.add_argument("-o", "--output", help="Путь для сохранения (по умолчанию: out.bin)")
    
    args = parser.parse_args()
    
    output_path = args.output if args.output else "out.bin"

    if not os.path.exists(args.input):
        print(f"[-] Ошибка: Файл '{args.input}' не найден.")
        sys.exit(1)

    try:
        with open(args.input, 'rb') as f:
            compressed_data = f.read()
            
        print(f"[*] Чтение {len(compressed_data)} байт...")

        decompressed_data = zlib.decompress(compressed_data)

        with open(output_path, 'wb') as f:
            f.write(decompressed_data)
            
        print(f"[+] Успешно! Распаковано {len(decompressed_data)} байт.")
        print(f"[+] Результат сохранен в: {output_path}")

    except zlib.error as e:
        print(f"[-] Ошибка zlib: {e}")
        print("[!] Возможно, файл не является валидным zlib-архивом или поврежден.")
    except Exception as e:
        print(f"[-] Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
