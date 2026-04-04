import time
import random

SENTENCES = [
    "The quick brown fox jumps over the lazy dog",
    "Python is a great language for building fast programs",
    "Every great journey begins with a single step forward",
    "The stars shine brightest on the darkest of nights",
    "Coding is not just a skill it is a way of thinking",
    "A ship in harbor is safe but that is not what ships are for",
    "The only way to do great work is to love what you do",
    "In the middle of every difficulty lies an opportunity",
    "Programs must be written for people to read and machines to execute",
    "Simplicity is the soul of efficiency in every program",
]

def clear():
    print("\033[H\033[J", end="")

def color(txt, code):
    return f"\033[{code}m{txt}\033[0m"

GREEN  = lambda t: color(t, "92")
RED    = lambda t: color(t, "91")
YELLOW = lambda t: color(t, "93")
CYAN   = lambda t: color(t, "96")
BOLD   = lambda t: color(t, "1")
DIM    = lambda t: color(t, "2")

BANNER = r"""
 __          _______  __  __ _______ ______  _____ _______ 
 \ \        / /  __ \|  \/  |__   __|  ____|/ ____|__   __|
  \ \  /\  / /| |__) | \  / |  | |  | |__  | (___    | |   
   \ \/  \/ / |  ___/| |\/| |  | |  |  __|  \___ \   | |   
    \  /\  /  | |    | |  | |  | |  | |____ ____) |  | |   
     \/  \/   |_|    |_|  |_|  |_|  |______|_____/   |_|   
                                                           
"""

def print_banner():
    print(CYAN(BOLD(BANNER)))
    print(BOLD("          [ Speed Typing Test ]  --  words per minute\n"))

def wpm_rank(wpm):
    if wpm < 20:  return "Beginner"
    if wpm < 40:  return "Slow"
    if wpm < 60:  return "Average"
    if wpm < 80:  return "Fast"
    if wpm < 100: return "Very Fast"
    return            "Blazing Fast"

def accuracy(original, typed):
    orig_w  = original.split()
    typed_w = typed.split()
    correct = sum(o == t for o, t in zip(orig_w, typed_w))
    return round(correct / max(len(orig_w), 1) * 100, 1)

def progress_bar(wpm, max_wpm=120, width=40):
    filled = min(int(wpm / max_wpm * width), width)
    bar = "[" + "#" * filled + "-" * (width - filled) + "]"
    return bar

def run_test():
    sentence = random.choice(SENTENCES)
    word_count = len(sentence.split())

    clear()
    print_banner()
    print("+" + "-" * 60 + "+")
    print("|" + " TYPE THE FOLLOWING SENTENCE ".center(60) + "|")
    print("+" + "-" * 60 + "+")
    print("|" + "".center(60) + "|")
    print("|  " + YELLOW(BOLD(sentence))[:] + "")
    print("|" + "".center(60) + "|")
    print("+" + "-" * 60 + "+")
    print(DIM("  Press ENTER when ready, then type and press ENTER again."))
    input()

    print(f"\n  {GREEN('>> GO!')}  Timer running...\n")
    print("  > ", end="", flush=True)
    start = time.time()
    typed = input()
    elapsed = time.time() - start

    minutes = elapsed / 60
    wpm     = round(word_count / minutes)
    acc     = accuracy(sentence, typed)
    rank    = wpm_rank(wpm)
    bar     = progress_bar(wpm)

    clear()
    print_banner()
    print("+" + "-" * 60 + "+")
    print("|" + " RESULTS ".center(60) + "|")
    print("+" + "-" * 60 + "+")
    print(f"|  Time      : {str(round(elapsed, 2)) + 's':<46}|")
    print(f"|  Words     : {str(word_count):<46}|")
    print(f"|  WPM       : {str(wpm):<46}|")
    print(f"|  Accuracy  : {str(acc) + '%':<46}|")
    print(f"|  Rank      : {BOLD(rank):<55}|")
    print("|" + "".center(60) + "|")
    print(f"|  Speed     : {bar} {wpm}/120")
    print("|" + "".center(60) + "|")
    print("+" + "-" * 60 + "+")

    orig_w  = sentence.split()
    typed_w = typed.split() + [''] * (len(orig_w) - len(typed.split()))
    diff = " ".join(GREEN(o) if o == t else RED(o) for o, t in zip(orig_w, typed_w))
    print(f"|  {DIM('Diff')} : {diff}")
    print(f"|  {DIM('     (green = correct   red = wrong)')}")
    print("+" + "-" * 60 + "+")

    return wpm, acc

def show_stats(scores):
    if not scores:
        print(f"\n  {YELLOW('No tests run yet.')}")
        return
    avg_wpm = round(sum(s[0] for s in scores) / len(scores))
    avg_acc = round(sum(s[1] for s in scores) / len(scores), 1)
    best    = max(scores, key=lambda s: s[0])
    worst   = min(scores, key=lambda s: s[0])

    print()
    print("+" + "-" * 40 + "+")
    print("|" + " SESSION STATS ".center(40) + "|")
    print("+" + "-" * 40 + "+")
    print(f"|  Tests run   : {len(scores):<24}|")
    print(f"|  Avg WPM     : {avg_wpm:<24}|")
    print(f"|  Avg Acc     : {str(avg_acc) + '%':<24}|")
    print(f"|  Best WPM    : {str(best[0]) + ' wpm  @ ' + str(best[1]) + '% acc':<24}|")
    print(f"|  Worst WPM   : {str(worst[0]) + ' wpm  @ ' + str(worst[1]) + '% acc':<24}|")
    print("+" + "-" * 40 + "+")

def main():
    scores = []
    clear()
    print_banner()

    while True:
        print("\n  +---------------------------+")
        print("  |  [1]  Start a test        |")
        print("  |  [2]  Session stats       |")
        print("  |  [3]  Quit                |")
        print("  +---------------------------+")
        choice = input(f"\n  {BOLD('>')} ").strip()

        if choice == '1':
            wpm, acc = run_test()
            scores.append((wpm, acc))
            input(f"\n  {DIM('Press ENTER to continue...')}")
            clear()
            print_banner()
        elif choice == '2':
            show_stats(scores)
        elif choice == '3':
            print(f"\n  {CYAN('See you. Keep practicing.')}\n")
            break
        else:
            print(f"  {RED('Invalid option.')}")

if __name__ == "__main__":
    main()