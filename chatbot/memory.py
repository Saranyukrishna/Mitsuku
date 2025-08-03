def get_history(request):
    return request.session.get("chat_history", "")

def append_history(request, user_msg, ai_msg):
    history = request.session.get("chat_history", "")
    history += f"\nUser: {user_msg}\nAI: {ai_msg}"
    request.session["chat_history"] = history
