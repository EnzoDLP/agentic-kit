---
name: expo-startup-check
description: Check frame by frame what an Expo app shows at startup (splash, blank frame, screen shown twice, jump, wrong first screen) by recording the iOS simulator and reading every distinct frame. Use for any change to the splash, startup routing, initial auth or version gating, or when a flash or a sliding screen at launch is reported.
---

# Check a startup on the simulator, frame by frame

A screenshot misses what lasts 150 ms (a blank frame, a second screen sliding in). Record the
simulator during a cold launch, extract the frames that change, and **read all of them**. Typical
catches: the home screen pushed twice, a ~150 ms blank frame between splash and home.

## 1. Prepare

- A booted simulator (`xcrun simctl list devices booted`), the app installed (dev client or build).
  Note the UDID and the variant's bundle id.
- **A bundle without dev tools**, so the app is not confused with LogBox or the dev client menu:
  Metro with `--no-dev --minify` (`--clear` if an `EXPO_PUBLIC_*` variable changed), started from
  Bash in the background. Metro started from an agent session does not read `.env`: pass it the
  variables (`npx supabase status -o env` for a local Supabase stack).
- Compile the extractor once into a scratch directory (AVFoundation, no ffmpeg needed):
  `swiftc -O -o <scratch>/extract-frames .claude/agentic-kit/layers/expo/skills/startup-check/extract-frames.swift`
- Prepare the state to test (no session, onboarding in progress, full session, maintenance, update
  required, offline forced in code for the test — removed afterwards).

## 2. Record a cold launch

```bash
xcrun simctl terminate <udid> <bundle>
xcrun simctl io <udid> recordVideo --codec=h264 --force <scratch>/start.mov &
sleep 1
xcrun simctl launch <udid> <bundle>        # dev client: simctl openurl <udid> "<scheme>://expo-development-client/?url=http%3A%2F%2Flocalhost%3A8081"
sleep 8                                     # until the screen is stable
kill -INT %1                                # SIGINT: the video is finalized cleanly
```

Start the recording in the background in **the same** Bash call as the launch (job `%1` does not
exist from one call to the next), or keep its PID.

## 3. Extract and read

```bash
<scratch>/extract-frames <scratch>/start.mov <scratch>/frames-<case> 0.033 480
```

- Every ~33 ms, only the frames that **change** are kept; `frames.tsv` gives the time (ms), the mean
  luminance and the share of changed pixels.
- **Read every kept frame** (Read tool), in order, not a sample. Look for: a blank or flat frame
  between splash and first screen (luminance jump), the expected screen then another one sliding
  over it, content jumping afterwards, a splash that stays, a wrong first screen.
- Describe the sequence with timestamps ("0–1,200 ms splash, 1,233 ms fade to the filled home
  screen, nothing moves afterwards"). Repeat for each prepared state, and for the old code to show
  the defect before / after.

## 4. Conclude

- Say what was seen, state by state, and what **could not** be seen on the simulator (universal link
  opened from Messages, notification tapped with the app closed, purchase): to do on an iPhone.
- Delete the videos and frames (they can show account data); remove any code forced for the test.
