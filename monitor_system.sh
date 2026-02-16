#!/bin/bash

LOG_DIR="$HOME/sys_monitor"
HISTORY_FILE="$LOG_DIR/history.log"
ALERT_FILE="$LOG_DIR/alerts.log"

# PROGI DOMYŚLE
CPU_LIMIT=95
DISK_LIMIT=95
SERVICES=("sshd" "nginx")

mkdir -p "$LOG_DIR"

# FUNKCJE ZAPISUJĄCE DANE
log_info() {
    echo "$(date '+%F %T') [INFO] $1" >> "$HISTORY_FILE"
}

log_alert() {
    echo "$(date '+%F %T') [ALERT] $1" >> "$ALERT_FILE"
}

# PARAMETRYZACJA
while [[ $# -gt 0 ]]; do
    case "$1" in
        --cpu) CPU_LIMIT="$2"; shift 2 ;;
        --disk) DISK_LIMIT="$2"; shift 2 ;;
        --services)
            shift
            SERVICES=()
            while [[ $# -gt 0 && "$1" != --* ]]; do
                SERVICES+=("$1")
                shift
            done
            ;;
        *)
            echo "Nieznana opcja: $1"
            echo "Użycie: $0 [--cpu <limit>] [--disk <limit>] [--services <svc1 svc2 ...>]"
            exit 1 ;;
    esac
done

# ZBIERANIE DANYCH
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print int(100 - $8)}')
mem_usage=$(free | awk '/Mem/{print int($3/$2*100)}')
disk_usage=$(df / | awk 'NR==2 {print int($5)}')


log_info "=== Raport z monitoringu systemu $(date '+%F %T') ==="
log_info "Progi: CPU>${CPU_LIMIT}% | DYSK>${DISK_LIMIT}% | Usługi: ${SERVICES[@]}"
log_info "CPU:${cpu_usage}% MEM:${mem_usage}% DISK_FREE:${disk_usage}%"

# SPRAWDZANIE PROGÓW 
if [[ "$cpu_usage" -gt "$CPU_LIMIT" ]]; then
    log_alert "CPU przekroczyło ${CPU_LIMIT}% (jest ${cpu_usage}%)"
fi

if [[ "$disk_usage" -gt "$DISK_LIMIT" ]]; then
    log_alert "Dysk powyżej ${DISK_LIMIT}% wolnego miejsca (jest ${disk_usage}%)"
fi

# SPRAWDZANIE DOSTĘPNOŚCI USŁUG
for svc in "${SERVICES[@]}"; do
    if systemctl is-active --quiet "$svc"; then
        log_info "Usługa $svc działa poprawnie."
    else
        log_alert "Usługa $svc nie działa!"
    fi
done

# BŁEDY SYSLOG
log_info "--- Ostatnie błędy z /var/log/syslog ---"
if [ -r /var/log/syslog ]; then
    grep -i "error" /var/log/syslog 2>/dev/null | tail -n 5 >> "$HISTORY_FILE"
else
    log_info "Brak dostępu do syslog."
fi

# NIEUDANE LOGOWANIA (ROOT)
if [ -r /var/log/auth.log ]; then
    failed_root=$(grep "Failed password for root" /var/log/auth.log 2>/dev/null | tail -n 3)
    [ -n "$failed_root" ] && {
        log_alert "Nieudane logowania jako root!"
        echo "$failed_root" >> "$ALERT_FILE"
    }
fi

echo "Logi zapisane w: $LOG_DIR"
