import json
from pathlib import Path


def load_people_data(json_path):
    """verileri yükleyip her kişi için tek bir metin döner"""
    path = Path(json_path)
    with path.open("r",encoding="utf-8") as f:
        people = json.load(f)

    
    docs = []

    for i , person in enumerate(people):
        person_text = f"""
        Name: {person['name']}
        Role: {person['role']}
        Main Challenge: {person['challenge']}
        Team Role: {person['team_role']}
        AI Expectation: {person['ai_expectation']}
        Motivation: {person['motivation']}
        Communication Style: {person['communication']}
        Company Culture: {', '.join(person['company_culture'])}
        Problem Solving Style: {person['problem_solving']}
        Routine: {person['routine']}
        Daily Reminder Wish: {person['daily_reminder']}
        """.strip()
        
        docs.append({
            "id": f"person_{i}",
            "content": person_text
        })

    return docs