import subprocess
import sys

def ps(cmd):
    return subprocess.run(
        ["powershell", "-Command", cmd],
        capture_output=True,
        text=True
    )

try:
    # Admin check
    if "True" not in ps(
        "([Security.Principal.WindowsPrincipal]"
        "[Security.Principal.WindowsIdentity]::GetCurrent()"
        ").IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)"
    ).stdout:
        print("Administratorrechten vereist.")
        sys.exit(1)

    # Status controleren
    status = ps(
        "Get-MpComputerStatus | "
        "Select-Object -ExpandProperty RealTimeProtectionEnabled"
    ).stdout.strip()

    print(f"Realtime Protection status: {status}")

    # Uitschakelen
    ps("Set-MpPreference -DisableRealtimeMonitoring $true")
    print("Realtime Protection uitgeschakeld.")

except Exception as e:
    print("Fout tijdens uitvoering.")
    print(e)