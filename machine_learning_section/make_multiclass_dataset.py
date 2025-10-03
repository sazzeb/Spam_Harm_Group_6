from __future__ import annotations
from pathlib import Path
import csv, random, os

"""
Generates machine_learning_section/spam_multiclass.csv with four labels:
  Not harmful, Not Spam, Spam, Harmful
No external data. Purely synthetic to unblock training/running.

You can control rows/class via env var ROWS_PER_CLASS (default: 250).
"""

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "machine_learning_section" / "spam_multiclass.csv"

def _samples():
    # Keep content generic and safe.
    not_spam_bases = [
        "Hey are we still meeting at 3", "Please review the document",
        "Lunch at 1 pm", "On my way now", "Thanks for your help",
        "Let’s catch up tomorrow", "Family dinner tonight", "Where did you park",
        "Project status looks good", "Can you send the notes",
    ]
    not_spam_addons = [
        "please", "thanks", "today", "tomorrow", "before noon", "after work",
        "at the library", "at the cafe", "in room 204", "when you're free",
    ]

    not_harmful_bases = [
        "The weather is nice today", "Remember to water the plants",
        "Your package should arrive tomorrow", "I enjoyed the movie",
        "Let's schedule a game night", "The file has been saved",
        "This is a reminder to back up your files", "Meeting went well",
        "Coffee was great", "Dinner was delicious",
    ]
    not_harmful_addons = [
        "just a note", "for your info", "no rush", "take care", "all good",
        "no action needed", "talk later", "see you soon", "thanks", "okay",
    ]

    spam_bases = [
        "WIN a prize now", "Congratulations you won", "Claim your FREE reward",
        "URGENT call now", "You have been selected", "Exclusive offer just for you",
        "Limited time offer", "Cheap meds available", "You are a lucky winner",
        "Act now to claim",
    ]
    spam_addons = [
        "Text WIN to 80055", "Click http://bit.ly/win", "Call 0906 123 4567",
        "No purchase necessary", "Terms apply", "Limited stock",
        "Only today", "Act fast", "100% guaranteed", "Reply STOP to opt out",
    ]

    harmful_bases = [
        "Your account was locked click the link to unlock",
        "Password expired immediately verify your account",
        "Unrecognized sign in attempt confirm details",
        "Payment failed update billing information",
        "Suspicious activity detected verify now",
        "Invoice attached open to view",
        "Security alert action required to keep access",
        "Delivery failed reschedule by confirming your info",
        "Tax refund available confirm bank details",
        "Authentication issue follow this link to resolve",
    ]
    harmful_addons = [
        "http://example-security-check.com", "http://short.co/verify",
        "We will disable your account", "Failure to act may lead to suspension",
        "Urgent response needed", "Do not share this code",
        "This is an automated alert", "Confirm within 24 hours",
        "Unusual activity detected", "Open the attachment to proceed",
    ]

    return (not_spam_bases, not_spam_addons,
            not_harmful_bases, not_harmful_addons,
            spam_bases, spam_addons,
            harmful_bases, harmful_addons)

def _generate(rows_per_class: int) -> list[tuple[str, str]]:
    random.seed(7)
    (ns_b, ns_a, nh_b, nh_a, sp_b, sp_a, hf_b, hf_a) = _samples()
    rows: list[tuple[str, str]] = []

    for _ in range(rows_per_class):
        rows.append(("Not Spam", f"{random.choice(ns_b)} {random.choice(ns_a)}."))

    for _ in range(rows_per_class):
        rows.append(("Not harmful", f"{random.choice(nh_b)} {random.choice(nh_a)}."))

    for _ in range(rows_per_class):
        rows.append(("Spam", f"{random.choice(sp_b)}. {random.choice(sp_a)}."))

    for _ in range(rows_per_class):
        rows.append(("Harmful", f"{random.choice(hf_b)}. {random.choice(hf_a)}."))

    random.shuffle(rows)
    return rows

def main():
    rows_per_class = int(os.getenv("ROWS_PER_CLASS", "250"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = _generate(rows_per_class)

    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["label", "text"])
        w.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT}")

if __name__ == "__main__":
    main()
