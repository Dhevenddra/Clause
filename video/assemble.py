"""Assemble the pitch video: cards + footage segments + narration -> CLAUSE-pitch.mp4

Run: python video/assemble.py
"""
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
AUDIO = HERE / "audio"
SEGS = HERE / "segs"
SEGS.mkdir(exist_ok=True)

marks = json.loads((HERE / "marks.json").read_text())
durs = json.loads((AUDIO / "durations.json").read_text())
RAW = marks["_video_file"]
PAD = 0.5  # breathing room after each narration segment

V_ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30"]
A_ENC = ["-c:a", "aac", "-ar", "44100", "-ac", "2", "-b:a", "160k"]


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"ffmpeg failed:\n{' '.join(cmd)}\n{r.stderr[-1500:]}")


def card(name: str, png: str) -> None:
    d = durs[name] + PAD
    run(["ffmpeg", "-y", "-loop", "1", "-t", f"{d}", "-i", str(HERE / "cards" / png),
         "-i", str(AUDIO / f"{name}.mp3"),
         "-filter_complex", "[0:v]scale=1280:720,fps=30[v];[1:a]apad[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{d}", *V_ENC, *A_ENC, str(SEGS / f"{name}.mp4")])


def footage(name: str, subclips: list[tuple[float, float]]) -> None:
    """subclips: (start, end) in raw-video seconds; last clip freeze-extended to fit narration."""
    d = durs[name] + PAD
    clips_len = sum(e - s for s, e in subclips)
    freeze = max(0.0, d - clips_len)
    parts, labels = [], []
    for i, (s, e) in enumerate(subclips):
        tail = f",tpad=stop_mode=clone:stop_duration={freeze:.2f}" if i == len(subclips) - 1 and freeze > 0.05 else ""
        parts.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS{tail}[v{i}]")
        labels.append(f"[v{i}]")
    fc = ";".join(parts) + f";{''.join(labels)}concat=n={len(subclips)}:v=1:a=0,scale=1280:720,fps=30[v];[1:a]apad[a]"
    run(["ffmpeg", "-y", "-i", RAW, "-i", str(AUDIO / f"{name}.mp3"),
         "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{d}", *V_ENC, *A_ENC,
         str(SEGS / f"{name}.mp4")])


m = marks
card("s1_problem", "card1.png")
footage("s2_intro", [(m["hero"] + 0.5, m["adjudicate_click"])])
footage("s3_verdict", [(m["adjudicate_click"], m["adjudicate_click"] + 4.0),
                       (m["result_visible"] - 0.3, m["result_visible"] + 4.9)])
footage("s4_ledger", [(m["ledger"] - 0.3, m["highlight_click"] + 4.9)])
footage("s5_adversarial", [(m["adversarial_paste"], m["adv_click"] + 4.0),
                           (m["adv_result"] - 0.3, m["end"] - 0.1)])
footage("s6_audit", [(m["audit"], m["audit"] + 4.0)])
card("s7_tech", "card7.png")
card("s8_close", "card8.png")

order = ["s1_problem", "s2_intro", "s3_verdict", "s4_ledger", "s5_adversarial", "s6_audit", "s7_tech", "s8_close"]
listfile = SEGS / "list.txt"
listfile.write_text("".join(f"file '{(SEGS / f'{n}.mp4').as_posix()}'\n" for n in order))
final = HERE / "CLAUSE-pitch.mp4"
run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile), "-c", "copy", str(final)])

probe = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration,size",
                        "-of", "json", str(final)], capture_output=True, text=True)
print(probe.stdout)
print(f"final: {final}")
