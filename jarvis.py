import subprocess
import json
import urllib.parse
import urllib.request

AI_URL = "http://127.0.0.1:8080/v1/chat/completions"

def run(args):
    try:
        return subprocess.run(
            args, capture_output=True, text=True, timeout=15
        )
    except Exception as e:
        print("Command error:", e)
        return None

def say(text):
    print("\nJARVIS:", text)
    run(["termux-tts-speak", text])

def ask_qwen(question):
    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are JARVIS, a concise and helpful offline "
                    "assistant running on an Android phone. "
                    "Do not claim to have performed actions you have not done."
                )
            },
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 180
    }
    try:
        request = urllib.request.Request(
            AI_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
        answer = data["choices"][0]["message"]["content"].strip()
        say(answer)
    except Exception as e:
        say("I could not reach my local AI server. Check that Qwen is running.")
        print("AI error:", e)

def open_youtube_search(query):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query)
    run(["am", "start", "-a", "android.intent.action.VIEW", "-d", url])
    say("Searching YouTube for " + query)

def battery():
    result = run(["termux-battery-status"])
    try:
        data = json.loads(result.stdout)
        say(f"Battery is {data.get('percentage')} percent.")
    except Exception:
        say("Battery information is unavailable.")

def handle(text):
    command = text.lower().strip()

    if command in ("exit", "quit", "stop", "goodbye"):
        say("Goodbye.")
        return False

    elif command in ("open youtube", "youtube"):
        run(["am", "start", "-a", "android.intent.action.VIEW", "-d", "https://youtube.com"])
        say("Opening YouTube.")

    elif "youtube" in command and any(w in command for w in ("play", "search", "song", "video", "find")):
        query = text
        for phrase in ("on youtube", "in youtube", "youtube"):
            query = query.replace(phrase, "")
        for word in ("play", "search", "find", "song", "video"):
            query = query.replace(word, "")
        open_youtube_search(query.strip() or text)

    elif command in ("open camera", "camera", "launch camera"):
        run(["am", "start", "-a", "android.media.action.STILL_IMAGE_CAMERA"])
        say("Opening camera.")

    elif command in ("open wifi", "wifi settings", "open wi-fi settings"):
        run(["am", "start", "-a", "android.settings.WIFI_SETTINGS"])
        say("Opening Wi-Fi settings.")

    elif "battery" in command:
        battery()

    elif command.startswith("ask "):
        ask_qwen(text[4:].strip())

    else:
        ask_qwen(text)

    return True

def main():
    say("JARVIS online. Type a command or ask me a question.")
    while True:
        try:
            text = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            say("Goodbye.")
            break
        if text and not handle(text):
            break

if __name__ == "__main__":
    main()
