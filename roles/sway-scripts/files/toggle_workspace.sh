#!/usr/bin/env bash

# Datei für Workspace-History
HISTORY_FILE="/tmp/sway_last_workspace.txt"

# Aktuell fokussierten Workspace ermitteln
current=$(swaymsg -t get_workspaces | jq -r '.[] | select(.focused==true) | .name')

# Letzten Workspace aus Datei lesen
last=$(cat "$HISTORY_FILE" 2>/dev/null || echo "")

# Wenn es einen gültigen letzten Workspace gibt und er anders ist als der aktuelle → toggle
if [[ -n "$last" && "$last" != "$current" ]]; then
    swaymsg workspace "$last"
fi

# Nach der Aktion den vorherigen Workspace auf jeden Fall aktualisieren
# Damit beim nächsten Toggle das aktuelle als letzter Workspace gilt
echo "$current" > "$HISTORY_FILE"