from django.shortcuts import render
from .forms import MessageForm
from .services.model import predict_proba_dict

def home(request):
    form = MessageForm()
    return render(request, "home.html", {"form": form})

def classify(request):
    form = MessageForm(request.POST or None)
    result = None

    if request.method == "POST" and form.is_valid():
        text = form.cleaned_data["message"]
        proba = predict_proba_dict(text)
        # pick top label
        label, score = max(proba.items(), key=lambda kv: kv[1])
        result = {
            "label": label,  # keep exact label text (e.g., "Not Spam")
            "score": round(float(score), 4),
            "proba": {k: round(float(v), 4) for k, v in proba.items()},
            "text": text,
        }

    return render(request, "home.html", {"form": form, "result": result})
