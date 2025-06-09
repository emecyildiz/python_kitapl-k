from db import (create_tables, add_user, get_user, add_book, list_books,
                list_books_with_status, is_book_available, add_transaction)

def admin_menu():
    while True:
        print("\n--- Admin Menü ---")
        print("1. Personel Ekle")
        print("2. Çıkış")

        secim = input("Seçiminiz: ")

        if secim == '1':
            name = input("Personel adı: ")
            password = input("Personel şifresi: ")
            add_user(name, "personel", password, added_by=1)  # added_by=1 → Admin ID
            print(f"Personel {name} eklendi.")
        elif secim == '2':
            break
        else:
            print("Geçersiz seçim.")


def kullanici_menu(user):
    while True:
        print("\n--- Kitap Listesi ---")
        books = list_books_with_status()
        for book in books:
            status = book[4]
            status_str = ""
            if status == "kiralama":
                status_str = " (Şu anda kiralık)"
            elif status == "satin_alma":
                continue  # Satın alınan kitap listeden siliniyor
            print(f"İsim: {book[1]}, Fiyat: {book[2]}, Kategori: {book[3]}{status_str}")

        secim = input("\nSatın almak veya kiralamak istediğiniz kitabın ismini yazın (Çıkmak için 'q'): ")
        if secim.lower() == 'q':
            break

        secilen_kitap = None
        for book in books:
            if book[1].lower() == secim.lower():
                secilen_kitap = book
                break

        if not secilen_kitap:
            print("Kitap bulunamadı, lütfen tekrar deneyin.")
            continue

        if not is_book_available(secilen_kitap[0]):
            print("Üzgünüz, bu kitap şu anda kiralanmış veya satın alınmış.")
            continue

        islem = input("Satın almak için 's', kiralamak için 'k' yazın: ").lower()
        if islem == 's':
            add_transaction(user[0], secilen_kitap[0], "satin_alma")
            print(f"'{secilen_kitap[1]}' kitabını satın aldınız.")
        elif islem == 'k':
            add_transaction(user[0], secilen_kitap[0], "kiralama")
            print(f"'{secilen_kitap[1]}' kitabını kiraladınız.")
        else:
            print("Geçersiz işlem seçildi.")


def personel_menu(user):
    while True:
        print("\n--- Personel Menü ---")
        print("1. Kullanıcı Ekle")
        print("2. Kitap Ekle")
        print("3. Kitapları Listele")
        print("4. Çıkış")

        secim = input("Seçiminiz: ")

        if secim == '1':
            name = input("Kullanıcı adı: ")
            password = input("Kullanıcı şifresi: ")
            add_user(name, "kullanıcı", password, added_by=user[0])  # user[0] = Personel ID
            print(f"Kullanıcı {name} eklendi.")
        elif secim == '2':
            name = input("Kitap adı: ")
            price = float(input("Kitap fiyatı: "))
            category = input("Kitap türü: ")
            add_book(name, price, category)
            print(f"Kitap {name} eklendi.")
        elif secim == '3':
            books = list_books()
            print("\n--- Kitap Listesi ---")
            for book in books:
                print(f"ID: {book[0]}, İsim: {book[1]}, Fiyat: {book[2]}, Tür: {book[3]}")
        elif secim == '4':
            break
        else:
            print("Geçersiz seçim.")

def main():
    create_tables()

    # En başta admin şifresi sabit (örnek)
    admin_name = "admin"
    admin_password = "admin123"

    # Eğer admin yoksa ekle
    admin = get_user(admin_name, admin_password)
    if not admin:
        add_user(admin_name, "admin", admin_password)
        print("Admin kullanıcı oluşturuldu.")

    while True:
        print("\n--- Giriş Sistemi ---")
        name = input("Kullanıcı adı: ")
        password = input("Şifre: ")

        user = get_user(name, password)
        if user:
            role = user[2]  # role kolonu
            if role == "admin":
                admin_menu()
            elif role == "personel":
                personel_menu(user)
            else:
                kullanici_menu(user)
        else:
            print("Kullanıcı adı veya şifre yanlış!")

if __name__ == "__main__":
    main()
