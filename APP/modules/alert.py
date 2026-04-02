from twilio.rest import Client
import datetime
import time

account_sid = 'AC1590ff3a################'
auth_token = 'bd3cb60676ea67269cdfdd########'
twilio_number = '+1 260 254 88###'
target_number = '+977984188######'

client = Client(account_sid, auth_token)

# Cooldown tracking (per source)
last_alert_time = {}

ALERT_COOLDOWN = 300  # 5 minutes (in seconds)


def send_alert(source_id):
    """
    Sends SMS alert if cooldown passed.
    """
    current_time = time.time()

    # Check cooldown
    if source_id in last_alert_time:
        elapsed = current_time - last_alert_time[source_id]
        if elapsed < ALERT_COOLDOWN:
            print(f"[ALERT] Skipped (cooldown active: {int(300 - elapsed)}s left)")
            return

    try:
        message = client.messages.create(
            body=f"Violence Detected in {source_id} at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            from_=twilio_number,
            to=target_number
        )

        last_alert_time[source_id] = current_time
        print(f"[ALERT] Message sent! SID: {message.sid}")

    except Exception as e:
        print(f"[ALERT ERROR] {e}")