import json
from models import db
from extensions import app
from models import (DidYouKnow, Playground, NeverHaveIEver, HotTakes,
                    Hypotheticals, Riddle, StoryBuilder, WouldYouRather, TwoTruthsAndALie)


def seed_did_you_know():
    with app.app_context():
        # Load JSON
        with open('games/did_you_know.json', encoding='utf-8') as file:
            data = json.load(file)

        did_you_know_data = data.get("did you know", {})

        # 1. Create or get Playground row
        playground = Playground.query.filter_by(type="did you know").first()
        if not playground:
            playground = Playground(type="did you know")
            db.session.add(playground)
            # db.session.commit()
            print("✅ Created Playground entry for 'did you know'")

        # 2. Insert facts
        for category, facts in did_you_know_data.items():
            for fact in facts:
                # Avoid duplicates
                existing = DidYouKnow.query.filter_by(fact=fact).first()
                if not existing:
                    new_fact = DidYouKnow(
                        category=category,
                        fact=fact,
                        playground_id=playground.id
                    )
                    db.session.add(new_fact)

        db.session.commit()


def seed_nhie():
    with app.app_context():
        with open('games/never_have_i_ever.json', encoding='utf-8') as file:
            data = json.load(file)

        nhie_data = data.get("never have I ever", {})

        # Get or create Playground entry
        playground = Playground.query.filter_by(type="never have i ever").first()
        if not playground:
            playground = Playground(type="never have i ever")
            db.session.add(playground)
            db.session.commit()
            print("✅ Created Playground entry for 'never have i ever'")

        # Seed questions
        for category, questions in nhie_data.items():
            for q in questions:
                existing = NeverHaveIEver.query.filter_by(question=q).first()
                if not existing:
                    new_q = NeverHaveIEver(
                        category=category,
                        question=q,
                        playground_id=playground.id
                    )
                    db.session.add(new_q)

        db.session.commit()


def seed_hot_takes():
    with app.app_context():
        # Load JSON data
        with open('games/hot_takes.json', encoding='utf-8') as file:
            data = json.load(file)

        hot_takes_data = data.get("hot takes", {})

        # Get or create Playground entry
        playground = Playground.query.filter_by(type="hot takes").first()
        if not playground:
            playground = Playground(type="hot takes")
            db.session.add(playground)
            db.session.commit()
            print("✅ Created Playground entry for 'hot takes'")

        # Insert each opinion
        count = 0
        for category, opinions in hot_takes_data.items():
            for opinion in opinions:
                existing = HotTakes.query.filter_by(opinion=opinion).first()
                if not existing:
                    new_opinion = HotTakes(
                        category=category,
                        opinion=opinion,
                        playground_id=playground.id
                    )
                    db.session.add(new_opinion)
                    count += 1

        db.session.commit()
        print(f"✅ Inserted {count} new Hot Takes")


def seed_hypotheticals():
    with app.app_context():
        # Load JSON data
        with open('games/hypotheticals.json', encoding='utf-8') as file:
            data = json.load(file)

        hypo_data = data.get("hypotheticals", {})

        # Get or create Playground entry
        playground = Playground.query.filter_by(type="hypotheticals").first()
        if not playground:
            playground = Playground(type="hypotheticals")
            db.session.add(playground)
            db.session.commit()
            print("✅ Created Playground entry for 'hypotheticals'")

        # Insert each scenario
        count = 0
        for category, scenarios in hypo_data.items():
            for scenario in scenarios:
                existing = Hypotheticals.query.filter_by(scenario=scenario).first()
                if not existing:
                    new_scenario = Hypotheticals(
                        category=category,
                        scenario=scenario,
                        playground_id=playground.id
                    )
                    db.session.add(new_scenario)
                    count += 1

        db.session.commit()
        print(f"✅ Inserted {count} new Hypotheticals")


def seed_riddles():
    with app.app_context():
        with open('games/riddles.json', encoding='utf-8') as file:
            data = json.load(file)

        riddles_data = data.get("riddles", {})

        # Get or create Playground entry
        playground = Playground.query.filter_by(type="riddles").first()
        if not playground:
            playground = Playground(type="riddles")
            db.session.add(playground)
            db.session.commit()
            print("✅ Created Playground entry for 'riddles'")

        # Insert riddles
        count = 0
        for category, riddles in riddles_data.items():
            for riddle_obj in riddles:
                question = riddle_obj["riddle"]
                answer = riddle_obj["answer"]

                existing = Riddle.query.filter_by(question=question).first()
                if not existing:
                    new_riddle = Riddle(
                        category=category,
                        question=question,
                        answer=answer,
                        playground_id=playground.id
                    )
                    db.session.add(new_riddle)
                    count += 1

        db.session.commit()
        print(f"✅ Inserted {count} riddles into Riddle table")


def seed_story_builder():
    with app.app_context():
        with open('games/story_builder.json', encoding='utf-8') as file:
            data = json.load(file)

        starters = data.get("story_builder", [])

        # Get or create Playground entry
        playground = Playground.query.filter_by(type="story builder").first()
        if not playground:
            playground = Playground(type="story builder")
            db.session.add(playground)
            db.session.commit()
            print("✅ Created Playground entry for 'story builder'")

        # Insert story starters
        count = 0
        for item in starters:
            category = item["category"]
            starter = item["starter"]
            difficulty = item.get("difficulty", "easy")

            existing = StoryBuilder.query.filter_by(starter=starter).first()
            if not existing:
                new_entry = StoryBuilder(
                    category=category,
                    starter=starter,
                    difficulty=difficulty,
                    playground_id=playground.id
                )
                db.session.add(new_entry)
                count += 1

        db.session.commit()
        print(f"✅ Inserted {count} story starters into StoryBuilder")

def seed_would_you_rather():
    with app.app_context():
        with open('games/would_you_rather.json', encoding='utf-8') as file:
            data = json.load(file)

        wyr_data = data.get("would you rather", {})

        # Get or create Playground entry
        playground = Playground.query.filter_by(type="would you rather").first()
        if not playground:
            playground = Playground(type="would you rather")
            db.session.add(playground)
            db.session.commit()
            print("✅ Created Playground entry for 'would you rather'")

        # Insert scenarios
        count = 0
        for category, questions in wyr_data.items():
            for question in questions:
                existing = WouldYouRather.query.filter_by(scenario=question).first()
                if not existing:
                    new_entry = WouldYouRather(
                        category=category,
                        scenario=question,
                        playground_id=playground.id
                    )
                    db.session.add(new_entry)
                    count += 1

        db.session.commit()
        print(f"✅ Inserted {count} 'Would You Rather' scenarios")


def seed_two_truths_and_a_lie():
    with app.app_context():
        with open('games/two_truths_and_a_lie.json', encoding='utf-8') as file:
            data = json.load(file)

        two_truths_data = data.get("two truths and a lie", {})

        # Get or create Playground entry
        playground = Playground.query.filter_by(type="two truths and a lie").first()
        if not playground:
            playground = Playground(type="two_truths and a lie")
            db.session.add(playground)
            db.session.commit()
            print("✅ Created Playground entry for 'two truths and a lie'")

        # Insert entries
        count = 0
        for category, entries in two_truths_data.items():
            for entry in entries:
                statements = entry.get("statements", [])
                if len(statements) != 3:
                    continue  # skip malformed entries

                truths = [s["statement"] for s in statements if s["truth"] is True]
                lies = [s["statement"] for s in statements if s["truth"] is False]

                if len(truths) != 2 or len(lies) != 1:
                    continue  # skip invalid ones

                # Unpack
                true1, true2 = truths
                false = lies[0]

                # Prevent duplicate combos
                existing = TwoTruthsAndALie.query.filter_by(
                    true_statement_1=true1,
                    true_statement_2=true2,
                    false_statement=false
                ).first()

                if not existing:
                    new_entry = TwoTruthsAndALie(
                        category=category,
                        true_statement_1=true1,
                        true_statement_2=true2,
                        false_statement=false,
                        playground_id=playground.id
                    )
                    db.session.add(new_entry)
                    count += 1

        db.session.commit()
        print(f"✅ Inserted {count} 'Two Truths and a Lie' entries")
if __name__ == "__main__":
    seed_did_you_know()
    seed_nhie()
    seed_hot_takes()
    seed_hypotheticals()
    seed_riddles()
    seed_story_builder()
    seed_would_you_rather()
    seed_two_truths_and_a_lie()
