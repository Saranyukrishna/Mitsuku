from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .agents import agent_executor
from django.utils.html import escape
import re

def format_response(text):
    text = escape(text)
    text = re.sub(r'```(.*?)```', r'<pre>\1</pre>', text, flags=re.DOTALL)
    return text.replace('\n', '<br>')

@csrf_exempt
def chat_view(request):
    # Reset session on each browser reload (GET request)
    if request.method == "GET":
        request.session.flush()
        request.session['history'] = []

    if 'history' not in request.session:
        request.session['history'] = []

    if request.method == "POST":
        user_msg = request.POST.get("message")
        history_text = "\n".join([f"User: {h['user']}\nAI: {h['ai']}" for h in request.session['history']])
        state = {"input": user_msg, "history": history_text, "output": ""}
        result = agent_executor.invoke(state)
        ai_msg = format_response(result['output'])

        request.session['history'].append({
            "user": user_msg,
            "ai": ai_msg
        })
        request.session.modified = True

    return render(request, "chat.html", {"history": request.session['history']})