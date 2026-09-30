import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
WORKOUT_MODEL=os.getenv("GEMINI_WORKOUT_MODEL","gemini-3.8-flash")
NUTRITION_MODEL=os.getenv("GEMINI_NUTRITION_MODEL","gemini-3.8-flash")

def get_client():
    key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    return genai.Client(api_key=key) if key else None

def generate_text(model,prompt):
    client=get_client()
    if not client: return None
    try:
        response=client.models.generate_content(model=model, contents=prompt)
        return response.text.strip() if response.text else None
    except Exception:
        return None

def demo_workout(user):
    return f'''7-DAY BEGINNER FITNESS PLAN\n\nUser: {user["name"]}\nGoal: {user["goal"]}\nIntensity: {user["intensity"]}\n\nDAY 1 - Full Body\n• Squats: 3 x 10\n• Incline Push-ups: 3 x 8\n• Glute Bridges: 3 x 12\n• Warm-up and cool-down: 5-10 minutes\n\nDAY 2 - Cardio\n• Brisk walk: 25-30 minutes\n• Light stretching: 10 minutes\n\nDAY 3 - Upper Body + Core\n• Incline Push-ups: 3 x 8\n• Shoulder Taps: 3 x 10\n• Bird Dog: 3 x 10 each side\n• Plank: 3 x 20 seconds\n\nDAY 4 - Recovery\n• Easy walk: 15-20 minutes\n• Gentle stretching\n\nDAY 5 - Lower Body\n• Squats: 3 x 10\n• Reverse Lunges: 3 x 8 each side\n• Calf Raises: 3 x 12\n\nDAY 6 - Cardio + Core\n• Brisk walk: 20-30 minutes\n• Dead Bug: 3 x 10\n• Plank: 3 x 20 seconds\n\nDAY 7 - Rest\n• Full rest or easy walking\n\nSafety: Start slowly and stop if you feel pain, dizziness, or unusual discomfort.'''

def generate_workout(user):
    prompt=f'''Create a simple beginner-friendly 7-day fitness plan.\nUser: {user["name"]}, age {user["age"]}, weight {user["weight"]}, goal {user["goal"]}, intensity {user["intensity"]}.\nGive Day 1 to Day 7 with warm-up, exercises, sets/reps or time, cool-down and at least one rest/recovery day. Use simple English. Do not diagnose or prescribe treatment. Add a short safety note.'''
    return generate_text(WORKOUT_MODEL,prompt) or demo_workout(user)

def generate_nutrition(user):
    prompt=f'''Give simple general nutrition tips for a person following a fitness plan. Age: {user["age"]}; weight: {user["weight"]}; goal: {user["goal"]}; intensity: {user["intensity"]}. Include hydration, protein/balanced meals, fruits/vegetables, and simple pre/post-workout suggestions. Do not give medical treatment or extreme dieting advice.'''
    return generate_text(NUTRITION_MODEL,prompt) or "Drink enough water, include protein and vegetables in regular meals, choose fruits and whole grains, and avoid extreme diets. After exercise, have a balanced meal or snack with protein and carbohydrates."

def update_workout(original_plan, feedback):
    prompt=f'''Update this 7-day fitness plan using the user's feedback.\n\nOriginal plan:\n{original_plan}\n\nFeedback:\n{feedback}\n\nKeep it beginner-friendly, practical, simple, and include a safety note.'''
    return generate_text(WORKOUT_MODEL,prompt) or original_plan+"\n\nUPDATED BASED ON FEEDBACK:\n"+feedback
