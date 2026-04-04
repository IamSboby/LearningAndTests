def caesar(text, shift, mode='encrypt'):
    if mode == 'decrypt':
        shift = -shift

    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)


def main():
    print()
    print("╔══════════════════════════════╗")
    print("║     🔐  CAESAR CIPHER        ║")
    print("╠══════════════════════════════╣")
    print("║  [1]  Encrypt                ║")
    print("║  [2]  Decrypt                ║")
    print("╚══════════════════════════════╝")

    while True:
        choice = input("\n  Choose [1/2]: ").strip()
        if choice in ('1', '2'):
            break
        print("  ⚠️  Enter 1 or 2.")

    mode = 'encrypt' if choice == '1' else 'decrypt'
    text = input(f"\n  Text to {mode}: ")

    while True:
        try:
            shift = int(input("  Shift (1-25): "))
            if 1 <= shift <= 25:
                break
            print("  ⚠️  Must be between 1 and 25.")
        except ValueError:
            print("  ⚠️  Enter a whole number.")

    output = caesar(text, shift, mode)

    print()
    print("╔══════════════════════════════════════════════╗")
    print(f"║  Mode   : {mode:<35}║")
    print(f"║  Shift  : {shift:<35}║")
    print(f"║  Input  : {text[:35]:<35}║")
    print(f"║  Output : {output[:35]:<35}║")
    print("╚══════════════════════════════════════════════╝")
    print()


if __name__ == "__main__":
    main()