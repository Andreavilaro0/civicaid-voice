#!/usr/bin/env bash
set -euo pipefail

SESSION="civicaid"
WIN="team"
ROOT="/Users/andreaavila/Documents/hakaton/civicaid-voice"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "Session '$SESSION' already exists. Attaching..."
  exec tmux attach -t "$SESSION"
fi

tmux new-session -d -s "$SESSION" -n "$WIN" -c "$ROOT"

# Pane inicial (sea cual sea su índice)
P0="$(tmux display-message -p -t "$SESSION:$WIN" '#{pane_id}')"

tmux select-pane -t "$P0" -T "LEAD"
tmux send-keys  -t "$P0" "cd \"$ROOT\"" C-m

# Split horizontal: crea P1 a la derecha
P1="$(tmux split-window -h -t "$P0" -c "$ROOT" -P -F '#{pane_id}')"
tmux select-pane -t "$P1" -T "BACKEND"
tmux send-keys  -t "$P1" "cd \"$ROOT\"" C-m

# Split horizontal otra vez sobre P1: crea P2 a la derecha
P2="$(tmux split-window -h -t "$P1" -c "$ROOT" -P -F '#{pane_id}')"
tmux select-pane -t "$P2" -T "QA/TESTS"
tmux send-keys  -t "$P2" "cd \"$ROOT\"" C-m

# Split vertical bajo cada pane del top row:
P3="$(tmux split-window -v -t "$P0" -c "$ROOT" -P -F '#{pane_id}')"
tmux select-pane -t "$P3" -T "DOCS/NOTION"
tmux send-keys  -t "$P3" "cd \"$ROOT\"" C-m

P4="$(tmux split-window -v -t "$P1" -c "$ROOT" -P -F '#{pane_id}')"
tmux select-pane -t "$P4" -T "DEVOPS/DEPLOY"
tmux send-keys  -t "$P4" "cd \"$ROOT\"" C-m

P5="$(tmux split-window -v -t "$P2" -c "$ROOT" -P -F '#{pane_id}')"
tmux select-pane -t "$P5" -T "INTEGRATIONS"
tmux send-keys  -t "$P5" "cd \"$ROOT\"" C-m

tmux select-layout -t "$SESSION:$WIN" tiled

echo "Created tmux session '$SESSION' window '$WIN' with 6 panes."
echo "Pane IDs: $P0 $P1 $P2 $P3 $P4 $P5"
echo "Prefix per your config: Ctrl-s"
exec tmux attach -t "$SESSION"
