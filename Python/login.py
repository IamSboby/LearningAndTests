import getpass

# --- Users "database" ---
USERS = {
    "admin": "1234",
    "sboby": "hello123",
}

MAX_ATTEMPTS = 3


def login():
    print("=" * 30)
    print("       🔒 LOGIN REQUIRED")
    print("=" * 30)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()  # hides input while typing

        if USERS.get(username) == password:
            print(f"\n✅ Welcome, {username}! You're in.\n")
            return username
        else:
            remaining = MAX_ATTEMPTS - attempt
            if remaining > 0:
                print(f"❌ Wrong credentials. {remaining} attempt(s) left.\n")
            else:
                print("🚫 Too many failed attempts. Access denied.\n")
                return None


def main():
    user = login()

    if user:
        # --- Your protected app starts here ---
        print("=" * 30)
        print("       🏠 SECRET AREA")
        print("=" * 30)
        print("You have accessed the protected zone.")
        print("(Put whatever you want in here!)")


if __name__ == "__main__":
    main()