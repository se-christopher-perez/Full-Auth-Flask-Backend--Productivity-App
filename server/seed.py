from faker import Faker
from config import app, db
from models import User, JournalEntry

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    JournalEntry.query.delete()
    User.query.delete()
    db.session.commit()

    print("Creating users...")
    users = []

    for new_user in range(5):
        user = User(

            username = fake.user_name()

        )

        user.password_hash = user.username + "password"
        db.session.add(user)
        users.append(user)

    db.session.commit()

    print("Creating journal entries...")

    for user in users:
        for entry in range(5):
            journal_entry = JournalEntry(

                title = fake.sentence(nb_words=4),
                content = fake.paragraph(nb_sentences=3),
                user_id=user.id

            )

            db.session.add(journal_entry)

    db.session.commit()

    print("🌱 Seeded 🌱")