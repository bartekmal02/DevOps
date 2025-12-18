class BookAdress:
    def __init__(self):
        self.contacts = {}
        self.next_id = 1

        self.menu_options = {
            1: ("Dodaj kontakt", self.add_contact),
            2: ("Wyświetl kontakty", self.show_contacts),
            3: ("Wyszukaj kontakt", self.search_contact),
            4: ("Usuń kontakt", self.delete_contact),
            0: ("Zakończ", self.exit_program)
        }

    def menu(self):
        while True:
            print("MENU")
            for key, value in self.menu_options.items():
                print(f"{key}. {value[0]}")

            choice = input("Wybierz opcję: ")

            if not choice.isdigit():
                print("Podaj liczbę!")
                continue

            choice = int(choice)

            if choice in self.menu_options:
                self.menu_options[choice][1]()
            else:
                print("Nieprawidłowy numer!")

    def add_contact(self):
        name = input("Imię: ")
        surname = input("Nazwisko: ")
        phone = input("Telefon: ").strip()
        email = input("Email: ")

        self.contacts[self.next_id] = {
            "name": name,
            "surname": surname,
            "phone": phone,
            "email": email
        }

        print("Kontakt został dodany do słownika")
        self.next_id = self.next_id + 1

    def show_contacts(self):
        if not self.contacts:
            print("Brak kontaktów w słowniku")

        for id, data in self.contacts.items():
            print(
                f"ID: {id} | "
                f"{data['name']} {data['surname']} | "
                f"Tel: {data['phone']} | "
                f"Email: {data['email']}"
            )

    def search_contact(self):
        phone = input("Podaj numer telefonu: ").strip()

        if not phone.isdigit():
            print("Telefon musi zawiera wyłacznie cyfry")
            return

        for id, data in self.contacts.items():
            if data["phone"] == phone:
                print(
                    f"ID: {id} | "
                    f"{data['name']} {data['surname']} | "
                    f"Tel: {data['phone']} | "
                    f"Email: {data['email']}"
                )
                return

        print("Nie znaleziono kontaktu")

    def delete_contact(self):
        id = input("Podaj ID kontaktu do usunięcia: ")

        if not id.isdigit():
            print("ID musi być liczbą")
            return

        id = int(id)

        if id in self.contacts:
            del self.contacts[id]
            print("Kontakt usunięty")
        else:
            print("Nieprawidłowe id")

    def exit_program(self):
        print("Koniec programu")
        exit()

def main():
    book = BookAdress()
    book.menu()

if __name__ == "__main__":
    main()